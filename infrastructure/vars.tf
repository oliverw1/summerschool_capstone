variable "summer_capstone_version" {
  default = ""
}

data "external" "git_describe" {
  program = ["${path.module}/git_describe.sh"]
}