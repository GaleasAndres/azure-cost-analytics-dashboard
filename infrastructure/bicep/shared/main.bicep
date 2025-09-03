targetScope = 'subscription'

// Parameters are passed from parameters.dev.json
param location string
param resourcePrefix string
param environment string
param workload string

// Parameters for Modules
param containerRegistryConfig object
param keyVaultConfig object
param monitoringConfig object

// Creating shared resource group
resource sharedResourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: '${resourcePrefix}-${workload}-${environment}-rg'
  location: location
}

// Deploying Azure Container Registry
module containerRegistryModule 'modules/container-registry.bicep' = {
  name: 'containerRegistryModule'
  scope: sharedResourceGroup
  params: {
    registryName: '${resourcePrefix}${environment}acr'
    location: location
    config: containerRegistryConfig
  }
}

// Deploying Azure Key Vault
module keyVaultModule 'modules/key-vault.bicep' = {
  name: 'keyVaultModule'
  scope: sharedResourceGroup
  params: {
    vaultName: '${resourcePrefix}-${environment}-kv'
    location: location
    config: keyVaultConfig
  }
}

// Deploying Azure Monitoring tools
module monitoringModule 'modules/monitoring.bicep' = {
  name: 'monitoringModule'
  scope: sharedResourceGroup
  params: {
    resourcePrefix: resourcePrefix
    workload: workload
    environment: environment
    location: location
    config: monitoringConfig
  }
}
