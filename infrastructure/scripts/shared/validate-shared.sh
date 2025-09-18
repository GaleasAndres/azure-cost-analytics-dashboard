#!/bin/bash

read -p "Enter the Azure location: " location

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
template_file="$script_dir/../../bicep/shared/main.bicep"
parameters_file="$script_dir/../../bicep/shared/parameters.dev.json"

template_file="$(realpath "$template_file")"
parameters_file="$(realpath "$parameters_file")"

# Trying to deploy the template to validate it
output=$(az deployment sub what-if --location "$location" --template-file "$template_file" --parameters "@$parameters_file" 2>&1)
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "$output"
    echo -e "\033[32mValidation succeeded. The deployment can proceed.\033[0m"
else
    # Check if there is an error with the location specified
    if echo "$output" | grep -q "LocationNotAvailableForDeployment"; then
        echo -e "\033[33mThe location '$location' is not available or doesn't exist, please make sure to enter a valid Azure location.
Use 'az account list-locations' to see the list of available locations.\033[0m"
    else
        echo -e "\033[31mValidation failed with error:\033[0m"
        echo "$output"
    fi
fi