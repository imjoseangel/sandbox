output "servers" {
  value = fakewebservices_server.servers
}

output "vpc" {
  value = fakewebservices_vpc.primary_vpc
}

output "load_balancer" {
  value = fakewebservices_load_balancer.primary_lb
}

output "database" {
  value = fakewebservices_database.prod_db
}
