# SSOT Template Generation Guide

## Overview
Convert merged SSOT YAML data into comprehensive Markdown documentation for development teams.

## Document Structure

### 1. Header Section
```markdown
# Single Source of Truth (SSOT) - {Project Name}

## Project Overview
{Project description and context}

**Technology Stack**: {Technology} {Version}+
**Architecture**: Clean Architecture with SSOT-driven development
**Knowledge Management**: GraphRAG integration for context-aware development
```

### 2. Functional Requirements Section

#### Format for Each FR:
```markdown
### FR-001: Configuration Management
**Description**: System must support structured configuration with schema validation
**Priority**: Critical
**Dependencies**: [List if any]
**Business Value**: Secure, maintainable configuration management
**Acceptance Criteria**:
- Load configuration from structured files with schema validation
- Support environment-specific configurations (dev, test, prod)
- Hot-reload capability without service restart
- No environment variables for configuration (security requirement)
```

#### Processing Rules:
- Extract from `functional_requirements` section of YAML
- Sort by ID (FR-001, FR-002, etc.)
- Include all fields: name, description, priority, dependencies, business_value, acceptance_criteria
- Convert YAML arrays to markdown bullet lists
- Handle missing fields gracefully (show "Not specified" if empty)

### 3. Non-Functional Requirements Section

#### Format for Each NFR:
```markdown
### NFR-001: Performance
**Description**: System must handle specified load with acceptable latency
**Category**: Performance
**Measurement Criteria**:
- Response time: < 200ms (95th percentile) for API calls
- Throughput: > 1000 requests/second
- Memory usage: < 512MB baseline
**Testing Method**: Load testing, performance profiling
**Priority**: High
```

#### Processing Rules:
- Extract from `non_functional_requirements` section
- Include: name, description, category, measurement_criteria, testing_method, priority
- Group by category if desired (Performance, Security, Usability, etc.)

### 4. Units of Work Section

#### Format for Each UoW:
```markdown
### UoW-000: Project Structure Setup
**Goal**: Establish architecture foundation
**Layer**: Foundation
**Priority**: Critical
**Dependencies**: []
**Implements**: NFR-005
**Estimated Effort**: 8 hours
**Acceptance Criteria**:
- Standard project layout with clear directory structure
- Architecture layers clearly defined and documented
- Module interfaces defined for dependency injection
```

#### Processing Rules:
- Extract from `units_of_work` section
- Group by layer for better organization
- Show dependency chains clearly
- Convert effort hours to readable format

### 5. Cross-Reference Matrices

#### FR to UoW Mapping Table:
```markdown
### FR to UoW Mapping
| Functional Requirement | Primary UoWs | Validation Method |
|------------------------|--------------|-------------------|
| FR-001 (Configuration Management) | UoW-101, UoW-102 | Unit + Integration tests |
| FR-002 (HTTP API Server) | UoW-103, UoW-104 | Unit + Integration tests |
```

#### Generation Logic:
1. For each FR, find UoWs where `implements` array contains the FR ID
2. List all implementing UoWs
3. Default validation method: "Unit + Integration tests"

#### NFR to UoW Mapping Table:
```markdown
### NFR to UoW Mapping
| Non-Functional Requirement | Related UoWs | Measurement Method | Target Value |
|-----------------------------|--------------|-------------------|--------------|
| NFR-001 (Performance) | UoW-201, UoW-301 | Load testing | < 200ms response |
```

#### Generation Logic:
1. For each NFR, find UoWs where `implements` array contains the NFR ID
2. Extract measurement method from NFR data
3. Extract target value from measurement_criteria (first item)

#### UoW Dependency Matrix:
```markdown
### UoW Dependency Matrix
**Foundation**: UoW-000 → UoW-101 → UoW-102
**Infrastructure**: UoW-201 → UoW-202 → UoW-203
**Application**: UoW-301 → UoW-302 → UoW-303
**Integration**: UoW-401 → UoW-402
**Deployment**: UoW-501 → UoW-502
```

