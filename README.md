# Cory learns glue
A project used for me to learn how to use [AWS Glue](https://aws.amazon.com/glue/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc) and other adventures in data analytics.

## Deployment
To deploy this application, take the following steps:
1. Run `./deploy.sh`. This will run Terraform to deploy necessary resources out to AWS
1. Application code is deployed via [circleci](https://circleci.com/). Go to [the project](https://app.circleci.com/pipelines/github/cohuebn/cory-learns-glue) and deploy application code from there.

## Local development
To develop the ETL scripts used by Glue, see the instructions in the [etl](etl/README.md)
