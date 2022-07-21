data "aws_s3_bucket" "exists" {
  bucket = "zih-zugl-airflow-poc-ec-s3s"
}

resource "aws_s3_bucket" "main" {
  count  = data.aws_s3_bucket.exists.bucket == "" ? 1 : 0
  bucket = "zih-zugl-airflow-poc-ec-s3"
}
