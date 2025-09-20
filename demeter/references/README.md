# Demeter References

This directory contains reference templates and examples for different technologies and patterns. These are **optional** resources that can be used as starting points when implementing your technology stack.

## Directory Structure

```
references/
├── languages/          # Language-specific templates and examples
│   ├── go/            # Go language templates
│   ├── python/        # Python language templates
│   └── typescript/    # TypeScript language templates
└── patterns/          # Common architectural patterns (future)
```

## How to Use

### Language Templates

The language templates provide technology-specific implementations of common patterns:

1. **Choose your technology stack** based on your project requirements
2. **Copy relevant templates** to your project directory
3. **Adapt templates** to your specific needs and SSOT requirements

### Available Languages

#### Go
- Project structure templates
- Configuration management examples
- HTTP server foundations
- Testing framework setup
- CI/CD pipeline configurations

#### Python
- Project structure templates
- Configuration management examples
- FastAPI/Flask examples
- Testing framework setup
- Dependency management

#### TypeScript
- Project structure templates
- Node.js/Express examples
- Configuration management
- Testing framework setup
- Build system configurations

## Philosophy

Demeter follows the principle that **SSOT defines WHAT to build, technology stack defines HOW to build**. These reference templates help bridge that gap by providing concrete implementations for different technology choices.

## Usage Guidelines

1. **Start with SSOT**: Always begin with your project's SSOT requirements
2. **Choose technology**: Select the most appropriate technology for your requirements
3. **Reference templates**: Use these templates as starting points, not rigid requirements
4. **Adapt and customize**: Modify templates to fit your specific needs
5. **Maintain independence**: Your project should not depend on Demeter after initialization

## Contributing

When adding new language templates:

1. Follow the established directory structure
2. Provide clear documentation
3. Include example implementations of core patterns
4. Ensure templates are technology-agnostic where possible
5. Focus on common patterns rather than specific frameworks

## Technology Selection Criteria

Consider these factors when choosing your technology stack:

- **Performance requirements** (NFR-001)
- **Team expertise** and learning curve
- **Ecosystem maturity** and community support
- **Scalability needs** (NFR-004)
- **Security requirements** (NFR-003)
- **Deployment constraints** (NFR-007)
- **Maintenance considerations** (NFR-005)

---

*Remember: Demeter provides the seed, but your technology choices determine how the project grows.*