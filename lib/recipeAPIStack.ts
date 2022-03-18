import { Stack, StackProps, RemovalPolicy } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ResourceName } from '../lib/resource_name';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export interface ToDoAPIStackProps extends StackProps {
  resourceName: ResourceName;
}

export class recipeAPIStack extends Stack {
  public recipeDynamoTable: dynamodb.Table;

  constructor(scope: Construct, id: string, props: ToDoAPIStackProps) {
    super(scope, id, props);

    //==========================================================================
    // レシピ情報を格納するDynamoDBテーブルを作成
    this.recipeDynamoTable = new dynamodb.Table(this, `recipe-dynamo-table`, {
      tableName: props.resourceName.tableName(`recipe-data`),
      removalPolicy: RemovalPolicy.DESTROY, // 今回はスタック削除時にテーブルも削除
      partitionKey: {
        name: "id",
        type: dynamodb.AttributeType.STRING,
      },
      sortKey: {
        name: "itemId",
        type: dynamodb.AttributeType.STRING,
      }
    });

  }
}
