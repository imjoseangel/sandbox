variable "environment" {
  description = "Azure tenant Id."
  default = "holaquetalestas"
}

output name {
  value = substr(var.environment, 0, 8)
}
