import { aws_apigateway } from "aws-cdk-lib";
import { Construct } from 'constructs';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';

import { ResourceName } from './resource_name';
import { PostFunction } from './post_function';
import { PatchFunction } from './patch_function';
import { DeleteFunction } from './delete_function';

export interface ApiProps {
  resourceName: ResourceName;
  postFunction: PostFunction;
  patchFunction: PatchFunction;
  deleteFunction: DeleteFunction;
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
    restApi.addGatewayResponse('gateway-response', {
      type: apigateway.ResponseType.DEFAULT_4XX,
      statusCode: '404',
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

    // 既存レシピ更新関数をPATCHメソッドとして統合
    const patchIntegration = new aws_apigateway.LambdaIntegration(
      props.patchFunction.function
    );
    recipes.addMethod("PATCH", patchIntegration);

    // 既存レシピ削除関数をPATCHメソッドとして統合
    const deleteIntegration = new aws_apigateway.LambdaIntegration(
      props.deleteFunction.function
    );
    recipes.addMethod("DELETE", deleteIntegration);
  }
}
