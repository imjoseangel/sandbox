locals {

  dns_zones = [
    "privatelink.dfs.core.windows.net",
    "privatelink.monitor.azure.com",
    "privatelink.redis.cache.windows.net"
  ]

  vnets = [
    {
      name                = "vnet-dev"
      subscription_id     = "xxx"
      resource_group_name = "rg-dev"
    },
    {
      name                = "vnet-stg"
      subscription_id     = "xxx"
      resource_group_name = "rg-stg"
    },
    {
      name                = "vnet-prd"
      subscription_id     = "xxx"
      resource_group_name = "rg-prd"
    }
  ]

  resources = flatten([
    for dns_zone in local.dns_zones : [
      for vnet in local.vnets : {
        zone      = dns_zone
        link_name = format("privatedns-link-%s", vnet.name)
        vnet_id   = format("/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/virtualNetworks/%s", vnet.subscription_id, vnet.resource_group_name, vnet.name)
      }
    ]
  ])
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "myzonersg"
  location = "westeurope"
}

resource "azurerm_private_dns_zone" "main" {
  count               = length(local.dns_zones)
  name                = local.dns_zones[count.index]
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "main" {
  for_each = {
    for resource in local.resources : "${resource.zone}.${resource.link_name}" => resource
  }
  name                  = each.value.link_name
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = each.value.zone
  virtual_network_id    = each.value.vnet_id
}
