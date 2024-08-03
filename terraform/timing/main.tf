locals {
  not_before_date = timestamp()
  expiration_date = timeadd(timestamp(), "4320h")
}

resource "time_rotating" "main" {
  rotation_days = 180
}

resource "random_password" "pass" {
  length = 24
  keepers = {
    time = time_rotating.main.id
  }
}

output "locals" {
  value = {
    not_before_date = local.not_before_date,
    expiration_date = local.expiration_date
  }
}

output "time_rotating" {
  value = {
    not_before_date  = time_rotating.main.rfc3339,
    expiration_date  = time_rotating.main.rotation_rfc3339
    expiration_date2 = timeadd(time_rotating.main.id, "4320h")
  }
}
