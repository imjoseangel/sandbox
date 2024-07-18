include {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../comm/pet"
}

// terraform {
//   source = "${get_parent_terragrunt_dir()}/comm//pet"
// }

inputs = {
  length = 2
}
