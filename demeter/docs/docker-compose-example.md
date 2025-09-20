# 🐳 Docker-Compose First Deployment Example

## 📖 Overview

This example demonstrates the Demeter v1.1 approach to deployment using docker-compose as the primary deployment method. Kubernetes becomes optional for advanced use cases.

## 🚀 Production-Ready Docker-Compose Configuration

### Basic Application Setup

```yaml
# docker-compose.yml - Production Configuration
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    image: your-api:1.0.0
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - LOG_LEVEL=info
      - API_TITLE=Your API Name
      - API_VERSION=1.0.0
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    restart: unless-stopped
    networks:
      - app-network
    depends_on:
      database:
        condition: service_healthy

  database:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: your_app_db
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backup:/backup
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "app_user"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass $${REDIS_PASSWORD}
    environment:
      REDIS_PASSWORD_FILE: /run/secrets/redis_password
    secrets:
      - redis_password
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge

secrets:
  db_password:
    file: ./secrets/db_password.txt
  redis_password:
    file: ./secrets/redis_password.txt
```

## 📊 Optional Monitoring Stack

For projects requiring monitoring, add these services:

```yaml
# docker-compose.monitoring.yml - Optional Monitoring
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    restart: unless-stopped
    networks:
      - monitoring
    profiles:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD_FILE=/run/secrets/grafana_password
    secrets:
      - grafana_password
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards:ro
    restart: unless-stopped
    networks:
      - monitoring
    profiles:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge

secrets:
  grafana_password:
    file: ./secrets/grafana_password.txt
```

## 🚀 Deployment Commands

### Basic Deployment
```bash
# Start the application stack
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### With Monitoring
```bash
# Start application with monitoring
docker-compose --profile monitoring up -d

# Start only monitoring services
docker-compose --profile monitoring up -d prometheus grafana
```

### Production Deployment
```bash
# Build and deploy production version
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale application instances
docker-compose up -d --scale app=3

# Update deployment
docker-compose pull && docker-compose up -d
```

## 🔧 Configuration Files Structure

```
project-root/
├── docker-compose.yml              # Main application stack
├── docker-compose.monitoring.yml   # Optional monitoring
├── docker-compose.prod.yml         # Production overrides
├── Dockerfile                      # Application container
├── secrets/                        # Secret files
│   ├── db_password.txt
│   ├── redis_password.txt
│   └── grafana_password.txt
├── monitoring/                     # Monitoring configuration
│   ├── prometheus.yml
│   └── grafana/
│       └── dashboards/
└── backup/                         # Database backup location
```

## 🛡️ Security Best Practices

### Secret Management
- Use Docker secrets for sensitive data
- Never store passwords in environment variables
- Rotate secrets regularly
- Use secret files instead of environment variables

### Network Security
- Isolate services with custom networks
- Use internal networks for service communication
- Expose only necessary ports
- Implement proper firewall rules

### Container Security
- Use official, minimal base images
- Run containers as non-root users
- Keep images updated
- Scan for vulnerabilities

## 📈 Scaling and Performance

### Horizontal Scaling
```bash
# Scale application instances
docker-compose up -d --scale app=3

# Scale with load balancer
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d
```

### Resource Management
- Set appropriate resource limits and reservations
- Monitor resource usage with monitoring stack
- Optimize based on actual usage patterns
- Use health checks for reliable deployments

## 🔄 Advanced: Optional Kubernetes Migration

When docker-compose reaches its limits, migrate to Kubernetes:

```yaml
# kubernetes/deployment.yaml - Advanced orchestration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: your-app
  template:
    metadata:
      labels:
        app: your-app
    spec:
      containers:
      - name: app
        image: your-api:1.0.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## ✅ Benefits of Docker-Compose First Approach

### Simplicity
- Single file deployment configuration
- Easy local development and testing
- Straightforward CI/CD integration
- Minimal learning curve

### Production Ready
- Resource limits and health checks
- Secret management
- Network isolation
- Monitoring integration

### Gradual Scaling
- Start simple with docker-compose
- Add monitoring and advanced features as needed
- Migrate to Kubernetes when orchestration complexity requires it
- Maintain consistency across environments

---

**Framework**: Demeter WAVIS v1.1 | **Approach**: Docker-Compose First | **Status**: Production Ready