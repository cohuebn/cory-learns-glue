#!/bin/bash

set -e

# Print help text and exit.
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  cat <<HELP
Usage: deploy --tf-organization <your-tf-cloud-organization>

Args:
  - tf-organization: The name of your Terraform cloud organization. This overrides the TF_ORGANIZATION environment variable value when set
  - tf-workspace: The name of your Terraform cloud workspace. This overrides the TF_WORKSPACE environment variable value when set

Examples:
  - deploy
  - deploy --tf-organization alternative-tf-org-name
HELP
  exit 1
fi

# If this isn't a "help" command, get inputs
tf_organization=${TF_ORGANIZATION:-cory-huebner-training}
tf_action="apply"

while [ $# -gt 0 ]; do

   if [[ $1 == *"--"* ]]; then
        param=$(echo "${1/--/}" | tr '-' '_')
        declare $param="$2"
   fi

  shift
done

echo "TF organization used: $tf_organization"
echo "TF action: $tf_action"

cd terraform
terraform init -backend-config="organization=$tf_organization"
terraform fmt
terraform $tf_action