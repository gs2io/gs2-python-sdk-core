# encoding: utf-8
#
# Copyright 2016 Game Server Services, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from abc import ABCMeta


class AbstractGs2Client(object):
    __metaclass__ = ABCMeta

    def __init__(self, credential, region):
        """
        コンストラクタ
        :param credential: 認証情報
        :type credential: gs2_core_client.model.IGs2Credential.IGs2Credential
        :param region: GS2リージョン
        :type region: str
        """
        self.__credential = credential
        self.__region = region

    def __parse_response(self, response):
        """
        HTTPレスポンスをパースする
        :param response: HTTPレスポンス
        :type response: requests.models.Response
        :return: レスポンス
        :rtype: dict
        """
        try:
            import json
            if response.status_code == 200:
                return json.loads(response.text)
            if response.status_code == 400:
                from gs2_core_client.exception.BadRequestException import BadRequestException
                raise BadRequestException(json.loads(response.text)['message'])
            if response.status_code == 401:
                from gs2_core_client.exception.UnauthorizedException import UnauthorizedException
                raise UnauthorizedException(json.loads(response.text)['message'])
            if response.status_code == 402:
                from gs2_core_client.exception.QuotaExceedException import QuotaExceedException
                raise QuotaExceedException(json.loads(response.text)['message'])
            if response.status_code == 404:
                from gs2_core_client.exception.NotFoundException import NotFoundException
                raise NotFoundException(json.loads(response.text)['message'])
            if response.status_code == 409:
                from gs2_core_client.exception.ConflictException import ConflictException
                raise ConflictException(json.loads(response.text)['message'])
            if response.status_code == 500:
                from gs2_core_client.exception.InternalServerErrorException import InternalServerErrorException
                raise InternalServerErrorException(json.loads(response.text)['message'])
            if response.status_code == 502:
                from gs2_core_client.exception.BadGatewayException import BadGatewayException
                raise BadGatewayException(json.loads(response.text)['message'])
            if response.status_code == 503:
                from gs2_core_client.exception.ServiceUnavailableException import ServiceUnavailableException
                raise ServiceUnavailableException('')
            if response.status_code == 504:
                from gs2_core_client.exception.RequestTimeoutException import RequestTimeoutException
                raise RequestTimeoutException(json.loads(response.text)['message'])
        except ValueError:
            pass
        raise RuntimeError('[' + str(response.status_code) + '] ' + str(response.text))

    def _do_get_request(self, url, service, module, function, query_strings, headers):
        """
        GETリクエストを発行する
        :param url: URL
        :type url: unicode
        :param service: サービス名
        :type service: str
        :param module: モジュール名
        :type module: str
        :param function: ファンクション名
        :type function: str
        :param query_strings: クエリストリング
        :type query_strings: dict
        :param headers: リクエストヘッダ
        :type headers: dict
        :return: レスポンス
        :rtype: dict
        """
        import time
        import requests

        self.__credential.authorized(
            module=module,
            function=function,
            headers=headers,
            timestamp=int(time.time())
        )

        response = requests.get(
            url=url.replace('{service}', service).replace('{region}', self.__region),
            params=query_strings,
            headers=headers
        )

        return self.__parse_response(response)

    def _do_post_request(self, url, service, module, function, body, headers):
        """
        POSTリクエストを発行する
        :param url: URL
        :type url: unicode
        :param service: サービス名
        :type service: str
        :param module: モジュール名
        :type module: str
        :param function: ファンクション名
        :type function: str
        :param body: POST Body
        :type body: dict
        :param headers: リクエストヘッダ
        :type headers: dict
        :return: レスポンス
        :rtype: dict
        """
        import time
        import requests

        self.__credential.authorized(
            module=module,
            function=function,
            headers=headers,
            timestamp=int(time.time())
        )

        response = requests.post(
            url=url.replace('{service}', service).replace('{region}', self.__region),
            json=body,
            headers=headers
        )

        return self.__parse_response(response)

    def _do_put_request(self, url, service, module, function, body, headers):
        """
        PUTリクエストを発行する
        :param url: URL
        :type url: unicode
        :param service: サービス名
        :type service: str
        :param module: モジュール名
        :type module: str
        :param function: ファンクション名
        :type function: str
        :param body: POST Body
        :type body: dict
        :param headers: リクエストヘッダ
        :type headers: dict
        :return: レスポンス
        :rtype: dict
        """
        import time
        import requests

        self.__credential.authorized(
            module=module,
            function=function,
            headers=headers,
            timestamp=int(time.time())
        )

        response = requests.put(
            url=url.replace('{service}', service).replace('{region}', self.__region),
            json=body,
            headers=headers
        )

        return self.__parse_response(response)

    def _do_delete_request(self, url, service, module, function, query_strings, headers):
        """
        DELETEリクエストを発行する
        :param url: URL
        :type url: unicode
        :param service: サービス名
        :type service: str
        :param module: モジュール名
        :type module: str
        :param function: ファンクション名
        :type function: str
        :param query_strings: クエリストリング
        :type query_strings: dict
        :param headers: リクエストヘッダ
        :type headers: dict
        :return: レスポンス
        :rtype: dict
        """
        import time
        import requests

        self.__credential.authorized(
            module=module,
            function=function,
            headers=headers,
            timestamp=int(time.time())
        )

        response = requests.delete(
            url=url.replace('{service}', service).replace('{region}', self.__region),
            params=query_strings,
            headers=headers
        )

        return self.__parse_response(response)
