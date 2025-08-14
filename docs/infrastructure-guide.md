# Infrastructure Guide

## 🏗️ Infrastructure Overview

This project uses **Azure Bicep** for Infrastructure as Code (IaC) to deploy and manage Azure resources across multiple hosting strategies and environments. The infrastructure is designed for learning Azure services while maintaining cost efficiency and production readiness.

## 📁 Folder Structure Explained

### `/infrastructure/` vs `/deployments/` - Key Differences

```
infrastructure/          # WHAT resources to create (Azure infrastructure)
├── bicep/              # Bicep templates for Azure resources
└── scripts/            # Helper scripts for deployment

deployments/            # HOW to package and deploy the application
├── docker/             # Container definitions and build configs
├── kubernetes/         # K8s manifests for AKS deployment
├── helm/              # Helm charts for advanced K8s deployments
└── container-apps/     # Azure Container Apps configurations
```


## 🏗️ Infrastructure Structure Deep Dive

### 📂 `/infrastructure/bicep/`

The heart of our Infrastructure as Code implementation using Azure Bicep.

#### **`/modules/`** - Reusable Components
```
modules/
├── app-service/         # App Service Plan + Web App
│   ├── main.bicep      # Resource definitions
│   ├── parameters.json # Default parameters
│   └── outputs.bicep   # Resource outputs (URLs, IDs, etc.)
├── container-registry/ # Azure Container Registry
├── monitoring/        # Application Insights + Log Analytics
├── networking/        # VNets, subnets, NSGs
└── storage/          # Storage accounts, file shares
```

**Purpose**: Like functions in programming - write once, use everywhere.

**Example**: The `app-service` module can be used by dev, staging, and prod environments with different parameters.

#### **`/environments/`** - Complete Environment Deployments
```
environments/
├── development/
│   ├── main.bicep           # Orchestrates multiple modules
│   ├── parameters.dev.json  # Dev-specific values
│   └── deploy.sh           # Deployment script
├── staging/
└── production/
```

**Purpose**: Combine modules to create complete environments.

**Example**: Development environment uses Basic SKU services, Production uses Premium.

#### **`/shared/`** - Common Configurations
```
shared/
├── resource-naming.bicep  # Consistent naming conventions
├── common-tags.bicep     # Standard resource tags
└── variables.bicep       # Global variables and constants
```

**Purpose**: Ensure consistency across all resources and environments.

### 📂 `/infrastructure/scripts/`

Helper scripts for infrastructure management.

```
scripts/
├── setup-azure-cli.sh      # Initial Azure CLI and Bicep setup
├── deploy-all-envs.sh      # Deploy to multiple environments
├── validate-bicep.sh       # Template validation before deployment
└── cleanup.sh             # Resource cleanup and cost management
```

## 🎯 Resource Organization Strategy

### Resource Groups per Hosting Strategy

```
Dev Environment:
├── myapp-dev-shared-rg        # Container Registry, Key Vault
├── myapp-dev-appservice-rg    # App Service deployment
├── myapp-dev-aci-rg          # Azure Container Instances
├── myapp-dev-aks-rg          # Azure Kubernetes Service
└── myapp-dev-containerapp-rg  # Azure Container Apps

Prod Environment:
├── myapp-prod-shared-rg      # Container Registry, Key Vault
└── myapp-prod-appservice-rg  # App Service only (cost optimized)
```

**Benefits:**
- ✅ **Isolated experiments** - AKS problems don't affect App Service
- ✅ **Clear cost attribution** - See exactly what each hosting method costs
- ✅ **Easy cleanup** - Delete entire resource groups when done
- ✅ **Independent scaling** - Scale services independently

## 🧩 Bicep Module Design Patterns

### 1. **Shared Resources Module**
```bicep
// infrastructure/bicep/modules/container-registry/main.bicep
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-09-01' = {
  name: registryName
  location: location
  sku: {
    name: skuName  // Basic for dev, Standard for prod
  }
  properties: {
    adminUserEnabled: true
  }
}
```

### 2. **App Service Module**
```bicep
// infrastructure/bicep/modules/app-service/main.bicep
resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: planName
  location: location
  sku: {
    name: skuName    // B1 for dev, P1V2 for prod
    capacity: capacity
  }
}

resource webApp 'Microsoft.Web/sites@2021-02-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'DOCKER|${containerImage}'
    }
  }
}
```

