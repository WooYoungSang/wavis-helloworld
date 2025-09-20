#!/bin/bash
#
# BDD Test Runner for Demeter Projects
# Executes Gherkin scenarios using appropriate BDD frameworks
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
FEATURES_DIR="$PROJECT_ROOT/features"
SSOT_DIR="$PROJECT_ROOT/demeter/core/ssot"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}✓ $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Detect project language and BDD framework
detect_bdd_framework() {
    if [ -f "$PROJECT_ROOT/go.mod" ]; then
        echo "godog"
    elif [ -f "$PROJECT_ROOT/package.json" ]; then
        if grep -q "@cucumber/cucumber" "$PROJECT_ROOT/package.json" 2>/dev/null; then
            echo "cucumber-js"
        else
            echo "unknown"
        fi
    elif [ -f "$PROJECT_ROOT/requirements.txt" ] || [ -f "$PROJECT_ROOT/pyproject.toml" ]; then
        if grep -q "behave" "$PROJECT_ROOT/requirements.txt" 2>/dev/null || grep -q "behave" "$PROJECT_ROOT/pyproject.toml" 2>/dev/null; then
            echo "behave"
        else
            echo "unknown"
        fi
    else
        echo "unknown"
    fi
}

# Generate feature files if they don't exist
generate_features_if_needed() {
    if [ ! -d "$FEATURES_DIR" ] || [ -z "$(ls -A "$FEATURES_DIR" 2>/dev/null)" ]; then
        log "No feature files found. Generating from UoW definitions..."

        if command -v python3 &> /dev/null; then
            python3 "$SCRIPT_DIR/generate-features.py" --ssot-dir "$SSOT_DIR" --output-dir "$FEATURES_DIR"
            log "Feature files generated successfully"
        else
            error "Python3 not found. Cannot generate feature files."
            exit 1
        fi
    else
        info "Feature files already exist in $FEATURES_DIR"
    fi
}

# Run BDD tests with Godog (Go)
run_godog_tests() {
    log "Running BDD tests with Godog..."

    # Check if godog is installed
    if ! command -v godog &> /dev/null; then
        warn "Godog not found. Installing..."
        go install github.com/cucumber/godog/cmd/godog@latest
    fi

    # Create godog configuration if it doesn't exist
    if [ ! -f "$PROJECT_ROOT/godog.yml" ]; then
        cat > "$PROJECT_ROOT/godog.yml" << EOF
# Godog BDD Test Configuration
default:
  paths:
    - features
  format: pretty,junit:godog-report.xml
  tags: ~@skip
  concurrency: 4
  strict: false
  stop-on-failure: false

# Step definitions location
# These will be implemented in Go files
step-definitions: |
  internal/bdd/steps
EOF
    fi

    # Run godog tests
    cd "$PROJECT_ROOT"
    if godog run; then
        log "All BDD tests passed!"
        return 0
    else
        error "Some BDD tests failed"
        return 1
    fi
}

# Run BDD tests with Cucumber.js (TypeScript/JavaScript)
run_cucumber_js_tests() {
    log "Running BDD tests with Cucumber.js..."

    # Check if cucumber is available
    if [ ! -f "$PROJECT_ROOT/node_modules/.bin/cucumber-js" ] && ! command -v cucumber-js &> /dev/null; then
        warn "Cucumber.js not found. Installing..."
        npm install --save-dev @cucumber/cucumber
    fi

    # Create cucumber configuration if it doesn't exist
    if [ ! -f "$PROJECT_ROOT/cucumber.js" ]; then
        cat > "$PROJECT_ROOT/cucumber.js" << 'EOF'
// Cucumber.js Configuration
module.exports = {
  default: {
    paths: ['features/**/*.feature'],
    require: ['src/test/bdd/steps/**/*.ts'],
    requireModule: ['ts-node/register'],
    format: ['pretty', 'json:cucumber-report.json'],
    formatOptions: { snippetInterface: 'async-await' },
    parallel: 2,
    strict: false,
    dryRun: false,
    failFast: false,
    tags: 'not @skip',
  }
};
EOF
    fi

    # Run cucumber tests
    cd "$PROJECT_ROOT"
    if npx cucumber-js; then
        log "All BDD tests passed!"
        return 0
    else
        error "Some BDD tests failed"
        return 1
    fi
}

