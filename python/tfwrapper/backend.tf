terraform {
  backend "azurerm" {
    resource_group_name  = "rsg-sharedresources"
    storage_account_name = "storageterraform"
    container_name       = "tfstate"
  }
}
