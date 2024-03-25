terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.48.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "srelearnResourceGroup"
  location = "${var.location}"
}

resource "azurerm_kubernetes_cluster" "cluster" {
  name                = "${var.clustername}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${var.clustername}"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2_v2"
  }

// must define either a dns_prefix or a dns_prefix_private_cluster
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

/*
output "kube_config" {
  value = azurerm_kubernetes_cluster.cluster.kube_config_raw
  sensitive = true
}
*/