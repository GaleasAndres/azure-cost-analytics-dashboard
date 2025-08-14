# Deployment Guide

## 🚀 Deployment Overview

This guide covers the containerization strategy and multiple Azure hosting methods for deploying the Flask application. Each hosting strategy provides different benefits for learning Azure services and understanding deployment patterns.

## 🐳 Containerization Strategy

### Why Containers?

The Flask application is containerized to ensure:
- ✅ **Consistency** - Same runtime environment across dev/staging/prod
- ✅ **Portability** - Deploy to any container-capable service
- ✅ **Scalability** - Easy horizontal scaling
- ✅ **Isolation** - Dependencies packaged with application

### Docker Setup

#### Production Dockerfile
```dockerfile
# deployments/docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add Gunicorn for production
RUN pip install gunicorn

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
```

#### Development Dockerfile
```dockerfile
# deployments/docker/Dockerfile.dev
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Development server with auto-reload
CMD ["python", "app.py"]
```

### Application Modifications for Containers

#### Required Changes

1. **Add Health Endpoint** (`app.py`)
```python
@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

2. **Add Gunicorn to Requirements**
```text
# requirements.txt
flask
python-dotenv
msal
azure-mgmt-resource
azure-mgmt-costmanagement
gunicorn
```

3. **Container-friendly Host Binding**
```python
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

#### Why Gunicorn?

**Flask Development Server** vs **Gunicorn Production Server**:

| Flask `app.run()` | Gunicorn |
|-------------------|----------|
| ❌ Single-threaded | ✅ Multi-worker |
| ❌ Debug mode security issues | ✅ Production security |
| ❌ No process management | ✅ Automatic worker restarts |
| ❌ Poor performance under load | ✅ Handles concurrent requests |

**Real-world example**: 100 simultaneous users → Flask queues them sequentially, Gunicorn handles them concurrently with multiple workers.

## 🏗️ Hosting Strategies

### 1. Azure App Service (Recommended First)

**Best for**: Learning PaaS concepts, easy deployment, built-in features

#### Architecture
```
Internet → App Service → Container Registry → Application Insights
```

#### Features
- ✅ **Managed platform** - No server management
- ✅ **Built-in load balancing** - Handle traffic spikes
- ✅ **Deployment slots** - Blue-green deployments
- ✅ **Auto-scaling** - Scale based on metrics
- ✅ **SSL certificates** - Free managed SSL

#### Configuration Example
```bicep
resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: '${appName}-plan'
  location: location
  sku: {
    name: 'B1'  // Basic tier for development
  }
}

resource webApp 'Microsoft.Web/sites@2021-02-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'DOCKER|${containerRegistry}.azurecr.io/myapp:latest'
      appSettings: [
        {
          name: 'AZURE_CLIENT_ID'
          value: clientId
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
      ]
    }
  }
}
```

#### Deployment Process
1. Build container image
2. Push to Azure Container Registry
3. Deploy to App Service
4. Configure environment variables
5. Enable Application Insights

---

### 2. Azure Container Instances (ACI)

**Best for**: Learning serverless containers, simple workloads, cost optimization

#### Architecture
```
Internet → Load Balancer → Container Group → Application Insights
```

#### Features
- ✅ **Serverless containers** - Pay per second
- ✅ **Fast startup** - Containers start in seconds
- ✅ **No orchestration complexity** - Simple container deployment
- ✅ **Flexible networking** - Custom VNet integration
- ✅ **Cost-effective** - Pay only for running time

#### Configuration Example
```bicep
resource containerGroup 'Microsoft.ContainerInstance/containerGroups@2021-10-01' = {
  name: '${appName}-aci'
  location: location
  properties: {
    osType: 'Linux'
    restartPolicy: 'Always'
    containers: [
      {
        name: appName
        properties: {
          image: '${containerRegistry}.azurecr.io/myapp:latest'
          ports: [
            {
              port: 8000
              protocol: 'TCP'
            }
          ]
          environmentVariables: [
            {
              name: 'AZURE_CLIENT_ID'
              value: clientId
            }
          ]
          resources: {
            requests: {
              cpu: 1
              memoryInGB: 1
            }
          }
        }
      }
    ]
    ipAddress: {
      type: 'Public'
      ports: [
        {
          port: 80
          protocol: 'TCP'
        }
      ]
    }
  }
}
```

---

### 3. Azure Kubernetes Service (AKS)

**Best for**: Learning container orchestration, microservices, advanced scaling

#### Architecture
```
Internet → Ingress Controller → Service → Pods → Application Insights
```

#### Features
- ✅ **Container orchestration** - Manage multiple containers
- ✅ **Advanced scaling** - Horizontal Pod Autoscaler
- ✅ **Service mesh** - Advanced networking and security
- ✅ **Rolling deployments** - Zero-downtime updates
- ✅ **Resource management** - CPU/memory limits and requests

