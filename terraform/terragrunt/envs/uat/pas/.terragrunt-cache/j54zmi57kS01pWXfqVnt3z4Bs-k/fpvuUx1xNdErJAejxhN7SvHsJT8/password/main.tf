resource "random_password" "main" {
  length = var.length
}

variable "length" {
  type    = number
  default = 17
}
