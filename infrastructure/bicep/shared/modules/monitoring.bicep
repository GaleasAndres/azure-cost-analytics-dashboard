targetScope = 'resourceGroup'

// Parameters are passed from main.bicep
param location string
param resourcePrefix string
param workload string
param environment string  
param config object

// Deploying Azure Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: '${resourcePrefix}-${workload}-${environment}-logs'
  location: location
  properties: {
    sku: {
      name: config.logAnalytics.sku
    }
    retentionInDays: config.logAnalytics.retentionInDays
  }
}

// Deploying Azure Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${resourcePrefix}-${workload}-${environment}-appi'
  location: location
  kind: config.appInsights.appType
  properties: {
    Application_Type: config.appInsights.appType
    WorkspaceResourceId: logAnalytics.id
    SamplingPercentage: 20
  }
}
