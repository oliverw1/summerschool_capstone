resource "aws_ecr_repository" "ecr_repos" {
  name  = "${local.env_name}/export"
}

resource "aws_batch_job_definition" "export" {
  name = "${local.env_name}-export"
  type = "container"

  container_properties = <<CONTAINER_PROPERTIES
{
    "command": ["python3 /opt/spark/work-dir/scripts/01_export_data_to_db.py"],
    "image": "${aws_ecr_repository.ecr_repos.name}:${var.summer_capstone_version}",
    "memory": 6000,
    "vcpus": 4,
    "jobRoleArn": "${aws_iam_role.job_role.arn}",
    "environment": [
        {"name": "AWS_DEFAULT_REGION", "value": "eu-west-1"}
    ]
}
CONTAINER_PROPERTIES
}

resource "aws_iam_role" "job_role" {
  name = "export-task-${local.env_name}"
  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Create a new S3 policy
data "aws_iam_policy_document" "s3_access" {
  statement {
    actions = [
      "s3:Get*",
      "s3:List*"
    ]
    resources = [
      "${local.s3_bucket_arn}/*",
      local.s3_bucket_arn,
    ]
    effect = "Allow"
  }
}

# Attach S3 policy to project role
resource "aws_iam_role_policy" "s3_policy" {
  name = "s3_policy"
  policy = data.aws_iam_policy_document.s3_access.json
  role = aws_iam_role.job_role.id
}

data "aws_iam_policy_document" "secret_manager" {
  statement {
    actions = [
      "secretsmanager:GetRandomPassword",
      "secretsmanager:GetResourcePolicy",
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
      "secretsmanager:ListSecretVersionIds"
    ]
    resources = [
      "arn:aws:secretsmanager:eu-west-1:130966031144:secret:${local.secret_name}*"
    ]
    effect = "Allow"
  }
}

resource "aws_iam_role_policy" "secret_manager" {
  name = "secret_policy"
  policy = data.aws_iam_policy_document.secret_manager.json
  role = aws_iam_role.job_role.id
}