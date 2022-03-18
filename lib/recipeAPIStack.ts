import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ResourceName } from '../lib/resource_name';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export interface ToDoAPIStackProps extends StackProps {
  resourceName: ResourceName;
}

export class recipeAPIStack extends Stack {
  constructor(scope: Construct, id: string, props: ToDoAPIStackProps) {
    super(scope, id, props);

  }
}
