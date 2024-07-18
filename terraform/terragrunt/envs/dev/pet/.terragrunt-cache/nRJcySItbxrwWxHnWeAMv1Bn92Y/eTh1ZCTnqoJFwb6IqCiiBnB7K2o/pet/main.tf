resource "random_pet" "main" {
  length = var.length
}

variable "length" {
  type    = number
  default = 1
}
