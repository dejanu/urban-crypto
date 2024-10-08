terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.48.0"
    }
  }

    backend "azurerm" {
      resource_group_name  = "sre-hackathon"
      storage_account_name = "srehackathon12632"
      container_name       = "terraformtfstate"
      key                  = "terraform.tfstate"
      }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.rg_name}"
  location = "${var.location}"
}

resource "azurerm_kubernetes_cluster" "cluster" {
  name                = "${var.clustername}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${var.clustername}"

# Network plugin to use for networking
network_profile {
    network_plugin    = "kubenet"
    load_balancer_sku = "standard"
    outbound_type     = "loadBalancer"
  }

  
  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2_v2"
  }

# enable HTTP Application Routing addon, which provides an ingress controller
addon_profile {
    http_application_routing {
      enabled = true
    }
}

identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "SRE"
  }

# Enable Role Based Access Control
role_based_access_control {
  enabled = true
  }

}

output "client_certificate" {
   value     = azurerm_kubernetes_cluster.cluster.kube_config[0].client_certificate
   sensitive = true
 }

output "kube_config" {
  value = azurerm_kubernetes_cluster.cluster.kube_config_raw
  sensitive = true
}
