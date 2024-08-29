#!/usr/bin/bash


# Storage accounts need to be unique across all subscriptions globally
# https://learn.microsoft.com/en-us/azure/azure-resource-manager/troubleshooting/error-storage-account-name?tabs=bicep#storage-account-already-taken
export RESOURCE_GROUP_NAME=sre-hackathon
export STORAGE_ACCOUNT_NAME=srehackathon$RANDOM
export CONTAINER_NAME=terraformtfstate

# check if the following environment variables are set: RESOURCE_GROUP_NAME STORAGE_ACCOUNT_NAME CONTAINER_NAME
if [ -z "$RESOURCE_GROUP_NAME" ] || [ -z "$STORAGE_ACCOUNT_NAME" ] || [ -z "$CONTAINER_NAME" ]; then
    echo "Please set the following environment variables: RESOURCE_GROUP_NAME STORAGE_ACCOUNT_NAME CONTAINER_NAME"
    exit 1
fi


# Create resource group
# az group create --name $RESOURCE_GROUP_NAME --location eastus

# Create storage account that will hold the blob container
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob

# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME

echo "Storage account created": $STORAGE_ACCOUNT_NAME
echo "Storage access key:"
ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP_NAME --account-name $STORAGE_ACCOUNT_NAME --query '[0].value' -o tsv)
echo $ACCOUNT_KEY

