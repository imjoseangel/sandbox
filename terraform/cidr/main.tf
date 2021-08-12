provider "azurerm" {
  features {}
}

variable "counter" {
  description = "A simple counter"
  type        = number
  default     = 4
}


locals {
  count = var.counter % 2 == 0 ? var.counter : 0
}

resource "random_pet" "main" {
  count  = local.count
  length = format("%d", local.count / 2)
}

data "azurerm_resource_group" "network" {
  name = "rsg-network"
}

data "azurerm_virtual_network" "network" {
  name                = "net-test-voyager"
  resource_group_name = data.azurerm_resource_group.network.name
}

module "subnet_addrs" {
  source = "hashicorp/subnets/cidr"

  base_cidr_block = data.azurerm_virtual_network.network.address_space[0]

  networks = [
    for name in random_pet.main[*].id :
    {
      "name"     = format("%s", name)
      "new_bits" = format("%d", local.count / 2)
    }
  ]

  #   networks = [
  #     {
  #       name     = format("network-%d", 1)
  #       new_bits = format("%d", local.count / 2)
  #     },
  #     {
  #       name     = format("network-%d", 2)
  #       new_bits = format("%d", local.count / 2)
  #     },
  #     {
  #       name     = format("network-%d", 3)
  #       new_bits = format("%d", local.count / 2)
  #     },
  #     {
  #       name     = format("network-%d", 4)
  #       new_bits = format("%d", local.count / 2)
  #     }
  #   ]
}

resource "azurerm_subnet" "subnets" {
  count                = length(random_pet.main[*].id)
  name                 = format("subnet-%s", random_pet.main[count.index].id)
  resource_group_name  = data.azurerm_resource_group.network.name
  virtual_network_name = data.azurerm_virtual_network.network.name
  address_prefixes     = [module.subnet_addrs.networks[count.index].cidr_block]
}

# output "networks" {
#   value = module.subnet_addrs.networks[*].cidr_block
# }

# output "names" {
#   value = random_pet.main[*].id
# }


output "networks" {
  value = zipmap(random_pet.main[*].id, module.subnet_addrs.networks[*].cidr_block)
}
