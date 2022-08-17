provider "azurerm" {
  alias           = "dns"
  subscription_id = "00000000-0000-000a-0a00-0e00000e00cf"
  features {}
}

data "azurerm_dns_zone" "main" {
  provider            = azurerm.dns
  name                = "secondary.example.com"
  resource_group_name = "rsg-publicdns"
}

data "azurerm_app_service" "main" {
  name                = var.name
  resource_group_name = var.resource_group
}

resource "azurerm_dns_cname_record" "main" {
  provider            = azurerm.dns
  name                = data.azurerm_app_service.main.name
  zone_name           = data.azurerm_dns_zone.main.name
  resource_group_name = data.azurerm_dns_zone.main.resource_group_name
  ttl                 = 3600
  record              = format("%s.azurewebsites.net", data.azurerm_app_service.main.name)
}

resource "azurerm_dns_txt_record" "main" {
  provider            = azurerm.dns
  name                = format("asuid.%s", data.azurerm_app_service.main.name)
  zone_name           = data.azurerm_dns_zone.main.name
  resource_group_name = data.azurerm_dns_zone.main.resource_group_name
  ttl                 = 3600

  record {
    value = data.azurerm_app_service.main.custom_domain_verification_id
  }
}

resource "azurerm_app_service_custom_hostname_binding" "main" {
  hostname            = trim(azurerm_dns_cname_record.main.fqdn, ".")
  app_service_name    = data.azurerm_app_service.main.name
  resource_group_name = data.azurerm_app_service.main.resource_group_name
  depends_on          = [azurerm_dns_txt_record.main]

  # Ignore ssl_state and thumbprint as they are managed using
  # azurerm_app_service_certificate_binding
  lifecycle {
    ignore_changes = [ssl_state, thumbprint]
  }
}

resource "azurerm_app_service_managed_certificate" "main" {
  custom_hostname_binding_id = azurerm_app_service_custom_hostname_binding.main.id
}

resource "azurerm_app_service_certificate_binding" "main" {
  hostname_binding_id = azurerm_app_service_custom_hostname_binding.main.id
  certificate_id      = azurerm_app_service_managed_certificate.main.id
  ssl_state           = "SniEnabled"
}
