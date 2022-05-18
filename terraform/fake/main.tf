resource "fakewebservices_vpc" "primary_vpc" {
  name       = "Primary VPC"
  cidr_block = "0.0.0.0/1"
}
