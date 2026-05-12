#!/bin/bash
stack=${stack:-history_service}
stage=${stage:-beta}
region=${region:-'eu-west-1'}
aws_profile=${aws_profile:-savir}
terraform_path=${terraform_path:-deployment/terraforms}
s3_backend_bucket_name=${s3_backend_bucket_name:-"justclick-advertisements-infrastructure-and-configurations"}
s3_backend_bucket_region=${s3_backend_bucket_region:-"eu-west-1"}
help()
{
    echo "Usage:  [ -s | --stage ]
        [ -r | --region ]
        [ -t | --stack ]
        [ -p | --profile ]
        [ -w | --path ]
        [ -h | --help  ]"
    exit 2
}

SHORT=s:,t:,p:,w:,a:,b:,h
LONG=stage:,stack:,profile:,path:,region:,s3_backend_bucket_name:,s3_backend_bucket_region:,help
OPTS=$(getopt -a -n weather --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"
while :
do
  case "$1" in
    -s | --stage )
      stage="$2"
      shift 2
      ;;
    -t | --stack )
      stack="$2"
      shift 2
      ;;
    -p | --path )
      terraform_path="$2"
      shift 2
      ;;
    -w | --profile )
      aws_profile="$2"
      shift 2
      ;;
    -r | --region )
      region="$2"
      shift 2
      ;;
    -a | --s3_backend_bucket_name )
      s3_backend_bucket_name="$2"
      shift 2
      ;;
    -b | --s3_backend_bucket_region )
      s3_backend_bucket_region="$2"
      shift 2
      ;;
    -h | --help)
      help
      ;;
    --)
      shift;
      break
      ;;
    *)
      echo "Unexpected option: $1"
      help
      ;;
  esac
done
function build(){
	echo "Started Building"
	mkdir "$PWD/build"
	mkdir "$PWD/build/package"
	mkdir "$PWD/build/artifacts"
	echo "started building requirements ..."
	pip3 install -r requirements.txt -t "$PWD/build/package"
	cp -r "$PWD/src"/* "$PWD/build/package"
	echo "building completed ..."
}
if [[ -d "$PWD/build/" ]]; then
	echo "folder present ..."
	echo "removing build folder"
	rm -r "$PWD/build/"
	echo "building ..."
	build
else
	echo "folder not present ..."
	build
fi
export AWS_PROFILE=$aws_profile
#bash tests.sh
#status=$?
#if test $status -eq 0; then
#  echo "All Tests are successful"
#else
#  echo "One or more tests failed, exiting deployment."
#  exit
#fi

#deploying resources with stage

cd "$terraform_path" || exit
rm -rf .terraform .terraform.lock.hcl out.tfplan terraform.tfplan
s3_backend_key="Terraforms/$stage.$stack/deploy/terraform.tfstate"
terraform init \
-backend=true -force-copy \
-backend-config="bucket=$s3_backend_bucket_name" \
-backend-config="key=$s3_backend_key" \
-backend-config="region=$s3_backend_bucket_region"
terraform plan -var="stack=$stack" -var="profile=$aws_profile" -var="region=$region" \
-var="stage=$stage" -lock=false -out terraform.tfplan
terraform apply -lock=false terraform.tfplan
