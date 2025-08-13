an R`

## Project Overview

### Learning Objectives
- Master Infrastructure as Code (Bicep) for Azure and Az-104 certification prep
- Implement GitFlow with multi-environment CI/CD pipelines
- Practice Azure CLI and Azure PowerShell automation
- Explore multiple Azure hosting strategies (App Service, ACI, AKS, Container Apps)
- Build production-ready monitoring and logging
- Learn Azure cost optimization strategies

### Application Architecture
- **Backend**: Flask Python application with Azure SDK integration
- **Authentication**: Azure AD OAuth 2.0 via MSAL
- **APIs**: Azure Cost Management API, Resource Management API
- **Frontend**: Vanilla JavaScript SPA
- **Deployment**: Containerized with Docker

## Branching & Environment Strategy

### Git Branching Model
```
main (production)
├── develop (integration)
├── feature/new-dashboard-charts
├── feature/cost-alerts
├── hotfix/auth-token-refresh
└── release/v1.2.0
```

### Environment Mapping
| Branch | Environment | Auto Deploy | Approval Required |
|--------|-------------|-------------|-------------------|
| `feature/*` | Feature environments (temporary) | ✅ | ❌ |
| `develop` | Development | ✅ | ❌ |
| `release/*` | Staging | ✅ | ✅ Manual |
| `main` | Production | ✅ | ✅ Manual + Gates |

### Environment Lifecycle
1. **Feature Environment**: Created on feature branch push, destroyed on branch deletion
2. **Development**: Persistent environment for integration testing
3. **Staging**: Production-like environment for final testing
4. **Production**: Live environment with blue-green deployment

## Phase 1: Foundation Setup (Week 1)

### ✅ Project Structure & Health Endpoint
- [ ] Create health endpoint (`/health`) for monitoring
- [ ] Implement structured logging with Python logging module
- [ ] Create Dockerfile with Gunicorn production server
- [ ] Setup environment-specific configuration files

### ✅ Infrastructure as Code Foundation
- [ ] Bicep development environment setup with Azure CLI
- [ ] Create Bicep modules for reusable components
- [ ] Implement multi-environment parameter management
- [ ] Setup Azure service principals for automation

### ✅ Development Environment
- [ ] Create development resource group via Bicep
- [ ] Deploy basic App Service for initial testing
- [ ] Setup Application Insights for monitoring
- [ ] Configure Azure Container Registry

## Phase 2: CI/CD Pipeline Implementation (Week 2)

### ✅ GitHub Actions Setup (Recommended)
- [ ] Configure GitHub repository secrets for Azure authentication
- [ ] Setup environment protection rules for staging/production
- [ ] Configure branch protection rules and pull request requirements
- [ ] Create reusable workflow templates

### ✅ Linux-based Pipeline (Primary)
```yaml
# Workflow: .github/workflows/ci-cd-linux.yml
name: CI/CD Pipeline (Linux)
on:
  push:
    branches: [main, develop, feature/*, release/*]
  pull_request:
    branches: [main, develop]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Azure CLI Deployment
      uses: azure/CLI@v1
```

### ✅ Windows-based Pipeline (Learning)
```yaml
# Workflow: .github/workflows/ci-cd-windows.yml
# Same logic but using Azure PowerShell instead of Azure CLI
name: CI/CD Pipeline (Windows)
on:
  push:
    branches: [main, develop]

jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v4
    - name: Azure PowerShell Deployment
      uses: azure/powershell@v1
```

### ✅ Pipeline Features
- [ ] Automated testing (unit tests, security scans)
- [ ] Docker image building and pushing to ACR
- [ ] Bicep validation and deployment automation
- [ ] Environment-specific deployments
- [ ] Rollback capabilities

## Phase 3: Multiple Deployment Strategies (Week 3-4)

### ✅ Strategy 1: Azure App Service
**Learning Focus**: PaaS, scaling, deployment slots
- [ ] Bicep module for App Service deployment
- [ ] Blue-green deployment with slots
- [ ] Auto-scaling configuration
- [ ] Custom domain and SSL setup

### ✅ Strategy 2: Azure Container Instances
**Learning Focus**: Serverless containers, networking
- [ ] ACI deployment with Bicep
- [ ] Container group networking
- [ ] Persistent volume mounting
- [ ] Cost comparison with App Service

### ✅ Strategy 3: Azure Kubernetes Service
**Learning Focus**: Orchestration, service mesh, advanced scaling
- [ ] AKS cluster provisioning with Bicep
- [ ] Kubernetes manifests and Helm charts
- [ ] Ingress controller setup (NGINX/Application Gateway)
- [ ] Horizontal Pod Autoscaler configuration
- [ ] Azure Container Insights integration

### ✅ Strategy 4: Azure Container Apps
**Learning Focus**: Event-driven scaling, serverless patterns
- [ ] Container Apps environment setup
- [ ] KEDA-based scaling configuration
- [ ] Dapr integration exploration
- [ ] Managed identity authentication

## Phase 4: Production Readiness (Week 5)

### ✅ Security Implementation
- [ ] Azure Key Vault integration for secrets
- [ ] Managed Identity authentication for Azure APIs
- [ ] Container image security scanning
- [ ] Network security groups and private endpoints
- [ ] Azure Policy compliance

### ✅ Monitoring & Observability
- [ ] Application Insights custom telemetry
- [ ] Log Analytics workbooks and dashboards
- [ ] Azure Monitor alerts and action groups
- [ ] Performance monitoring and APM
- [ ] Cost monitoring and budgets

### ✅ Disaster Recovery & Backup
- [ ] Multi-region deployment strategy
- [ ] Automated backup procedures
- [ ] Recovery time objective (RTO) planning
- [ ] Infrastructure drift detection

## Project Folder Structure

```
azure-cost-analytics-dashboard/
├── README.md
├── DEVOPS-PLAN.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── app.py
├── config.py
│
├── backend/                           # Application code
│   ├── __init__.py
│   ├── api/
│   ├── auth/
│   ├── azure/
│   ├── models/
│   ├── tests/
│   └── utils/
│
├── frontend/                          # Frontend assets
│   ├── index.html
│   ├── app.js
│   └── styles.css
│
├── .github/                           # GitHub Actions & workflows
│   ├── workflows/
│   │   ├── ci-cd-linux.yml           # Main Linux-based pipeline
│   │   ├── ci-cd-windows.yml         # Windows-based pipeline (learning)
│   │   ├── infrastructure.yml         # Infrastructure-only deployment
│   │   ├── feature-environment.yml   # Temporary feature environments
│   │   └── cleanup.yml               # Resource cleanup automation
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── infrastructure/                    # Infrastructure as Code
│   ├── bicep/                        # Bicep Infrastructure as Code
│   │   ├── modules/                   # Reusable Bicep modules
│   │   │   ├── app-service/
│   │   │   │   ├── main.bicep
│   │   │   │   ├── parameters.json
│   │   │   │   └── outputs.bicep
│   │   │   ├── container-registry/
│   │   │   │   ├── main.bicep
│   │   │   │   └── parameters.json
│   │   │   ├── monitoring/
│   │   │   │   ├── main.bicep
│   │   │   │   └── parameters.json
│   │   │   ├── networking/
│   │   │   │   ├── main.bicep
│   │   │   │   └── parameters.json
│   │   │   └── storage/
│   │   │       ├── main.bicep
│   │   │       └── parameters.json
│   │   ├── environments/              # Environment-specific deployments
│   │   │   ├── development/
│   │   │   │   ├── main.bicep
│   │   │   │   ├── parameters.dev.json
│   │   │   │   └── deploy.sh
│   │   │   ├── staging/
│   │   │   │   ├── main.bicep
│   │   │   │   ├── parameters.staging.json
│   │   │   │   └── deploy.sh
│   │   │   └── production/
│   │   │       ├── main.bicep
│   │   │       ├── parameters.prod.json
│   │   │       └── deploy.sh
│   │   └── shared/                    # Shared configurations
│   │       ├── resource-naming.bicep
│   │       ├── common-tags.bicep
│   │       └── variables.bicep
│   │
│   └── scripts/                      # Helper scripts
│       ├── setup-azure-cli.sh        # Azure CLI and Bicep setup
│       ├── deploy-all-envs.sh        # Multi-environment deployment
│       ├── validate-bicep.sh         # Bicep template validation
│       └── cleanup.sh                # Resource cleanup
│
├── deployments/                      # Deployment configurations
│   ├── docker/
│   │   ├── Dockerfile                # Production Dockerfile
│   │   ├── Dockerfile.dev            # Development Dockerfile
│   │   ├── docker-compose.yml        # Local development
│   │   └── .dockerignore
│   │
│   ├── kubernetes/                   # AKS deployment manifests
│   │   ├── namespaces/
│   │   ├── deployments/
│   │   ├── services/
│   │   ├── ingress/
│   │   └── monitoring/
│   │
│   ├── helm/                         # Helm charts for AKS
│   │   ├── azure-cost-analytics/
│   │   │   ├── Chart.yaml
│   │   │   ├── values.yaml
│   │   │   ├── values-dev.yaml
│   │   │   ├── values-staging.yaml
│   │   │   ├── values-prod.yaml
│   │   │   └── templates/
│   │   └── README.md
│   │
│   └── container-apps/               # Azure Container Apps configs
│       ├── environment.yaml
│       ├── application.yaml
│       └── scaling-rules.yaml
│
├── environments/                     # Environment-specific configurations
│   ├── development/
│   │   ├── app.env
│   │   └── secrets.example
│   ├── staging/
│   │   ├── app.env
│   │   └── secrets.example
│   └── production/
│       ├── app.env
│       └── secrets.example
│
├── monitoring/                       # Monitoring and observability
│   ├── dashboards/
│   │   ├── application-insights.json
│   │   ├── cost-monitoring.json
│   │   └── infrastructure.json
│   ├── alerts/
│   │   ├── application-alerts.json
│   │   ├── cost-alerts.json
│   │   └── infrastructure-alerts.json
│   └── workbooks/
│       ├── performance-analysis.json
│       └── cost-optimization.json
│
├── docs/                            # Documentation
│   ├── deployment-guides/
│   │   ├── app-service.md
│   │   ├── container-instances.md
│   │   ├── kubernetes.md
│   │   └── container-apps.md
│   ├── architecture/
│   │   ├── system-design.md
│   │   ├── security-model.md
│   │   └── diagrams/
│   ├── runbooks/
│   │   ├── incident-response.md
│   │   ├── deployment-rollback.md
│   │   └── troubleshooting.md
│   └── learning-notes/
│       ├── terraform-lessons.md
│       ├── kubernetes-lessons.md
│       └── azure-gotchas.md
│
└── tests/                           # Testing
    ├── unit/
    ├── integration/
    ├── e2e/
    └── load/
```

## Infrastructure Components

### Core Resources (Per Environment)
```bicep
// Bicep resources for each environment
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01'
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-09-01'
resource servicePlan 'Microsoft.Web/serverfarms@2021-02-01'
resource webApp 'Microsoft.Web/sites@2021-02-01'
resource applicationInsights 'Microsoft.Insights/components@2020-02-02'
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2021-06-01'
resource keyVault 'Microsoft.KeyVault/vaults@2021-10-01'
```

### Environment-Specific Sizing
| Component | Development | Staging | Production |
|-----------|-------------|---------|------------|
| App Service Plan | B1 (Basic) | S1 (Standard) | P1V2 (Premium) |
| Container Registry | Basic | Standard | Premium |
| Log Analytics | Pay-as-you-go | Pay-as-you-go | Commitment Tier |
| Key Vault | Standard | Standard | Premium |

## Cost Estimation

### Monthly Cost Breakdown (USD)
| Environment | App Service | Container Registry | Monitoring | Storage | Total |
|-------------|-------------|-------------------|------------|---------|-------|
| **Development** | $13 (B1) | $5 (Basic) | $3 | $2 | **~$23** |
| **Staging** | $56 (S1) | $20 (Standard) | $5 | $3 | **~$84** |
| **Production** | $146 (P1V2) | $20 (Standard) | $10 | $5 | **~$181** |
| **AKS (Learning)** | $73 (2 nodes) | $20 | $15 | $5 | **~$113** |

### **Total Estimated Monthly Cost: $288-401**

### Cost Optimization Strategies
- [ ] Use Azure Dev/Test pricing for non-production
- [ ] Implement auto-shutdown for development environments
- [ ] Use Azure Reservations for production workloads
- [ ] Monitor and alert on cost thresholds
- [ ] Regular resource cleanup automation

## Learning Checkpoints

### Week 1 Checkpoint
**Skills Acquired:**
- [ ] Bicep template development and modularization
- [ ] Azure CLI automation and Bicep deployment commands
- [ ] Container orchestration basics
- [ ] Infrastructure parameter management

**Challenges to Document:**
- [ ] Bicep template validation and debugging
- [ ] Environment parameter management
- [ ] Container registry authentication

### Week 2 Checkpoint
**Skills Acquired:**
- [ ] Azure DevOps pipeline authoring
- [ ] Multi-environment deployment patterns
- [ ] Automated testing integration
- [ ] Secret management best practices

### Week 3-4 Checkpoint
**Skills Acquired:**
- [ ] Kubernetes cluster management
- [ ] Container networking concepts
- [ ] Service discovery and load balancing
- [ ] Performance monitoring and alerting

### Final Checkpoint
**Skills Acquired:**
- [ ] Production operations with Bicep-deployed infrastructure
- [ ] Disaster recovery planning
- [ ] Cost optimization techniques
- [ ] Security compliance implementation
- [ ] Bicep best practices and advanced features

## CLI Commands Reference

### Essential Azure CLI Commands
```bash
# Resource Group Management
az group create --name myapp-dev-rg --location eastus
az group delete --name myapp-dev-rg --yes --no-wait

# Bicep Deployment Commands
az deployment group create --resource-group myapp-dev-rg --template-file main.bicep --parameters @parameters.dev.json
az deployment group validate --resource-group myapp-dev-rg --template-file main.bicep --parameters @parameters.dev.json
az deployment group what-if --resource-group myapp-dev-rg --template-file main.bicep --parameters @parameters.dev.json

# Container Registry
az acr create --resource-group myapp-dev-rg --name myappdevcr --sku Basic
az acr build --registry myappdevcr --image myapp:latest .

# App Service
az webapp create --resource-group myapp-dev-rg --plan myplan --name myapp-dev
az webapp deployment source config --name myapp-dev --resource-group myapp-dev-rg --repo-url https://github.com/user/repo

# AKS Commands
az aks create --resource-group myapp-dev-rg --name myapp-aks --node-count 2
az aks get-credentials --resource-group myapp-dev-rg --name myapp-aks
```

### Essential PowerShell Commands
```powershell
# Resource Group Management
New-AzResourceGroup -Name "myapp-dev-rg" -Location "East US"
Remove-AzResourceGroup -Name "myapp-dev-rg" -Force

# Bicep Deployment Commands
New-AzResourceGroupDeployment -ResourceGroupName "myapp-dev-rg" -TemplateFile "main.bicep" -TemplateParameterFile "parameters.dev.json"
Test-AzResourceGroupDeployment -ResourceGroupName "myapp-dev-rg" -TemplateFile "main.bicep" -TemplateParameterFile "parameters.dev.json"

# Container Registry
New-AzContainerRegistry -ResourceGroupName "myapp-dev-rg" -Name "myappdevcr" -Sku "Basic"

# App Service
New-AzWebApp -ResourceGroupName "myapp-dev-rg" -Name "myapp-dev" -AppServicePlan "myplan"
```

## Success Criteria

### Technical Milestones
- [ ] Application deployable to 4 different Azure services
- [ ] Fully automated CI/CD with multi-environment promotion
- [ ] Production-ready monitoring and alerting
- [ ] Infrastructure 100% defined as code
- [ ] Zero-downtime deployment capability

### Learning Outcomes
- [ ] Proficiency in Bicep for Azure infrastructure management
- [ ] Understanding of Kubernetes fundamentals
- [ ] CI/CD pipeline design and implementation
- [ ] Azure cost optimization strategies
- [ ] Production operations best practices
- [ ] Az-104 certification readiness

## Next Steps & Advanced Topics

### Future Enhancements
- [ ] Implement Azure Front Door for global load balancing
- [ ] Add Azure API Management for API governance
- [ ] Explore Azure Arc for hybrid deployments
- [ ] Implement GitOps with Flux or ArgoCD
- [ ] Add chaos engineering with Azure Chaos Studio

### Integration Opportunities
- [ ] Azure Logic Apps for workflow automation
- [ ] Azure Functions for serverless processing
- [ ] Azure Service Bus for async messaging
- [ ] Azure Cognitive Services for AI features

---

## Current Status: Planning Phase ✏️

**Last Updated**: 2025-08-12  
**Current Phase**: Foundation Setup  
**Next Milestone**: Health endpoint implementation and Dockerfile creation