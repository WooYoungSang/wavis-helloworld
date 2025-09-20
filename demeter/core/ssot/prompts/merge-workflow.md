# SSOT Merge Workflow Guide

## Overview
This guide provides detailed instructions for merging base SSOT files with domain extensions to create a complete project-specific SSOT.

## Merge Process

### 1. File Loading Order

#### Base Files (Load First):
```
demeter/core/ssot/base/
├── fr-base.yaml          → functional_requirements
├── nfr-base.yaml         → non_functional_requirements
└── uow-base.yaml         → units_of_work
```

#### Extension Files (Merge Second):
```
demeter/core/ssot/extensions/
├── domain/
│   ├── e-commerce.yaml   → E-commerce specific requirements
│   ├── fintech.yaml      → Financial technology requirements
│   └── healthcare.yaml   → Healthcare specific requirements
├── features/
│   ├── ai-ml.yaml        → AI/ML integration requirements
│   ├── blockchain.yaml   → Blockchain features
│   └── iot.yaml          → IoT connectivity
└── compliance/
    ├── gdpr.yaml         → GDPR compliance requirements
    ├── hipaa.yaml        → HIPAA compliance requirements
    └── pci-dss.yaml      → PCI-DSS compliance requirements
```

### 2. ID Conflict Resolution

#### Conflict Detection:
- Compare all IDs from extensions against base SSOT
- Identify any duplicate IDs (FR-001, NFR-001, UoW-001, etc.)

#### Resolution Strategy:
```
Original ID: FR-001 (from base)
Conflicting ID: FR-001 (from e-commerce extension)
↓
Resolution: Rename extension ID to FR-ECOMMERC-001
```

#### Extension Prefixes:
- **e-commerce** → `ECOMMERC`
- **fintech** → `FINTECH`
- **healthcare** → `HEALTH`
- **ai-ml** → `AIML`
- **blockchain** → `BLOCKCHAIN`
- **iot** → `IOT`
- **gdpr** → `GDPR`
- **hipaa** → `HIPAA`
- **pci-dss** → `PCIDSS`

### 3. Dependency Update Process

#### Track ID Changes:
```yaml
# ID Mapping Table
original_to_new:
  FR-001: FR-ECOMMERC-001
  NFR-002: NFR-GDPR-002
  UoW-301: UoW-HEALTH-301
```

#### Update References:
```yaml
# Before
UoW-302:
  dependencies: ["UoW-301"]
  implements: ["FR-001", "NFR-002"]

# After
UoW-302:
  dependencies: ["UoW-HEALTH-301"]
  implements: ["FR-ECOMMERC-001", "NFR-GDPR-002"]
```

### 4. Merge Rules

#### Priority Rules:
1. **Base takes precedence** for ID conflicts
2. **Extensions get prefixed** to avoid conflicts
3. **Metadata is combined** from all sources
4. **Dependencies are updated** after all merges

#### Section Merging:
```yaml
# Result structure
functional_requirements:
  # Base FRs (unchanged)
  FR-001: {base FR data}
  FR-002: {base FR data}

  # Extension FRs (prefixed if conflicts)
  FR-ECOMMERC-001: {extension FR data}
  FR-GDPR-001: {extension FR data}

non_functional_requirements:
  # Similar pattern
  NFR-001: {base NFR data}
  NFR-ECOMMERC-001: {extension NFR data}

units_of_work:
  # Similar pattern
  UoW-001: {base UoW data}
  UoW-ECOMMERC-301: {extension UoW data}
```

### 5. Validation Steps

#### Dependency Validation:
- [ ] All `dependencies` arrays reference existing IDs
- [ ] All `implements` arrays reference existing IDs
- [ ] No circular dependencies exist
- [ ] UoW layer dependencies are logical

#### Cross-Reference Validation:
- [ ] Every FR is implemented by at least one UoW
- [ ] Every NFR is addressed by at least one UoW
- [ ] No orphaned requirements or UoWs

#### Structure Validation:
- [ ] All required fields present in each item
- [ ] Priority values are valid (Critical/High/Medium/Low)
- [ ] Layer values are valid (Foundation/Infrastructure/Application/Integration/Deployment)

### 6. Statistics Generation

#### Count Statistics:
```yaml
statistics:
  total_functional_requirements: 24
  total_non_functional_requirements: 13
  total_units_of_work: 30
  id_conflicts_resolved: 8
```

#### Priority Distribution:
```yaml
fr_by_priority:
  Critical: 8
  High: 12
  Medium: 3
  Low: 1
```

#### Layer Distribution:
```yaml
uow_by_layer:
  Foundation: 5
  Infrastructure: 8
  Application: 12
  Integration: 3
  Deployment: 2
```

#### Effort Estimation:
```yaml
estimated_total_effort_hours: 720
average_effort_per_uow: 24
```

### 7. Metadata Combination

#### Final Metadata Structure:
```yaml
metadata:
  # Project Information
  project_name: "Project Name"
  project_extensions: "e-commerce"

  # Merge Information
  merge_timestamp: "2025-01-19T10:30:00Z"
  extensions_merged: ["e-commerce", "gdpr"]

  # Base Metadata
  base_version: "1.0.0"
  framework_version: "Demeter v1.3"

  # Statistics
  statistics: {as above}

  # Quality Metrics
  coverage:
    fr_implemented: "100%"
    nfr_addressed: "95%"
    dependency_completeness: "100%"
```

### 8. Output Format

#### Complete Merged SSOT:
```yaml
functional_requirements:
  FR-001:
    name: "Configuration Management"
    description: "System must support structured configuration..."
    priority: "Critical"
    business_value: "Secure, maintainable configuration management"
    acceptance_criteria:
      - "Load configuration from structured files..."
    tags: ["foundation", "security", "config"]

  FR-ECOMMERC-001:
    name: "Product Catalog Management"
    description: "Comprehensive product catalog with categories..."
    priority: "Critical"
    dependencies: ["FR-003", "FR-004"]
    business_value: "Core e-commerce functionality"
    acceptance_criteria:
      - "Product CRUD operations..."
    tags: ["product", "catalog", "inventory"]

non_functional_requirements:
  NFR-001:
    name: "Performance"
    description: "System must handle specified load..."
    category: "Performance"
    measurement_criteria:
      - "Response time: < 200ms (95th percentile)"
    testing_method: "Load testing, performance profiling"
    priority: "High"

units_of_work:
  UoW-000:
    name: "Project Structure Setup"
    goal: "Establish architecture foundation"
    layer: "Foundation"
    priority: "Critical"
    dependencies: []
    implements: ["NFR-005"]
    estimated_effort_hours: "8"
    acceptance_criteria:
      - "Standard project layout..."

metadata:
  {complete metadata as above}
```

### 9. Quality Assurance

#### Pre-Merge Validation:
- [ ] All input files are valid YAML
- [ ] All input files follow SSOT schema
- [ ] Base directory contains required files

#### Post-Merge Validation:
- [ ] No syntax errors in output
- [ ] All dependencies resolved
- [ ] Statistics are accurate
- [ ] No data loss during merge

#### Error Handling:
- Report missing files with clear error messages
- Identify and report circular dependencies
- Validate ID format compliance
- Check for required field completeness