#!/bin/bash
stack=${stack:-authentication_service}
stage=${stage:-beta}
region=${region:-'eu-west-1'}
aws_profile=${aws_profile:-savir}
terraform_path=${terraform_path:-deployment/static}
export AWS_PROFILE=$aws_profile
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

SHORT=s:,t:,p:,w:,h
LONG=stage:,stack:,profile:,path:,help
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
    -path | --path )
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
function configure_aws(){
	echo "Enter AWS Credentials:"
	aws configure --profile "$aws_profile"
	echo "Enter Again:"
	aws configure --profile "$aws_profile"
}
if command -v aws --version ; then
	echo "AWS CLI already present"
	configure_aws
else
	echo "Installing AWS CLI"
	apt-get install awscli
	echo "Installation Done"
	configure_aws
fi
