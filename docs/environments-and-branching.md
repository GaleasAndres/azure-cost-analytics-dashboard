# Environments and Branching Strategy

## 🌍 Environment Strategy Overview

This project uses a **cost-optimized two-environment approach** that balances learning opportunities with budget constraints while following enterprise DevOps best practices.

## 🏗️ Environment Architecture

### Development Environment (Learning Focus)
```
DEV Environment - Multiple Hosting Methods
├── myapp-dev-shared-rg           # Shared resources
│   ├── Azure Container Registry  # Store all container images
│   ├── Key Vault                # Store secrets and certificates  
│   └── Log Analytics Workspace  # Centralized logging
│
├── myapp-dev-appservice-rg      # App Service deployment
│   ├── App Service Plan (B1)    # Basic tier for development
│   ├── Web App                  # PaaS hosting
│   └── Application Insights     # Monitoring
│
├── myapp-dev-aci-rg             # Container Instances deployment  
│   ├── Container Group          # Serverless containers
│   └── Application Insights     # Monitoring
│
├── myapp-dev-aks-rg             # Kubernetes deployment
│   ├── AKS Cluster (2 nodes)    # Container orchestration
│   ├── Load Balancer            # Traffic distribution
│   └── Application Insights     # Monitoring
│
└── myapp-dev-containerapp-rg    # Container Apps deployment
    ├── Container App Environment # Managed Kubernetes
    ├── Container App            # Serverless orchestration
    └── Application Insights     # Monitoring
```

**Purpose**: 
- Test all hosting strategies
- Compare performance and costs
- Learn different Azure services
- Validate deployments before production

### Production Environment (Cost-Optimized)
```
PROD Environment - Single Optimized Method  
├── myapp-prod-shared-rg         # Shared resources
│   ├── Azure Container Registry  # Production image storage
│   ├── Key Vault                # Production secrets
│   └── Log Analytics Workspace  # Production logging
│
└── myapp-prod-appservice-rg     # App Service only
    ├── App Service Plan (P1V2)   # Premium tier for production
    ├── Web App                  # Production hosting
    ├── Application Insights     # Production monitoring
    └── Deployment Slots         # Blue-green deployments
```

**Purpose**:
- Cost-effective production hosting
- Single, well-tested deployment method
- Production-grade performance and reliability

## 🌿 Branching Strategy

### Branch Structure
```
main branch                    # Production deployments only
├── Deploys to: PROD (App Service only)
├── Requires: Pull request + approvals
└── Protected: Direct pushes disabled

feature/* branches             # Development and testing
├── Deploys to: ALL dev hosting methods
├── Testing: App Service, ACI, AKS, Container Apps
├── Validation: Choose best performer for production
└── Merge: Creates production deployment
```

### Workflow Examples

#### Feature Development Flow
```
1. Developer creates: feature/cost-alerts-dashboard
   ├── Automatic deployment to DEV environment
   ├── Tests on App Service, ACI, AKS, Container Apps
   ├── Compares performance, costs, and reliability
   └── Validates feature works across all methods

2. Code Review & Testing
   ├── Pull request created to main
   ├── Team reviews code and deployment results
   ├── Choose optimal hosting method for production
   └── Approve merge

3. Production Deployment
   ├── Merge to main branch
   ├── Automatic deployment to PROD (App Service)
   ├── Blue-green deployment with zero downtime
   └── Production monitoring and validation
```

## 🚀 CI/CD Pipeline Logic

### Branch-Based Deployment Logic
```yaml
# Simplified pipeline logic
if branch_name.startswith('feature/'):
    deploy_to_all_dev_environments()
    run_comprehensive_testing()
    generate_performance_comparison()
    
elif branch_name == 'main':
    deploy_to_production_app_service()
    run_production_health_checks()
    notify_team_of_deployment()
```

### Feature Branch Pipeline
```yaml
name: Feature Branch CI/CD
on:
  push:
    branches: ['feature/*']

jobs:
  deploy-dev-environments:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        hosting: [app-service, aci, aks, container-apps]
    steps:
    - name: Deploy to ${{ matrix.hosting }}
      run: |
        az deployment group create \
          --resource-group myapp-dev-${{ matrix.hosting }}-rg \
          --template-file infrastructure/bicep/${{ matrix.hosting }}/main.bicep
        
    - name: Run Health Tests
      run: |
        python tests/health_check.py --environment dev --hosting ${{ matrix.hosting }}
        
    - name: Generate Cost Report
      run: |
        python scripts/cost_analysis.py --environment dev --hosting ${{ matrix.hosting }}
```

### Production Branch Pipeline
```yaml
name: Production Deployment
on:
  push:
    branches: ['main']

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval
    steps:
    - name: Deploy to Production App Service
      run: |
        az deployment group create \
          --resource-group myapp-prod-appservice-rg \
          --template-file infrastructure/bicep/app-service/main.bicep \
          --parameters @infrastructure/bicep/environments/production/parameters.prod.json
        
    - name: Blue-Green Deployment
      run: |
        az webapp deployment slot swap \
          --name myapp-prod-app \
          --resource-group myapp-prod-appservice-rg \
          --slot staging
          
    - name: Production Health Check
      run: |
        python tests/production_health_check.py
        python tests/load_test.py
```

