# Natural Language to SSOT Conversion Guide

## Analysis Patterns for Converting Requirements

### 1. Functional Requirements Detection

#### Action Patterns:
- **"Users should/must/can..."** → FR-CUSTOM-XXX
- **"System allows/enables/provides..."** → FR-CUSTOM-XXX
- **"Application supports/handles..."** → FR-CUSTOM-XXX

#### User Story Patterns:
- **"As a [actor], I want [action] so that [benefit]"** → FR-CUSTOM-XXX
  - Extract actor, action, and benefit
  - Use action as requirement name
  - Use benefit as business value

#### Feature Descriptions:
- **Bullet points with capabilities** → FR-CUSTOM-XXX
- **"Feature X allows Y"** → FR-CUSTOM-XXX
- **"The system includes X"** → FR-CUSTOM-XXX

### 2. Non-Functional Requirements Detection

#### Performance Indicators:
- **Response time** (ms, seconds) → NFR-CUSTOM-XXX (Performance)
- **Throughput** (requests/second, rps) → NFR-CUSTOM-XXX (Performance)
- **Load capacity** (users, concurrent) → NFR-CUSTOM-XXX (Performance)
- **Availability** (uptime %, nines) → NFR-CUSTOM-XXX (Reliability)

#### Security & Compliance:
- **"Encrypt", "secure", "protect"** → NFR-CUSTOM-XXX (Security)
- **"GDPR", "HIPAA", "PCI-DSS"** → NFR-CUSTOM-XXX (Compliance)
- **"Authentication", "authorization"** → NFR-CUSTOM-XXX (Security)
- **"SSL/TLS", "HTTPS"** → NFR-CUSTOM-XXX (Security)

#### Usability:
- **"User-friendly", "intuitive"** → NFR-CUSTOM-XXX (Usability)
- **"Mobile responsive"** → NFR-CUSTOM-XXX (Usability)
- **"Accessibility", "WCAG"** → NFR-CUSTOM-XXX (Usability)

### 3. Priority Inference Rules

#### Critical Priority:
- **Keywords**: "critical", "essential", "must", "required", "mandatory"
- **Context**: Core functionality, security requirements, compliance

#### High Priority:
- **Keywords**: "important", "should", "high priority", "significant"
- **Context**: Main features, key user flows, major integrations

#### Medium Priority:
- **Default** for most requirements without explicit priority
- **Keywords**: "standard", "typical", "normal"

#### Low Priority:
- **Keywords**: "nice to have", "could", "optional", "enhancement", "future"
- **Context**: Nice-to-have features, future improvements

### 4. Business Value Extraction

#### From User Stories:
- Use the "so that" clause directly
- Example: "so that users can save time" → "Enable time-saving user workflows"

#### From Feature Descriptions:
- Infer from context and benefits mentioned
- Example: "Advanced search" → "Improve user experience and content discovery"

#### Default Patterns:
- For core features: "Deliver core functionality: [feature name]"
- For integrations: "Enable system connectivity and data flow"
- For security: "Ensure system security and compliance"

### 5. Acceptance Criteria Generation

#### For CRUD Operations:
- "Successfully create/add new items"
- "Successfully update existing items"
- "Successfully delete items when requested"
- "Validate input data before processing"

#### For Search/Filter:
- "Return relevant search results"
- "Handle empty search results gracefully"
- "Support multiple search criteria"
- "Provide clear feedback on search status"

#### For Integrations:
- "Successfully connect to external service"
- "Handle API errors gracefully"
- "Validate external data before processing"
- "Maintain system availability during integration failures"

#### For Security Features:
- "Implement according to security standards"
- "Validate all user inputs"
- "Log security events appropriately"
- "Handle authentication failures gracefully"

### 6. Units of Work Grouping

#### User Management Group:
- **Keywords**: "user", "account", "profile", "login", "register", "authentication"
- **UoW Pattern**: "UoW-CUSTOM-301: Implement User Management"

#### Data Management Group:
- **Keywords**: "data", "database", "store", "save", "retrieve", "CRUD"
- **UoW Pattern**: "UoW-CUSTOM-302: Implement Data Management"

#### Search/Discovery Group:
- **Keywords**: "search", "filter", "find", "query", "sort", "recommendation"
- **UoW Pattern**: "UoW-CUSTOM-303: Implement Search and Discovery"

#### Integration Group:
- **Keywords**: "API", "integration", "external", "service", "third-party"
- **UoW Pattern**: "UoW-CUSTOM-304: Implement External Integrations"

#### Business Logic Group:
- **Keywords**: Domain-specific terms, core functionality
- **UoW Pattern**: "UoW-CUSTOM-305: Implement Business Logic"

#### Security Group:
- **Keywords**: "secure", "encrypt", "protect", "authorize", "permission"
- **UoW Pattern**: "UoW-CUSTOM-306: Implement Security Features"

### 7. YAML Structure Template

```yaml
extends: "{domain}"
custom: "{project-name}"

functional_requirements:
  FR-CUSTOM-001:
    name: "Extracted Requirement Name"
    description: "Full description from natural language"
    priority: "Critical|High|Medium|Low"
    business_value: "Business value statement"
    acceptance_criteria:
      - "Specific testable criterion"
      - "Another testable criterion"
    tags: ["custom", "domain-specific"]

non_functional_requirements:
  NFR-CUSTOM-001:
    name: "Quality Attribute Name"
    category: "Performance|Security|Usability|Reliability"
    measurement_criteria:
      - "Measurable criteria with specific values"
    testing_method: "Testing approach description"
    priority: "Critical|High|Medium|Low"
    tags: ["custom", "quality"]

units_of_work:
  UoW-CUSTOM-301:
    name: "Implementation Task Name"
    goal: "Clear implementation objective"
    layer: "Application|Infrastructure|Integration|Deployment"
    priority: "Critical|High|Medium|Low"
    dependencies: ["UoW-XXX"]  # Reference existing UoWs if needed
    implements: ["FR-CUSTOM-001", "NFR-CUSTOM-001"]
    estimated_effort_hours: "24"
    acceptance_criteria:
      - "Specific deliverable"
      - "Testing requirement"
      - "Documentation requirement"
    tags: ["custom", "implementation"]

metadata:
  version: "1.0.0"
  created: "YYYY-MM-DD"
  description: "Custom SSOT for {project-name}"
  generated_from: "Natural language requirements"
  total_custom_frs: N
  total_custom_nfrs: N
  total_custom_uows: N
```

### 8. Quality Assurance Checklist

#### Completeness:
- [ ] All requirements from natural language captured
- [ ] No important features or constraints missed
- [ ] Business rules and constraints identified

#### Structure:
- [ ] Proper YAML format and syntax
- [ ] Consistent ID numbering (FR-CUSTOM-001, 002, etc.)
- [ ] All required fields present

#### Traceability:
- [ ] Clear mapping from natural language to structured format
- [ ] Source context preserved in descriptions
- [ ] Business rationale captured

#### Testability:
- [ ] Specific, measurable acceptance criteria
- [ ] Testable non-functional requirements
- [ ] Clear success metrics defined

#### Dependencies:
- [ ] UoW dependencies properly identified
- [ ] Implements relationships correct
- [ ] No circular dependencies