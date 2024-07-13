locals {
  map = tomap({
    "webserver_secret" = random_id.token.hex
    "random_password"  = nonsensitive(random_password.password.result)
    "fernet_key"       = null_resource.fernet_key.triggers.stdout
    "airflowdb"        = nonsensitive("postgresql://${random_pet.airflowusername.id}%40${var.airflowdbhost}:${random_password.password.result}@${var.airflowdbhost}.postgres.database.azure.com:5432/${random_pet.airflowusername.id}?sslmode=prefer")
    "pgbouncer"        = nonsensitive("db+postgresql://${random_pet.airflowusername.id}%40${var.airflowdbhost}:${random_password.password.result}@${var.airflowdbhost}.postgres.database.azure.com:5432/pgbouncer?sslmode=prefer")
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

resource "null_resource" "fernet_key" {
  triggers = {
    stdout = data.external.fernet_key.result.value
  }

  lifecycle {
    ignore_changes = [
      triggers
    ]
  }
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

output "map" {
  value = flatten([for key, value in local.map : { name = key, value = value }])
}
