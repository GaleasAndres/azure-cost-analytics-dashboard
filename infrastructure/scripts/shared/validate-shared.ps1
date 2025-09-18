$location = Read-Host "Enter the Azure location: "

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$templateFile = Resolve-Path (Join-Path $scriptDir "..\..\bicep\shared\main.bicep")
$parametersFile = Resolve-Path (Join-Path $scriptDir "..\..\bicep\shared\parameters.dev.json")

# Trying to deploy the template to validate it
try {
    New-AzSubscriptionDeployment -Location $location -TemplateFile $templateFile `
-TemplateParameterFile $parametersFile -WhatIf -ErrorAction Stop
    Write-Host "Validation succeeded. The deployment can proceed." -ForegroundColor Green
}
catch {
    # Check if there is an error with the location specified
    if ($_.Exception.Message -like "*LocationNotAvailableForDeployment*"){
        Write-Host ("The location '$location' is not available or doesn't exist, please make sure to enter a valid Azure location.
Use 'Get-AzLocation' to see the list of available locations.")`
        -ForegroundColor Yellow
    }
}

