# 🐳 Docker-Compose Deployment - AI-Driven Production Setup

## 🎯 Purpose
Generate production-ready Docker-Compose configurations as the primary deployment method for Demeter v1.1 projects. Focus on simplicity, security, and production readiness.

## 🚀 Quick Commands

### Basic Deployment
```markdown
"Generate a production-ready docker-compose.yml for my [technology stack] application with health checks and resource limits"
```

### With Monitoring
```markdown
"Create docker-compose configuration with Prometheus and Grafana monitoring for my application"
```

### Multi-Service Setup
```markdown
"Generate docker-compose configuration for my application with PostgreSQL database and Redis cache"
```

---

## 📋 Core Operations

### 1. Basic Production Configuration
**Quick Command**: `"Generate basic docker-compose production setup"`

**AI will create**:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    deploy:
      resources:
        limits: {memory: 512M, cpus: '0.5'}
        reservations: {memory: 256M, cpus: '0.25'}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    user: "1000:1000"
```

### 2. Multi-Service Configuration
**Quick Command**: `"Generate docker-compose with database and cache"`

**AI will create**:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/dbname
      - REDIS_URL=redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 30s
    secrets:
      - db_password
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### 3. Monitoring Stack Integration
**Quick Command**: `"Add monitoring stack with Prometheus and Grafana"`

**AI will add**:
```yaml
  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
    environment:
      - GF_SECURITY_ADMIN_PASSWORD_FILE=/run/secrets/grafana_password
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
    secrets:
      - grafana_password
    restart: unless-stopped
```

---

## 🔧 Production Optimizations

### Security Hardening
**Command**: `"Apply security best practices to docker-compose configuration"`

**AI will implement**:
- Non-root user execution
- Secret management for passwords
- Network isolation
- Resource limits
- Health check implementation
- Security context configuration

### Performance Tuning
**Command**: `"Optimize docker-compose for [expected load/traffic pattern]"`

**AI will optimize**:
- Resource allocation based on load
- Connection pool sizing
- Cache configuration
- Volume mount optimization
- Network configuration

### Environment Management
**Command**: `"Create docker-compose files for development, staging, and production"`

**AI will generate**:
- `docker-compose.yml` (base configuration)
- `docker-compose.dev.yml` (development overrides)
- `docker-compose.staging.yml` (staging overrides)
- `docker-compose.prod.yml` (production overrides)

---

## 📊 Common Deployment Patterns

### Pattern 1: Simple API
```bash
# Use for: Hello World, simple REST APIs
# Services: app only
# Resources: 256MB memory, 0.25 CPU
# Features: health checks, auto-restart
```

### Pattern 2: API with Database
```bash
# Use for: Standard web applications
# Services: app + postgres/mysql
# Resources: 512MB memory, 0.5 CPU
# Features: secrets, persistent volumes, health checks
```

### Pattern 3: Full Stack with Monitoring
```bash
# Use for: Production applications
# Services: app + database + cache + monitoring
# Resources: Scaled based on requirements
# Features: comprehensive monitoring, alerting, logging
```

---

## 🚀 Deployment Commands

### Development
```bash
# Hot reload for development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Development with logs
docker-compose -f docker-compose.dev.yml up --build
```

### Production
```bash
# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale app=3

# Update and restart
docker-compose pull && docker-compose up -d
```

### Monitoring
```bash
# View service status
docker-compose ps

# View logs
docker-compose logs -f app

# Check health
curl http://localhost:8000/health
```

---

## 🔍 Troubleshooting

### Common Issues
```bash
# Port conflicts
docker-compose down
lsof -i :8000  # Find what's using the port

# Resource issues
docker system prune -f  # Clean up resources
docker-compose down && docker-compose up -d

# Health check failures
docker-compose logs app  # Check application logs
docker-compose exec app curl localhost:8000/health
```

### Performance Issues
**Command**: `"Diagnose performance issues in my docker-compose setup"`

**AI will check**:
- Container resource usage
- Network latency between services
- Volume mount performance
- Health check intervals
- Connection pool settings

---

## 🎯 Best Practices

### ✅ Do
- Use health checks for all services
- Set resource limits and reservations
- Use secrets for sensitive data
- Implement proper logging
- Use non-root users
- Set restart policies

### ❌ Don't
- Expose unnecessary ports
- Use latest tags in production
- Store secrets in environment variables
- Run containers as root
- Skip health checks
- Ignore resource limits

---

## 🔗 Related Prompts

- **Security Configuration**: `demeter/prompts/tools/deployment-security.md`
- **Kubernetes Migration**: `demeter/prompts/tools/kubernetes-deployment.md`
- **Quality Verification**: `demeter/prompts/tools/quality-checks.md`

---

**🌾 Docker-Compose First - Simple, Secure, Production-Ready**

> *"Start simple with Docker-Compose, scale when needed"*