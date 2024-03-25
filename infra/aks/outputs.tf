resource "local_file" "kubeconfig" {
  depends_on   = [azurerm_kubernetes_cluster.cluster]
  filename     = "kubeconfig"
  content      = azurerm_kubernetes_cluster.cluster.kube_config_raw
}

resource "local_file" "clustercert" {
  depends_on   = [azurerm_kubernetes_cluster.cluster]
  filename     = "clustercert"
  content      = azurerm_kubernetes_cluster.cluster.kube_config[0].client_certificate
}