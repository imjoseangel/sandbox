terraform {
  # This module is now only being tested with Terraform 0.13.x. However, to make upgrading easier, we are setting
  # 0.12.26 as the minimum version, as that version added support for required_providers with source URLs, making it
  # forwards compatible with 0.13.x code.
  required_version = ">= 0.12.26"
}

variable "names" {
  description = "Create output with these names"
  type        = map(string)
  default     = {
      "api_services": "bigquery.dataEditor",
      "xx": "yy"
  }
}

# website::tag::1:: The simplest possible Terraform module: it just outputs "Hello, World!"
output "my_output" {
  value = { for p in sort(keys(var.names)) : var.names[p] => format("serviceAccount: %s", p) }
}
