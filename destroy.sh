stage="beta"
profile="savir"
region="eu-west-1"
stack="history_service"
terraform_path="deployment/terraforms"
s3_backup_folder_name="history_service"
s3_backup_bucket="justclick-advertisements-infrastructure-and-configurations"
s3_backup_folder="Terraforms/$stage.$s3_backup_folder_name/deploy/terraform.tfstate"
s3_backup_region="eu-west-1"
cd $terraform_path || exit
export AWS_PROFILE=$profile

terraform init -backend=true -force-copy \
-input=false \
-backend-config "bucket=$s3_backup_bucket" \
-backend-config "key=$s3_backup_folder" \
-backend-config "region=$s3_backup_region"
terraform destroy  -var="stack=$stack" -var="profile=$profile" -var="region=$region" -var="stage=$stage"
