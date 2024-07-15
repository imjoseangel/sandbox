data "azuread_client_config" "main" {}

data "external" "fernet_key2" {
  program = [
    "${local.python}",
    "-c",
    join("", [
      "from cryptography.fernet import Fernet;",
      "import json;",
      "fernet_key = Fernet.generate_key().decode();",
      "print(json.dumps({'value': fernet_key}));"
    ])
  ]
}

data "external" "fernet_key" {
  program = [
    "${local.python}",
    "${local.fernet}",
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

resource "time_rotating" "main" {
  rotation_days = 730
}

resource "random_id" "token" {
  byte_length = 16
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%*-_=+<>:?"
}

resource "azuread_application" "main" {
  display_name = lower(format("%s-sso", resource.random_pet.airflowusername.id))
  owners       = [data.azuread_client_config.main.object_id]

  required_resource_access {
    resource_app_id = "00000003-0000-0000-c000-000000000000" # Microsoft Graph

    resource_access {
      id   = "df021288-bdef-4463-88db-98f22de89214" # User.Read.All
      type = "Role"
    }
  }

  password {
    display_name = lower(format("%s-sso-secret", resource.random_pet.airflowusername.id))
    start_date   = time_rotating.main.id
    end_date     = timeadd(time_rotating.main.id, "17520h")
  }
}
