#!/bin/bash

aws cloudformation create-stack \
    --stack-name aws-ecs-npssurvey-app \
    --template-body file://./cloudformation.yaml \
    --capabilities CAPABILITY_NAMED_IAM \

