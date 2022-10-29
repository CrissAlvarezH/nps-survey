#!/bin/bash

VPC_ID=$1
SUBNET_1_ID=$2
SUBNET_2_ID=$3

[ -z $VPC_ID ] && echo "VPC_ID is required" && exit
[ -z $SUBNET_1_ID ] && echo "SUBNET_1_ID is required" && exit
[ -z $SUBNET_2_ID ] && echo "SUBNET_2_ID is required" && exit

aws cloudformation create-stack \
    --stack-name aws-ecs-npssurvey-app \
    --template-body file://./cloudformation.yaml \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameters ParameterKey=VPCID,ParameterValue=$VPC_ID \
    ParameterKey=Subnet1ID,ParameterValue=$SUBNET_1_ID \
    ParameterKey=Subnet2ID,ParameterValue=$SUBNET_2_ID
