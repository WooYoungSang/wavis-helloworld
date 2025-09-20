# Phase 0: AI-Driven Project Initialization

## 🎯 Mission
Initialize a new project using the Demeter WAVIS Framework v1.3 with complete AI-driven setup and GraphRAG knowledge management. Replace all manual setup.sh operations with intelligent automation.

## 📋 Initialization Tasks

### 1. Project Structure Creation
Create the complete project directory structure:

```
project-root/
├── docs/
│   ├── SSOT.md                  # Main requirements document
│   └── architecture/            # Architecture documentation
├── src/                         # Source code (technology-specific)
├── tests/                       # Test suites
├── config/                      # Configuration files
├── scripts/                     # Utility scripts
├── deployments/                 # Deployment configurations
├── graphrag/                    # GraphRAG knowledge base
│   ├── knowledge/
│   │   └── project-knowledge.md # Central knowledge tracking
│   ├── patterns/                # Architectural patterns
│   ├── lessons/                 # Lessons learned
│   ├── components/              # Reusable components
│   └── queries/                 # Query examples
├── batch/                       # UoW batch execution system
│   ├── configs/
│   ├── prompts/
│   ├── logs/
│   └── reports/
├── CLAUDE.md                    # AI development guidelines
├── LEARNING.md                  # Learning and progress tracker
└── README.md                    # Project documentation
```

### 2. SSOT Template Generation
Create a comprehensive SSOT template based on user requirements:

**2.1 Project Metadata**
```yaml
metadata:
  project_name: "[PROJECT_NAME]"
  description: "[PROJECT_DESCRIPTION]"
  version: "1.0.0"
  created: "[CURRENT_DATE]"
  framework: "Demeter WAVIS v1.3"
  mvp_phase: "[MVP_DEFINITION]"
```

**2.2 Functional Requirements Template**
```yaml
functional_requirements:
  FR-001:
    name: "Core System Setup"
    description: "Basic system infrastructure and configuration"
    priority: "High"
    category: "Foundation"
    stakeholders: ["Development Team"]

  # Add domain-specific FRs based on user selection
```

**2.3 Non-Functional Requirements Template**
```yaml
non_functional_requirements:
  NFR-001:
    name: "Performance Standards"
    description: "System performance requirements"
    category: "Performance"
    metrics:
      response_time: "< 200ms"
      throughput: "> 1000 req/sec"

  NFR-002:
    name: "Security Requirements"
    description: "Security and compliance standards"
    category: "Security"
    compliance: ["GDPR", "SOC2"]
```

**2.4 Units of Work Template**
```yaml
units_of_work:
  UoW-001:
    name: "Foundation Setup"
    description: "Setup basic project infrastructure"
    layer: "Foundation"
    implements: ["FR-001"]
    satisfies: ["NFR-001"]
    dependencies: []
    estimated_effort_hours: 8
    acceptance_criteria:
      AC-1:
        description: "Project structure is created"
        scenario:
          given: "Empty project directory"
          when: "Foundation setup is executed"
          then: "All required directories and files exist"
```

### 3. GraphRAG Knowledge Base Initialization
**Command**: `"Initialize GraphRAG knowledge base for [PROJECT_TYPE] project with framework patterns"`

**3.1 Create Project Knowledge Base**
Use the project-knowledge.md template and populate with:
- Project metadata and overview
- Initial architecture decisions
- Technology stack selections
- MVP scope and constraints

**3.2 Initialize Pattern Templates**
Create pattern templates for common architectural patterns:
- Dependency injection patterns
- Error handling strategies
- Interface design patterns
- Testing patterns and strategies

**3.3 Create Component Library Structure**
Initialize reusable component templates:
- Utility function templates
- Service layer templates
- Middleware templates
- Configuration templates

**3.4 Initialize Lesson Templates**
Create lesson learned templates for:
- Technical challenge lessons
- Process improvement lessons
- Quality improvement lessons
- Integration strategy lessons

**3.5 Setup Query Examples**
Populate query examples for:
- Pattern discovery queries
- Component search queries
- Lesson application queries
- Technology-specific queries

### 4. Development Guidelines Setup
**4.1 Create CLAUDE.md**
Generate comprehensive AI development guidelines based on project requirements and selected technology stack.

**4.2 Create LEARNING.md**
Initialize learning and progress tracking document with MVP milestones.

### 5. Configuration Files
**5.1 GraphRAG Configuration**
```yaml
# .graphrag_config.yaml
graphrag:
  enabled: true
  directory: "./graphrag"
  knowledge_integration: "prompt_based"
  auto_documentation: true
  pattern_discovery: true

  knowledge_types:
    patterns: true
    lessons: true
    components: true
    queries: true

  metrics:
    track_reuse: true
    track_effectiveness: true
    track_quality_impact: true
```

**5.2 Git Configuration**
```
# .gitignore additions
# Logs
batch/logs/
*.log

# Temporary files
.tmp/
temp/

# IDE files
.vscode/
.idea/

# Environment files
.env
.env.local
```

### 6. README Generation
Create comprehensive README.md with:
- Project overview and goals
- Quick start guide
- Development workflow
- Technology stack information
- Contributing guidelines

## 🤖 AI Integration Instructions

### Context Awareness
1. **Analyze user inputs** for project requirements
2. **Detect technology preferences** from user responses
3. **Identify domain characteristics** (e-commerce, fintech, etc.)
4. **Determine MVP scope** and complexity

### Intelligent Customization
1. **Domain-specific templates**: Customize SSOT based on domain
2. **Technology adaptation**: Adjust structure for chosen tech stack
3. **Compliance requirements**: Include necessary regulatory compliance
4. **Performance targets**: Set appropriate NFRs for project scale

### Quality Assurance
1. **Validate structure completeness**: Ensure all required files exist
2. **Check template consistency**: Verify YAML syntax and structure
3. **Verify GraphRAG setup**: Confirm knowledge base initialization
4. **Test prompt integration**: Ensure seamless Phase 1 transition

## 📊 Success Criteria

### Phase 0 Completion Checklist
- [ ] Complete directory structure created
- [ ] SSOT template generated with project-specific content
- [ ] GraphRAG knowledge base initialized with all templates
- [ ] GraphRAG patterns, lessons, components, and queries directories created
- [ ] Project documentation (README, CLAUDE.md, LEARNING.md) created
- [ ] GraphRAG configuration files properly set up
- [ ] Git repository initialized with appropriate .gitignore
- [ ] All templates customized for chosen domain and technology
- [ ] GraphRAG query examples populated
- [ ] Ready for Phase 1: SSOT Requirements Definition with GraphRAG integration

### Quality Gates
- [ ] All YAML files are syntactically valid
- [ ] Documentation is comprehensive and accurate
- [ ] GraphRAG structure follows framework standards
- [ ] GraphRAG templates are properly initialized
- [ ] Project structure supports chosen technology stack
- [ ] Configuration enables smooth Phase 1 transition
- [ ] GraphRAG knowledge integration is properly configured

## 🔄 Next Phase Preparation
Upon completion, the project should be ready for Phase 1 where requirements will be defined and refined using the initialized SSOT template.

**Expected transition**: User can immediately begin working on `docs/SSOT.md` to define specific functional and non-functional requirements.

---

*Execute this prompt in Claude Code to initialize a new Demeter v1.3 project with complete AI-driven setup and GraphRAG knowledge management*