targetScope = 'resourceGroup'

// Parameters are passed from main.bicep
param registryName string
param location string
param config object

// Deploying Azure Container Registry
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-02-01-preview' = {
  name: registryName
  location: location
  sku: {
    name: config.sku
  }
  properties: {
    adminUserEnabled: config.adminUserEnabled
    publicNetworkAccess: config.publicNetworkAccess
  }
}
