import { aws_apigateway } from "aws-cdk-lib";
import { Construct } from 'constructs';
import { ResourceName } from './resource_name';
import { PostFunction } from './post_function';

export interface ApiProps {
  resourceName: ResourceName;
  postFunction: PostFunction;
}

export class Api extends Construct {

  constructor(scope: Construct, id: string, props: ApiProps) {
    super(scope, id);

    //==========================================================================
    // API Gatewayを作成
    const restApi = new aws_apigateway.RestApi(this, "rest-api", {
      restApiName: `${props.resourceName.systemName}-api`,
      deployOptions: {
        loggingLevel: aws_apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        metricsEnabled: true,
      },
    });

    //==========================================================================
    // /recipes APIを作成
    const recipes = restApi.root.addResource("recipes");

    //==========================================================================
    // APIのメソッドにLambda関数を統合

    // 新規レシピ登録関数をPOSTメソッドとして統合
    const postIntegration = new aws_apigateway.LambdaIntegration(
      props.postFunction.function
    );
    recipes.addMethod("POST", postIntegration);
  }
}
