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

output "fernet_key" {
  value = data.external.fernet_key.result.value
}

output "webserver_secret" {
  value     = random_id.token.hex
  sensitive = false
}
