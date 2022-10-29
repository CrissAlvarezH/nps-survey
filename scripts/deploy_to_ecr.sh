#!/bin/bash

AWS_ACCOUNT_NUMBER=$1
AWS_REGION=$2

[ -z $AWS_ACCOUNT_NUMBER ] && echo "AWS_ACCOUNT_NUMBER is required" && exit
[ -z $AWS_REGION ] && echo "AWS_REGION is required" && exit

docker build --no-cache -t aws-ecs-npssurvey-app -f ./compose/production/Dockerfile .
docker tag aws-ecs-npssurvey-app:latest $AWS_ACCOUNT_NUMBER.dkr.ecr.$AWS_REGION.amazonaws.com/npssurvey/service-app:latest
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_NUMBER.dkr.ecr.$AWS_REGION.amazonaws.com
docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.$AWS_REGION.amazonaws.com/npssurvey/service-app:latest
# aws ecs update-service --cluster aws-ecs-npssurvey-app --service aws-ecs-npssurvey-app --force-new-deployment