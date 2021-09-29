terraform {
  backend "local" {
    path = "example.tfstate"
  }
}

resource "random_pet" "main" {
}

output "name" {
  value = random_pet.main.id
}
