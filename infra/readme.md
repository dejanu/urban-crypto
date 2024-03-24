## Terraform

* Terraform only supports authenticating to Azure via the Azure CLI
```bash
az login

# get subscriptions
az account list -o table --all

# set subscription  
az account set --subscription <subscription_ID>

# list resource groups
az group list -o table

# list service principals
az ad sp list --query "[].{id:id,name:displayName}" --show-mine

# create svp 
az ad sp create-for-rbac --name <service_principal_name> --role Contributor --scopes /subscriptions/<subscription_id>
az ad sp create-for-rbac --name dealsvp --role Contributor --scopes /subscriptions/33412aad-8988-47c9-a0ae-0c95efad1811
```

## Links

* [aks-terraform](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-terraform?tabs=bash&pivots=development-environment-azure-cli)

* [azurerm_kubernetes_cluster](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster)