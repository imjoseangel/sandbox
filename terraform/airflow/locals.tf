locals {
  python = (substr(pathexpand("~"), 0, 1) == "/") ? "python3" : "python.exe"
  fernet = "fernet.py"
  map = tomap({
    "webserver_secret" = random_id.token.hex
    "random_password"  = nonsensitive(random_password.password.result)
    "fernet_key"       = null_resource.fernet_key.triggers.stdout
    "airflowdb"        = nonsensitive("postgresql://${random_pet.airflowusername.id}%40${var.airflowdbhost}:${random_password.password.result}@${var.airflowdbhost}.postgres.database.azure.com:5432/${random_pet.airflowusername.id}?sslmode=prefer")
    "pgbouncer"        = nonsensitive("db+postgresql://${random_pet.airflowusername.id}%40${var.airflowdbhost}:${random_password.password.result}@${var.airflowdbhost}.postgres.database.azure.com:5432/pgbouncer?sslmode=prefer")
    "tenant_id"        = data.azuread_client_config.main.tenant_id
    "client_id"        = azuread_application.main.client_id
    "client_secret"    = nonsensitive(tolist(azuread_application.main.password).0.value)
  })
}
