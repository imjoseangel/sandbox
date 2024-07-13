locals {
  map = tomap({
    "webserver_secret" = random_id.token.hex
    "random_password"  = nonsensitive(random_password.password.result)
    "fernet_key"       = data.external.fernet_key.result.value
  })
}

data "external" "fernet_key" {
  program = [
    "python",
    "-c",
    join("", [
      "from cryptography.fernet import Fernet;",
      "import json;",
      "fernet_key = Fernet.generate_key().decode();",
      "print(json.dumps({'value': fernet_key}));"
    ])
  ]
}

resource "random_pet" "airflowusername" {
  prefix = "airflow"
  length = 1
}

resource "random_id" "token" {
  byte_length = 16
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%*-_=+<>:?"
}

variable "airflowdbhost" {
  type    = string
  default = "airflowpsql"
}

output "fernet_key" {
  value = data.external.fernet_key.result.value
}

output "webserver_secret" {
  value     = random_id.token.hex
  sensitive = false
}

output "random_password" {
  value     = random_password.password.result
  sensitive = true
}

output "map" {
  value = flatten([for key, value in local.map : { name = key, value = value }])
}

output "airflowdb" {
  value = "postgresql://${random_pet.airflowusername.id}%40${var.airflowdbhost}:${local.map["random_password"]}@${var.airflowdbhost}.postgres.database.azure.com:5432/${random_pet.airflowusername.id}?sslmode=prefer"
}

output "airflowusername" {
  value = random_pet.airflowusername.id
}
