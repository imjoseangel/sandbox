data "http" "azureips" {
  url = "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20211122.json"

  # Optional request headers
  request_headers = {
    Accept = "application/json"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_route" "main" {
  count               = length(local.ip_addrs)
  name                = format("acceptanceTestRoute%s", count.index)
  resource_group_name = "we-d-rsg-network"
  route_table_name    = "udr"
  address_prefix      = local.ip_addrs[count.index]
  next_hop_type       = "Internet"
}

locals {
  raw_data = jsondecode(data.http.azureips.body)
  values   = local.raw_data.values[*]
  ip_addrs = local.values[index(local.values.*.name, "AzureCloud.westus")].properties.addressPrefixes
}
