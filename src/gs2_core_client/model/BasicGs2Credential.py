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

import base64
import hashlib
import hmac

from gs2_core_client.model.IGs2Credential import IGs2Credential


class BasicGs2Credential(IGs2Credential):

    def __init__(self, client_id, client_secret):
        """
        コンストラクタ
        :param client_id: クライアントID
        :type client_id: str
        :param client_secret: クライアントシークレット
        :type client_secret: str
        """
        super(IGs2Credential, self).__init__()
        self.__client_id = client_id
        self.__client_secret = client_secret

    def authorized(self, module, function, headers, timestamp):
        """
        認証処理
        :param module: モジュール名
        :type module: str
        :param function: ファンクション名
        :type function: str
        :param headers: リクエストヘッダ
        :type headers: dict
        :param timestamp: リクエスト時間
        :type timestamp: int
        """
        headers['X-GS2-CLIENT-ID'] = self.__client_id
        headers['X-GS2-REQUEST-TIMESTAMP'] = str(timestamp)
        headers['X-GS2-REQUEST-SIGN'] = base64.b64encode(
            hmac.new(
                base64.b64decode(self.__client_secret),
                module + ":" + function + ":" + str(timestamp),
                hashlib.sha256
            ).digest())