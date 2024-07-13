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

resource "random_id" "token" {
  byte_length = 16
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%*-_=+<>:?"
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
