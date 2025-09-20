# ☸️ Kubernetes Deployment - Advanced Orchestration (Optional)

## 🎯 Purpose
Generate Kubernetes configurations for advanced orchestration needs when Docker-Compose is no longer sufficient. Use only when you need advanced features like auto-scaling, service mesh, or complex networking.

## ⚠️ When to Use Kubernetes
- **5+ interconnected services**
- **Auto-scaling requirements** based on metrics
- **Advanced deployment strategies** (blue-green, canary)
- **Service mesh networking** requirements
- **Complex CI/CD pipelines** with GitOps

## 🚀 Quick Commands

### Basic Migration from Docker-Compose
```markdown
"Convert my docker-compose.yml to Kubernetes manifests with deployments, services, and configmaps"
```

### Auto-scaling Setup
```markdown
"Create Kubernetes deployment with horizontal pod autoscaling based on CPU and memory"
```

### Advanced Networking
```markdown
"Generate Kubernetes manifests with service mesh, ingress controller, and network policies"
```

---

## 📋 Core Kubernetes Operations

### 1. Basic Deployment Conversion
**Command**: `"Convert docker-compose to Kubernetes"`

**AI will generate**:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8000
        resources:
          requests: {memory: 256Mi, cpu: 250m}
          limits: {memory: 512Mi, cpu: 500m}
        livenessProbe:
          httpGet: {path: /health, port: 8000}
          initialDelaySeconds: 30
        readinessProbe:
          httpGet: {path: /health, port: 8000}
          initialDelaySeconds: 5
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### 2. Auto-scaling Configuration
**Command**: `"Add horizontal pod autoscaling"`

**AI will create**:
```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 3. Ingress and Load Balancing
**Command**: `"Setup ingress controller with SSL termination"`

**AI will generate**:
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

---

## 🔧 Advanced Features

### Service Mesh Integration
**Command**: `"Setup Istio service mesh for my application"`

**AI will configure**:
- Service mesh sidecar injection
- Traffic management policies
- Security policies and mTLS
- Observability and tracing

### GitOps Deployment
**Command**: `"Create ArgoCD/Flux configuration for GitOps deployment"`

**AI will generate**:
- Application manifests for GitOps tools
- Automated sync policies
- Multi-environment promotion
- Rollback strategies

### Advanced Monitoring
**Command**: `"Setup comprehensive monitoring with Prometheus Operator"`

**AI will create**:
- Prometheus Operator configuration
- ServiceMonitor definitions
- Grafana dashboard provisioning
- AlertManager rules

---

## 📊 Deployment Strategies

### Blue-Green Deployment
```markdown
"Implement blue-green deployment strategy with traffic switching"
```

### Canary Deployment
```markdown
"Setup canary deployment with gradual traffic migration"
```

### Rolling Updates
```markdown
"Configure rolling updates with zero-downtime deployment"
```

---

## 🚀 Deployment Commands

### Apply Manifests
```bash
# Apply all manifests
kubectl apply -f k8s/

# Apply specific manifest
kubectl apply -f deployment.yaml

# Apply with dry-run
kubectl apply -f . --dry-run=client
```

### Monitoring and Debugging
```bash
# Check pod status
kubectl get pods -l app=myapp

# View logs
kubectl logs -f deployment/myapp

# Execute into pod
kubectl exec -it deployment/myapp -- /bin/sh

# Check resource usage
kubectl top pods
```

### Scaling Operations
```bash
# Manual scaling
kubectl scale deployment myapp --replicas=5

# Check HPA status
kubectl get hpa

# Check metrics
kubectl top nodes
```

---

## 🔍 Troubleshooting

### Pod Issues
```bash
# Check pod events
kubectl describe pod <pod-name>

# Check resource quotas
kubectl describe resourcequota

# Check node resources
kubectl describe nodes
```

### Network Issues
```bash
# Test service connectivity
kubectl run test --image=busybox -it --rm -- nslookup myapp-service

# Check ingress status
kubectl get ingress

# Test from within cluster
kubectl exec -it <pod-name> -- curl http://myapp-service
```

### Performance Issues
**Command**: `"Diagnose Kubernetes performance issues for my application"`

**AI will analyze**:
- Resource requests and limits
- Node capacity and allocation
- Network policies and latency
- Storage performance
- HPA configuration

---

## 🎯 Migration Path from Docker-Compose

### Phase 1: Basic Migration
1. Convert docker-compose services to Deployments
2. Create corresponding Services
3. Setup basic ConfigMaps and Secrets
4. Test functionality parity

### Phase 2: Add Kubernetes Features
1. Implement HPA for auto-scaling
2. Setup Ingress for external access
3. Add monitoring and logging
4. Configure security policies

### Phase 3: Advanced Operations
1. Implement advanced deployment strategies
2. Setup service mesh (if needed)
3. Configure GitOps workflows
4. Add comprehensive monitoring

---

## 🔗 Related Prompts

- **Docker-Compose Deployment**: `demeter/prompts/tools/docker-compose-deployment.md`
- **Security Configuration**: `demeter/prompts/tools/deployment-security.md`
- **Quality Verification**: `demeter/prompts/tools/quality-checks.md`

---

**☸️ Kubernetes - For When You Need Advanced Orchestration**

> *"Don't prematurely optimize - use Kubernetes when Docker-Compose isn't enough"*