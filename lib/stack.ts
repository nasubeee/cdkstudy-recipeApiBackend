import { Stack, StackProps, RemovalPolicy } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

import { ResourceName } from './resource_name';
import { PostFunction } from './post_function';
import { Api } from './api';

export interface RecipeAPIStackProps extends StackProps {
  resourceName: ResourceName;
}

export class RecipeAPIStack extends Stack {
  public recipeDynamoTable: dynamodb.Table;
  public api: Api;

  constructor(scope: Construct, id: string, props: RecipeAPIStackProps) {
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
    });

    //==========================================================================
    // 新規レシピを登録するLambda Functionを作成する
    const postFunction = new PostFunction(this, `post-function`, {
      resourceName: props.resourceName,
      table: this.recipeDynamoTable
    });

    //==========================================================================
    // API Gatewayを作成する
    this.api = new Api(this, `api`, {
      resourceName: props.resourceName,
      postFunction: postFunction,
    });
  }
}