### 3. **Environment Orchestration**
```bicep
// infrastructure/bicep/environments/development/main.bicep
module sharedResources '../../../modules/shared/main.bicep' = {
  name: 'shared-resources'
  params: {
    environment: 'dev'
    location: location
  }
}

module appService '../../../modules/app-service/main.bicep' = {
  name: 'app-service'
  params: {
    environment: 'dev'
    skuName: 'B1'  // Basic for development
    containerImage: '${sharedResources.outputs.acrLoginServer}/myapp:latest'
  }
}
```

## 🔧 Parameter Management Strategy

### Environment-Specific Parameters
```json
// infrastructure/bicep/environments/development/parameters.dev.json
{
  "environment": "dev",
  "location": "East US",
  "appServiceSku": "B1",
  "containerRegistrySku": "Basic",
  "logRetentionDays": 30
}
```

```json
// infrastructure/bicep/environments/production/parameters.prod.json
{
  "environment": "prod",
  "location": "East US",
  "appServiceSku": "P1V2",
  "containerRegistrySku": "Standard",
  "logRetentionDays": 365
}
```

## 🚀 Deployment Workflow

### Manual Deployment Process
```bash
# 1. Validate Bicep template
az deployment group validate \
  --resource-group myapp-dev-shared-rg \
  --template-file main.bicep \
  --parameters @parameters.dev.json

# 2. Preview changes
az deployment group what-if \
  --resource-group myapp-dev-shared-rg \
  --template-file main.bicep \
  --parameters @parameters.dev.json

# 3. Deploy resources
az deployment group create \
  --resource-group myapp-dev-shared-rg \
  --template-file main.bicep \
  --parameters @parameters.dev.json
```

### Automated Deployment (CI/CD)
```yaml
# GitHub Actions workflow excerpt
- name: Deploy Infrastructure
  run: |
    az deployment group create \
      --resource-group ${{ env.RESOURCE_GROUP }} \
      --template-file infrastructure/bicep/environments/${{ env.ENVIRONMENT }}/main.bicep \
      --parameters @infrastructure/bicep/environments/${{ env.ENVIRONMENT }}/parameters.${{ env.ENVIRONMENT }}.json
```

## 🏷️ Resource Naming Convention

### Naming Pattern
```
{app-name}-{environment}-{service-type}-{region}
```

### Examples
```
azurecost-dev-app-eastus        # App Service
azurecost-dev-acr-eastus        # Container Registry
azurecost-dev-ai-eastus         # Application Insights
azurecost-prod-app-eastus       # Production App Service
```

### Benefits
- ✅ **Consistent identification** - Easily identify resources
- ✅ **Environment separation** - Clear dev/prod boundaries
- ✅ **Cost tracking** - Group costs by environment
- ✅ **Automation friendly** - Predictable naming for scripts

## 🔍 Monitoring and Observability Infrastructure

### Application Insights Integration
```bicep
resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
  }
}
```

### Log Analytics Workspace
```bicep
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: workspaceName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: retentionDays
  }
}
```

## 🔐 Security and Access Management

### Key Vault Integration
```bicep
resource keyVault 'Microsoft.KeyVault/vaults@2021-10-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenant().tenantId
    accessPolicies: [
      {
        tenantId: tenant().tenantId
        objectId: webApp.identity.principalId
        permissions: {
          secrets: ['get']
        }
      }
    ]
  }
}
```

### Managed Identity for App Service
```bicep
resource webApp 'Microsoft.Web/sites@2021-02-01' = {
  name: appName
  location: location
  identity: {
    type: 'SystemAssigned'  // Enable managed identity
  }
  properties: {
    // ... other properties
  }
}
```

## 📊 Infrastructure Outputs and Dependencies

### Module Outputs
```bicep
// modules/container-registry/outputs.bicep
output acrLoginServer string = containerRegistry.properties.loginServer
output acrResourceId string = containerRegistry.id
output acrName string = containerRegistry.name
```

### Cross-Module Dependencies
```bicep
// In environment main.bicep
module appService '../../../modules/app-service/main.bicep' = {
  name: 'app-service'
  params: {
    containerRegistryName: sharedResources.outputs.acrName
    applicationInsightsKey: monitoring.outputs.appInsightsInstrumentationKey
  }
}
```

---

*This infrastructure guide provides the foundation for understanding how Azure resources are organized, deployed, and managed using Bicep Infrastructure as Code.*