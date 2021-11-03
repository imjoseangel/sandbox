module "naming" {
  source = "Azure/naming/azurerm"
  suffix = ["test"]
}

module "everything" {
  source                 = "Azure/naming/azurerm"
  prefix                 = ["pre", "fix"]
  suffix                 = ["su", "fix"]
  unique-seed            = "random"
  unique-length          = 2
  unique-include-numbers = false
}

output "everything" {
  value = module.everything.kubernetes_cluster.name_unique
}

terraform {
  required_providers {
    azurecaf = {
      source  = "aztfmod/azurecaf"
      version = "1.2.4"
    }
  }
}

provider "azurecaf" {

}

resource "azurecaf_naming_convention" "cafrandom_rg" {
  name          = "aztfmod"
  prefix        = "dev"
  resource_type = "rg"
  postfix       = "001"
  max_length    = 23
  convention    = "cafrandom"
}

output "cafrandom" {
  value = azurecaf_naming_convention.cafrandom_rg.result
}
