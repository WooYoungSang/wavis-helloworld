# 🔒 Deployment Security - AI-Driven Security Hardening

## 🎯 Purpose
Apply comprehensive security best practices to both Docker-Compose and Kubernetes deployments. Generate security configurations, policies, and monitoring systems automatically.

## 🚀 Quick Security Commands

### Basic Security Hardening
```markdown
"Apply security best practices to my Docker-Compose/Kubernetes deployment"
```

### Compliance Configuration
```markdown
"Configure deployment for [GDPR/HIPAA/SOX] compliance requirements"
```

### Security Monitoring
```markdown
"Setup security monitoring and intrusion detection for my deployment"
```

---

## 📋 Core Security Operations

### 1. Container Security
**Command**: `"Harden container security configuration"`

**AI will implement**:
```yaml
# Docker-Compose Security
services:
  app:
    build: .
    user: "1000:1000"  # Non-root user
    read_only: true     # Read-only filesystem
    tmpfs:
      - /tmp:noexec,nosuid,nodev
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - DAC_OVERRIDE
    security_opt:
      - no-new-privileges:true
    sysctls:
      - net.core.somaxconn=1024
```

### 2. Network Security
**Command**: `"Setup network isolation and security policies"`

**AI will configure**:
```yaml
# Network Security
networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  backend:
    driver: bridge
    internal: true  # No external access
    ipam:
      config:
        - subnet: 172.21.0.0/16

services:
  app:
    networks:
      - frontend
      - backend
  database:
    networks:
      - backend  # Only internal network
```

### 3. Secrets Management
**Command**: `"Implement secure secrets management"`

**AI will create**:
```yaml
# Docker-Compose Secrets
secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true
    name: production_api_key
  ssl_cert:
    file: ./certs/server.crt
  ssl_key:
    file: ./certs/server.key

services:
  app:
    secrets:
      - source: db_password
        target: /run/secrets/db_password
        mode: 0400
      - api_key
```

---

## 🔐 Advanced Security Features

### SSL/TLS Configuration
**Command**: `"Setup SSL/TLS with automatic certificate management"`

**AI will configure**:
- Automatic certificate generation (Let's Encrypt)
- TLS termination at load balancer
- Internal service encryption
- Certificate rotation policies

### Authentication & Authorization
**Command**: `"Implement authentication and RBAC"`

**AI will setup**:
- OAuth2/OIDC integration
- JWT token validation
- Role-based access control
- API key management

### Security Monitoring
**Command**: `"Setup security monitoring and alerting"`

**AI will deploy**:
```yaml
# Security Monitoring Stack
services:
  falco:
    image: falcosecurity/falco:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock
      - /proc:/host/proc:ro
      - /etc:/host/etc:ro
    command:
      - /usr/bin/falco
      - --k8s-api-endpoint=https://kubernetes.default.svc.cluster.local

  elk-security:
    image: sebp/elk:latest
    ports:
      - "5601:5601"  # Kibana
    environment:
      - ES_MIN_MEM=512m
      - ES_MAX_MEM=1g
```

---

## 🛡️ Compliance Configurations

### GDPR Compliance
**Command**: `"Configure deployment for GDPR compliance"`

**AI will implement**:
- Data encryption at rest and in transit
- Audit logging for data access
- Data anonymization capabilities
- Right to be forgotten functionality
- Consent management integration

### HIPAA Compliance
**Command**: `"Setup HIPAA-compliant deployment"`

**AI will configure**:
- PHI data encryption (AES-256)
- Access control and audit trails
- Network segmentation
- Backup encryption
- Business associate compliance

### SOX Compliance
**Command**: `"Implement SOX compliance controls"`

**AI will setup**:
- Immutable audit logs
- Separation of duties
- Change management controls
- Financial data protection

---

## 🔍 Security Scanning & Validation

### Vulnerability Scanning
**Command**: `"Setup automated vulnerability scanning"`

**AI will configure**:
```yaml
# Vulnerability Scanner
services:
  trivy:
    image: aquasec/trivy:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - trivy-cache:/root/.cache/trivy
    command:
      - image
      - --exit-code=1
      - myapp:latest
```

### Security Baseline Validation
**Command**: `"Validate security baseline compliance"`

**AI will check**:
- Container configuration against CIS benchmarks
- Network policy compliance
- Secret management validation
- Access control verification

### Penetration Testing
**Command**: `"Setup automated security testing"`

**AI will configure**:
- OWASP ZAP integration
- SQL injection testing
- XSS vulnerability scanning
- API security testing

---

## 🔒 Security Best Practices

### Container Hardening
```yaml
# Dockerfile Security
FROM node:18-alpine AS base
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Use non-root user
USER nextjs

# Health check with security
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1
```

### Environment Security
```bash
# Secure environment variables
# Use secrets instead of env vars for sensitive data
environment:
  - NODE_ENV=production
  - LOG_LEVEL=info
  # Don't put secrets here!

secrets:
  - db_password
  - api_key
```

### Network Security
```yaml
# Network policies (Kubernetes)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS only
```

---

## 🚨 Security Incident Response

### Monitoring & Alerting
**Command**: `"Setup security incident detection and response"`

**AI will configure**:
- Real-time threat detection
- Automated incident response
- Security event correlation
- Alert escalation policies

### Backup & Recovery
**Command**: `"Implement secure backup and disaster recovery"`

**AI will setup**:
- Encrypted backup storage
- Point-in-time recovery
- Cross-region replication
- Recovery testing automation

---

## 🔗 Security Tools Integration

### Static Analysis
```markdown
"Integrate security static analysis tools (SonarQube, CodeQL, Semgrep)"
```

### Runtime Security
```markdown
"Setup runtime security monitoring (Falco, Sysdig, Aqua)"
```

### Compliance Automation
```markdown
"Automate compliance reporting and validation"
```

---

## 🎯 Security Validation Checklist

### ✅ Container Security
- [ ] Non-root user execution
- [ ] Read-only filesystem
- [ ] Capability dropping
- [ ] Security contexts configured
- [ ] Resource limits set

### ✅ Network Security
- [ ] Network segmentation implemented
- [ ] TLS encryption enforced
- [ ] Firewall rules configured
- [ ] VPN setup (if required)
- [ ] Network policies active

### ✅ Data Security
- [ ] Encryption at rest enabled
- [ ] Encryption in transit configured
- [ ] Secrets properly managed
- [ ] Backup encryption active
- [ ] Access logging enabled

### ✅ Access Control
- [ ] Authentication implemented
- [ ] Authorization policies configured
- [ ] RBAC roles defined
- [ ] API security enforced
- [ ] Audit trails active

---

## 🔗 Related Prompts

- **Docker-Compose Deployment**: `demeter/prompts/tools/docker-compose-deployment.md`
- **Kubernetes Deployment**: `demeter/prompts/tools/kubernetes-deployment.md`
- **Quality Verification**: `demeter/prompts/tools/quality-checks.md`

---

**🔒 Security First - Protect Your Deployment from Day One**

> *"Security is not optional - it's foundational"*