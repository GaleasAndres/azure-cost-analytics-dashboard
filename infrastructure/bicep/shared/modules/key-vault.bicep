targetScope = 'resourceGroup'

// Parameters are passed from main.bicep
param vaultName string
param location string
param config object

// Deploying Azure Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' = {
  name: vaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: config.sku
    }
    tenantId: subscription().tenantId
    // More security and access configurations can be added here
    accessPolicies: []
  }
}