#### Generation Logic:
1. Group UoWs by layer
2. Sort within each layer by ID
3. Show dependency chains using `dependencies` arrays
4. Use arrow notation (→) for flow

### 6. Implementation Guidelines

#### Standard Section:
```markdown
## Implementation Guidelines

### Development Sequence
1. **Prerequisites First**: Complete foundation layer before implementation
2. **Layer by Layer**: Complete each layer before proceeding
3. **Dependency Respect**: Never implement a UoW before its dependencies
4. **Testing Priority**: Write tests first (TDD approach)
5. **Documentation**: Update documentation with each UoW

### Quality Gates
- **Foundation UoWs**: 80%+ test coverage, architectural review required
- **Infrastructure UoWs**: Integration testing, security review required
- **Business UoWs**: 60%+ test coverage, business logic validation required
- **Deployment UoWs**: End-to-end testing, security scanning required
```

### 7. Statistics and Metadata

#### Footer Section:
```markdown
---

**Template Version**: {from metadata.version}
**Framework**: SSOT-Driven Development with GraphRAG
**Generated**: {current timestamp}
**Statistics**: {N} FRs, {N} NFRs, {N} UoWs

### Project Statistics
- **Total Functional Requirements**: 24
- **Total Non-Functional Requirements**: 13
- **Total Units of Work**: 30
- **Estimated Total Effort**: 720 hours

### Priority Distribution
- **Critical**: 8 requirements
- **High**: 12 requirements
- **Medium**: 6 requirements
- **Low**: 1 requirement

### Layer Distribution
- **Foundation**: 5 UoWs
- **Infrastructure**: 8 UoWs
- **Application**: 12 UoWs
- **Integration**: 3 UoWs
- **Deployment**: 2 UoWs
```

## Generation Process

### 1. YAML Loading
```python
# Load and validate YAML structure
with open(input_yaml, 'r') as f:
    ssot_data = yaml.safe_load(f)

# Expected structure
assert 'functional_requirements' in ssot_data
assert 'non_functional_requirements' in ssot_data
assert 'units_of_work' in ssot_data
assert 'metadata' in ssot_data
```

### 2. Data Processing

#### Sort Items by ID:
- FRs: FR-001, FR-002, FR-CUSTOM-001, etc.
- NFRs: NFR-001, NFR-002, NFR-CUSTOM-001, etc.
- UoWs: UoW-000, UoW-001, UoW-CUSTOM-301, etc.

#### Build Cross-References:
```python
# FR to UoW mapping
fr_to_uow = {}
for uow_id, uow_data in units_of_work.items():
    for fr_id in uow_data.get('implements', []):
        if fr_id.startswith('FR-'):
            fr_to_uow.setdefault(fr_id, []).append(uow_id)
```

### 3. Content Generation

#### Template Processing:
- Use consistent formatting for all sections
- Handle missing or empty fields gracefully
- Maintain proper markdown syntax
- Ensure all cross-references are accurate

#### Error Handling:
- Check for broken references
- Validate all required fields
- Report any data inconsistencies
- Provide clear error messages

### 4. Quality Validation

#### Content Completeness:
- [ ] All FRs from YAML included
- [ ] All NFRs from YAML included
- [ ] All UoWs from YAML included
- [ ] All cross-references generated

#### Format Validation:
- [ ] Valid markdown syntax
- [ ] Consistent formatting
- [ ] Proper table structures
- [ ] Correct heading hierarchy

#### Accuracy Validation:
- [ ] Cross-reference tables accurate
- [ ] Statistics match data
- [ ] No broken internal links
- [ ] Metadata properly included

### 5. Output Requirements

#### File Structure:
```
docs/
├── SSOT.md              # Generated documentation
├── merged-ssot.yaml     # Source data
└── requirements/        # Optional: detailed requirements
```

#### Content Quality:
- **Readable**: Clear structure and formatting
- **Complete**: All requirements and UoWs documented
- **Accurate**: Cross-references and statistics correct
- **Usable**: Easy navigation and reference during development

#### Additional Features:
- Table of contents (optional)
- Quick reference summary
- Development checklist
- Progress tracking template