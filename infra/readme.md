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

# specify svp credentialas as env vars (source env_vars.sh)
export ARM_SUBSCRIPTION_ID="<azure_subscription_id>"
export ARM_TENANT_ID="<azure_subscription_tenant_id>"
export ARM_CLIENT_ID="<service_principal_appid>"
export ARM_CLIENT_SECRET="<service_principal_password>"
```

* Usage:

```bash
# initialize working directory
terraform init

# linting of TF files
tf validate

# create execution plan topreview changes and resource dependencies 
terraform plan -out maint.tfplan

# analyze tf execution plan: summary of the changes to be made, categorized by “to add,” “to change,” or “to destroy.”

# apply the changes required to reach the desired state of the configuration
terraform terraform apply main.tfplan

# proposed destroy changes without executing them
terraform plan -destroy -out main.destroy.tfplan
terraform apply main.destroy.tfplan
```

* State file is either stored locally (alternatively a remote backend can be used).

* Check infra:
```bash
# check k8s context
kubectl --kubeconfig kubeconfig config  current-context
```
## Links

* [aks-terraform](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-terraform?tabs=bash&pivots=development-environment-azure-cli)

* [azurerm_kubernetes_cluster](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster)

* Providers: [azurerm](https://github.com/hashicorp/terraform-provider-azurerm)