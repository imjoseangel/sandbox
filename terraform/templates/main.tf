locals {
  rendered = templatefile("${path.module}/backends.tmpl", {
    addr = "Justin", port = "8080"
  })
}

output name {
  value = local.rendered
}


# resource "null_resource" "pretend_template" {
#   triggers = {
#     rendered = "${local.rendered}"
#   }

#   provisioner "local-exec" {
#     command = "echo ${local.rendered}"
#   }
# }