# Run BDD tests with Behave (Python)
run_behave_tests() {
    log "Running BDD tests with Behave..."

    # Check if behave is installed
    if ! command -v behave &> /dev/null; then
        warn "Behave not found. Installing..."
        pip3 install behave
    fi

    # Create behave configuration if it doesn't exist
    if [ ! -f "$PROJECT_ROOT/behave.ini" ]; then
        cat > "$PROJECT_ROOT/behave.ini" << EOF
[behave]
paths = features
default_format = pretty
format = pretty,json.pretty:behave-report.json
tags = ~@skip
parallel = 4
stop = false
strict = false

[behave.formatters]
json.pretty = behave.formatter.json:PrettyJSONFormatter

[behave.userdata]
test_environment = development
EOF
    fi

    # Run behave tests
    cd "$PROJECT_ROOT"
    if behave; then
        log "All BDD tests passed!"
        return 0
    else
        error "Some BDD tests failed"
        return 1
    fi
}

# Update UoW tracker based on test results
update_uow_tracker() {
    local test_result=$1

    if command -v python3 &> /dev/null; then
        if [ -f "$SCRIPT_DIR/../tools/update-uow-from-bdd.py" ]; then
            python3 "$SCRIPT_DIR/../tools/update-uow-from-bdd.py" --test-result "$test_result" --project-root "$PROJECT_ROOT"
        else
            info "UoW tracker update script not found"
        fi
    fi
}

# Generate BDD test report
generate_bdd_report() {
    local test_result=$1

    log "Generating BDD test report..."

    # Create reports directory
    mkdir -p "$PROJECT_ROOT/reports/bdd"

    # Generate summary report
    cat > "$PROJECT_ROOT/reports/bdd/summary.md" << EOF
# BDD Test Report

**Generated**: $(date)
**Test Result**: $test_result
**Features Directory**: $FEATURES_DIR

## Test Execution Summary

$(if [ "$test_result" = "PASS" ]; then
    echo "✅ All BDD scenarios passed"
else
    echo "❌ Some BDD scenarios failed"
fi)

## Feature Files Executed

$(if [ -d "$FEATURES_DIR" ]; then
    find "$FEATURES_DIR" -name "*.feature" -exec basename {} \; | sed 's/^/- /'
else
    echo "No feature files found"
fi)

## Next Steps

$(if [ "$test_result" = "FAIL" ]; then
    echo "1. Review failed scenarios in test output"
    echo "2. Fix implementation issues"
    echo "3. Update UoW status in tracker"
    echo "4. Re-run BDD tests"
else
    echo "1. Update UoW tracker with completed status"
    echo "2. Proceed to next development phase"
    echo "3. Consider adding more test scenarios"
fi)

---
Generated by Demeter BDD Test Runner
EOF

    log "BDD report saved to: $PROJECT_ROOT/reports/bdd/summary.md"
}

# Main execution
main() {
    echo -e "${BLUE}"
    echo "🥒 ======================================"
    echo "   Demeter BDD Test Runner"
    echo "   Behavior-Driven Development Execution"
    echo "======================================${NC}"
    echo

    # Detect BDD framework
    BDD_FRAMEWORK=$(detect_bdd_framework)
    info "Detected BDD framework: $BDD_FRAMEWORK"

    # Generate features if needed
    generate_features_if_needed

    # Run tests based on framework
    local test_result="UNKNOWN"

    case $BDD_FRAMEWORK in
        "godog")
            if run_godog_tests; then
                test_result="PASS"
            else
                test_result="FAIL"
            fi
            ;;
        "cucumber-js")
            if run_cucumber_js_tests; then
                test_result="PASS"
            else
                test_result="FAIL"
            fi
            ;;
        "behave")
            if run_behave_tests; then
                test_result="PASS"
            else
                test_result="FAIL"
            fi
            ;;
        "unknown")
            warn "No BDD framework detected. Available options:"
            warn "- Go: Install godog (go install github.com/cucumber/godog/cmd/godog@latest)"
            warn "- TypeScript/JavaScript: Install @cucumber/cucumber (npm install --save-dev @cucumber/cucumber)"
            warn "- Python: Install behave (pip3 install behave)"
            exit 1
            ;;
    esac

    # Update UoW tracker
    update_uow_tracker "$test_result"

    # Generate report
    generate_bdd_report "$test_result"

    echo
    if [ "$test_result" = "PASS" ]; then
        log "🎉 All BDD tests completed successfully!"
        exit 0
    else
        error "❌ Some BDD tests failed. Check output above for details."
        exit 1
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --features-dir)
            FEATURES_DIR="$2"
            shift 2
            ;;
        --generate-only)
            generate_features_if_needed
            exit 0
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --features-dir DIR    Specify features directory (default: ./features)"
            echo "  --generate-only       Only generate feature files, don't run tests"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            warn "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main function
main "$@"