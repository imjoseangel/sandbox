locals {

  dns_zones = [
    "privatelink.dfs.core.windows.net",
    "privatelink.monitor.azure.com",
    "privatelink.redis.cache.windows.net"
  ]

  vnets = [
    "vnet-spoke-we-dev",
    "vnet-spoke-we-stg",
    "vnet-spoke-we-prd"
  ]

  vnet_links = [
    {
      "linkName" : "name-of-vnet-link1"
      "vnetId" : "vnet--resource-id-placeholder1"
    },
    {
      "linkName" : "name-of-vnet-link2"
      "vnetId" : "vnet--resource-id-placeholder2"
    }
  ]

  resources = flatten([
    for dns_zone in local.dns_zones : [
      for link in local.vnet_links : {
        zone      = dns_zone
        vnet_link = link
      }
    ]
  ])
}

output "resources" {
  value = local.resources
}