## 🔄 Development Workflow

### 1. Feature Development
```bash
# Create and switch to feature branch
git checkout -b feature/new-dashboard-charts

# Make changes to application and infrastructure
# ... development work ...

# Commit changes
git add .
git commit -m "Add new dashboard charts with improved visualizations"

# Push to trigger dev deployments
git push origin feature/new-dashboard-charts
```

**Result**: Automatic deployment to all 4 dev hosting methods

### 2. Testing and Validation
```bash
# Access deployed environments for testing
Dev App Service: https://myapp-dev-appservice.azurewebsites.net
Dev ACI:         http://myapp-dev-aci.eastus.azurecontainer.io
Dev AKS:         http://myapp-dev-aks-cluster-ip/
Dev Container App: https://myapp-dev-containerapp.azurecontainerapps.io

# Run automated tests
python tests/integration_tests.py --all-environments
python tests/performance_tests.py --all-environments
python scripts/cost_comparison.py --all-environments
```

### 3. Performance Comparison
```bash
# Generated automatically by pipeline
Environment Performance Report:
├── App Service:    Response time: 245ms, Uptime: 99.9%
├── ACI:           Response time: 189ms, Uptime: 99.7%
├── AKS:           Response time: 201ms, Uptime: 99.8%
└── Container Apps: Response time: 156ms, Uptime: 99.9%

Cost Analysis (Monthly):
├── App Service:    $13.00
├── ACI:           $8.50
├── AKS:           $73.00
└── Container Apps: $5.20

Recommendation: Container Apps (best performance + lowest cost)
```

### 4. Production Deployment
```bash
# Create pull request
gh pr create --title "Add new dashboard charts" --body "Performance tested across all hosting methods"

# Team review and approval
# ... code review process ...

# Merge to main
git checkout main
git merge feature/new-dashboard-charts
git push origin main
```

**Result**: Automatic deployment to production App Service with blue-green deployment

## 🛡️ Environment Protection Rules

### Development Environment
- ✅ **Auto-deploy** from feature branches
- ✅ **No approval required** for faster iteration
- ✅ **Resource cleanup** after branch deletion
- ✅ **Cost monitoring** with automatic alerts

### Production Environment
- 🔒 **Manual approval required** for all deployments
- 🔒 **Pull request required** - no direct pushes
- 🔒 **Status checks required** - all tests must pass
- 🔒 **Blue-green deployment** for zero downtime
- 🔒 **Automated rollback** on health check failure

## 📊 Cost Management Strategy

### Development Cost Controls
```bash
# Automatic cleanup after branch deletion
on:
  delete:
    branches: ['feature/*']
    
jobs:
  cleanup-dev-resources:
    runs-on: ubuntu-latest
    steps:
    - name: Delete Feature Environment Resources
      run: |
        branch_name=$(echo ${{ github.event.ref }} | sed 's/refs\/heads\///')
        feature_suffix=$(echo $branch_name | sed 's/feature\///')
        
        # Delete all resource groups for this feature
        az group delete --name myapp-dev-$feature_suffix-appservice-rg --yes --no-wait
        az group delete --name myapp-dev-$feature_suffix-aci-rg --yes --no-wait
        az group delete --name myapp-dev-$feature_suffix-aks-rg --yes --no-wait
        az group delete --name myapp-dev-$feature_suffix-containerapp-rg --yes --no-wait
```

### Monthly Cost Estimates
```
Development Environment (All Methods):
├── App Service (B1):      $13/month
├── ACI (1 CPU, 1GB):      $8/month  
├── AKS (2 B2s nodes):     $73/month
├── Container Apps:        $5/month
├── Shared Resources:      $15/month
└── Total DEV:            $114/month

Production Environment:
├── App Service (P1V2):    $146/month
├── Shared Resources:      $25/month
└── Total PROD:           $171/month

Project Total:             $285/month
```

## 🎯 Learning Benefits

### Skills Developed
1. **Multi-environment management** - Different configs for dev/prod
2. **Cost optimization** - Balance learning with budget constraints  
3. **Deployment strategies** - Blue-green, canary, rolling deployments
4. **Performance comparison** - Real-world hosting method evaluation
5. **Infrastructure automation** - Bicep templates for consistent deployments

### Real-World Practices
- **Feature branch testing** - Validate before production
- **Environment parity** - Similar configs across environments
- **Automated deployments** - Reduce human error and deployment time
- **Cost monitoring** - Track and optimize cloud spending
- **Performance testing** - Compare hosting methods objectively

## 🚦 Deployment Gates and Approvals

### Automated Gates (All Environments)
- ✅ **Bicep validation** - Template syntax and logic
- ✅ **Container security scan** - Vulnerability assessment  
- ✅ **Health check tests** - Application functionality
- ✅ **Performance baseline** - Response time thresholds

### Manual Gates (Production Only)
- 🔍 **Code review approval** - Team member verification
- 🔍 **Architecture review** - For significant changes
- 🔍 **Security review** - For authentication or data changes
- 🔍 **Performance validation** - Dev environment results review

---

*This environment and branching strategy provides a foundation for learning DevOps practices while maintaining cost efficiency and production reliability.*