terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.81.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "2.53.1"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.2"
    }
    null = {
      source  = "hashicorp/null"
      version = "3.2.2"
    }
    external = {
      source  = "hashicorp/external"
      version = "2.3.3"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.11.2"
    }
  }
  required_version = ">= 1.0.0"
}
