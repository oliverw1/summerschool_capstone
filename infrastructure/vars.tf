data "external" "git_describe" {
  program = ["${path.module}/git_describe.sh"]
}