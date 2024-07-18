include {
  path = find_in_parent_folders()
}

dependencies {
  paths = ["../pet"]
}

terraform {
  source = "../../../mods/password"
}

// terraform {
//   source = "${get_parent_terragrunt_dir()}/mods//password"
// }

inputs = {
  length = 2
}
