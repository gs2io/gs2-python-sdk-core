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

from gs2_core_client.Gs2BasicRequest import Gs2BasicRequest


class Gs2UserRequest(Gs2BasicRequest):

    def __init__(self, params=None):
        """
        コンストラクタ
        :param params: 辞書配列形式のパラメータ初期値リスト
        :type params: dict|None
        """
        super(Gs2UserRequest, self).__init__(params)
        if params is None:
            self.__access_token = None
        else:
            self.set_access_token(params['X-GS2-ACCESS-TOKEN'] if 'X-GS2-ACCESS-TOKEN' in params.keys() else None)

    def get_access_token(self):
        """
        GS2 クライアントIDを設定
        :return: GS2 クライアントID
        :rtype: unicode
        """
        return self.__access_token

    def set_access_token(self, access_token):
        """
        GS2 クライアントIDを設定
        :param access_token: GS2クライアントID
        :type access_token: unicode
        """
        if not isinstance(access_token, str) and not isinstance(access_token, unicode) and access_token is not None:
            raise TypeError()
        self.__access_token = access_token

    def with_access_token(self, access_token):
        """
        GS2 クライアントIDを設定
        :param access_token: GS2クライアントID
        :type access_token: unicode
        """
        self.set_access_token(access_token)
        return self
