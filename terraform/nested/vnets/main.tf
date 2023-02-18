locals {

  dns_zones = [
    "privatelink.dfs.core.windows.net",
    "privatelink.monitor.azure.com",
    "privatelink.redis.cache.windows.net"
  ]

  envs = [
    "dev",
    "stg",
    "prd"
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

output "resources" {
  value = local.resources
}
