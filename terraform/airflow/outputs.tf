output "map" {
  value = flatten([for key, value in local.map : { name = key, value = value }])
}