#### Deployment Manifests
```yaml
# deployments/kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: azure-cost-analytics
spec:
  replicas: 2
  selector:
    matchLabels:
      app: azure-cost-analytics
  template:
    metadata:
      labels:
        app: azure-cost-analytics
    spec:
      containers:
      - name: app
        image: myregistry.azurecr.io/myapp:latest
        ports:
        - containerPort: 8000
        env:
        - name: AZURE_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: azure-secrets
              key: client-id
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
```

```yaml
# deployments/kubernetes/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: azure-cost-analytics-service
spec:
  selector:
    app: azure-cost-analytics
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### Helm Chart Structure
```
deployments/helm/azure-cost-analytics/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default values
├── values-dev.yaml         # Development overrides
├── values-prod.yaml        # Production overrides
└── templates/
    ├── deployment.yaml     # Deployment template
    ├── service.yaml        # Service template
    ├── ingress.yaml        # Ingress template
    └── secrets.yaml        # Secret template
```

---

### 4. Azure Container Apps

**Best for**: Learning serverless orchestration, event-driven scaling, modern cloud-native patterns

#### Architecture
```
Internet → Container App Environment → Revisions → Application Insights
```

#### Features
- ✅ **Serverless Kubernetes** - Managed container orchestration
- ✅ **Event-driven scaling** - Scale to zero when idle
- ✅ **Built-in ingress** - No need for separate load balancer
- ✅ **Dapr integration** - Microservices patterns
- ✅ **Revision management** - Built-in blue-green deployments

#### Configuration Example
```bicep
resource containerApp 'Microsoft.App/containerApps@2022-03-01' = {
  name: '${appName}-containerapp'
  location: location
  properties: {
    managedEnvironmentId: containerEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
      }
      registries: [
        {
          server: '${containerRegistry}.azurecr.io'
          username: containerRegistryUsername
          passwordSecretRef: 'registry-password'
        }
      ]
      secrets: [
        {
          name: 'registry-password'
          value: containerRegistryPassword
        }
      ]
    }
    template: {
      containers: [
        {
          name: appName
          image: '${containerRegistry}.azurecr.io/myapp:latest'
          env: [
            {
              name: 'AZURE_CLIENT_ID'
              value: clientId
            }
          ]
          resources: {
            cpu: '0.5'
            memory: '1Gi'
          }
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 10
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '50'
              }
            }
          }
        ]
      }
    }
  }
}
```

## 🔄 Deployment Workflow

### 1. Build and Test Locally
```bash
# Build Docker image
docker build -f deployments/docker/Dockerfile -t myapp:latest .

# Run locally
docker run -p 8000:8000 --env-file .env myapp:latest

# Test health endpoint
curl http://localhost:8000/health
```

### 2. Push to Container Registry
```bash
# Login to ACR
az acr login --name myregistry

# Tag image
docker tag myapp:latest myregistry.azurecr.io/myapp:latest

# Push image
docker push myregistry.azurecr.io/myapp:latest
```

### 3. Deploy to Target Service
```bash
# App Service
az webapp config container set \
  --name myapp \
  --resource-group myapp-rg \
  --docker-custom-image-name myregistry.azurecr.io/myapp:latest

# AKS
kubectl apply -f deployments/kubernetes/

# Container Apps
az containerapp update \
  --name myapp-containerapp \
  --resource-group myapp-rg \
  --image myregistry.azurecr.io/myapp:latest
```

## 🔍 Monitoring and Health Checks

### Health Endpoint Implementation
```python
@app.route('/health')
def health():
    try:
        # Check dependencies (database, external APIs)
        # For this app, verify Azure connection
        
        return {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'dependencies': {
                'azure_auth': 'ok',
                'flask': 'ok'
            }
        }, 200
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }, 503
```

### Application Insights Integration
```python
from applicationinsights import TelemetryClient

# Initialize telemetry
tc = TelemetryClient(os.environ.get('APPINSIGHTS_INSTRUMENTATIONKEY'))

# Track custom metrics
tc.track_metric('cost_api_requests', 1)
tc.track_event('user_login', {'subscription_count': len(subscriptions)})
```

## 🚦 Deployment Strategy Comparison

| Aspect | App Service | ACI | AKS | Container Apps |
|--------|-------------|-----|-----|----------------|
| **Complexity** | Low | Low | High | Medium |
| **Learning Value** | PaaS concepts | Serverless containers | Orchestration | Modern serverless |
| **Cost (Dev)** | $13/month | $10/month | $73/month | $5/month |
| **Scaling** | Vertical/Horizontal | Manual | Advanced | Event-driven |
| **Management** | Managed | Serverless | Self-managed | Managed |
| **Best For** | Web apps | Simple containers | Microservices | Event-driven apps |

## 🎯 Recommended Learning Path

1. **Start with App Service** - Learn PaaS deployment patterns
2. **Try Container Instances** - Understand serverless containers
3. **Explore Container Apps** - Modern cloud-native patterns
4. **Master AKS** - Advanced orchestration (optional for cost)

This progression builds from simple to complex while teaching different Azure deployment paradigms.

---

*This deployment guide provides practical knowledge of containerization and multiple Azure hosting strategies for real-world DevOps scenarios.*