provider "random" {
  alias = "random_pet01"
}

provider "random" {
  alias = "random_pet02"
}

module "random" {
  source = "./mymodule"
  providers = {
    random = random.random_pet01
  }
}

module "random02" {
  source = "./mymodule"
  providers = {
    random = random.random_pet02
  }
}
