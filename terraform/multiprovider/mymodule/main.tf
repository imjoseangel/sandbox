terraform {
  required_providers {
    random = {
      source                = "hashicorp/random"
      version               = "3.1.0"
      configuration_aliases = [random]
    }
  }
}

resource "random_pet" "name" {
  provider = random
}
