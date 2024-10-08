variable "rg_name" {
  default = "sre-demo"
  type = string
  description = "The Name of the resource group"
}

variable "location" {
  default     = "West Europe"
  type = string
  description = "The Azure Region in which all resources in this example should be provisioned"
}

variable "clustername" {
  default = "demoaks"
  type = string
  description = "The name of the Managed Kubernetes Cluster to create"
}