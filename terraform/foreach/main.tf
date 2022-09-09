locals {
  myvar1 = [
    ["test1", "*"],
    ["test1", "-"]
  ]

  myvar2 = {
    "random1" = { prefix = "test1", separator = "*" },
    "random2" = { prefix = "test1", separator = "-" },
  }
}

resource "random_pet" "test1" {
  count     = length(local.myvar1)
  prefix    = element(local.myvar1[count.index], 0)
  separator = element(local.myvar1[count.index], 1)
}

resource "random_pet" "test2" {
  for_each  = local.myvar2
  prefix    = each.value.prefix
  separator = each.value.separator
}
