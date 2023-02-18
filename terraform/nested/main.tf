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
      name                = "vnet-spoke-we-dev"
      subscription_id     = "5e91a5fa-3787-4f0f-84ff-d7e9590c724a"
      resource_group_name = "rg-crossresources-dev"
    },
    {
      name                = "vnet-spoke-we-stg"
      subscription_id     = "4b570203-711c-4703-bc57-4a326e6a1dab"
      resource_group_name = "rg-crossresources-stg"
    },
    {
      name                = "vnet-spoke-we-prd"
      subscription_id     = "1e3ccec4-6390-4365-8688-aa89a0b08834"
      resource_group_name = "rg-crossresources-prd"
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
