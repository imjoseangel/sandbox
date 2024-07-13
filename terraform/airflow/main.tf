data "external" "fernet_key" {
  program = ["python", "-c", "from cryptography.fernet import Fernet; import json; FERNET_KEY = Fernet.generate_key().decode(); print(json.dumps({'value': FERNET_KEY}))"]
}

output "provisioner" {
  value = data.external.fernet_key.result.value
}
