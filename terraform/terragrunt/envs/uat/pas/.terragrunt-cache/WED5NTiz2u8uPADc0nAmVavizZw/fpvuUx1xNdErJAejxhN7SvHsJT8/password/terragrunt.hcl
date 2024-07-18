include {
  path = find_in_parent_folders()
}

dependencies {
  paths = ["../pet"]
}

terraform {
  source = "${get_parent_terragrunt_dir()}/mods//password"
}

inputs = {
  length = 2
}
