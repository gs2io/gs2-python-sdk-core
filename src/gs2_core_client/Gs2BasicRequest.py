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


class Gs2BasicRequest(object):

    def __init__(self, params=None):
        """
        コンストラクタ
        :param params: 辞書配列形式のパラメータ初期値リスト
        :type params: dict|None
        """
        if params is None:
            self.__client_id = None
            self.__timestamp = None
            self.__request_sign = None
            self.__request_id = None
        else:
            client_id = params['X-GS2-CLIENT-ID'] if 'X-GS2-CLIENT-ID' in params.keys() else None
            if client_id is not None:
                self.__set_client_id(client_id)
            timestamp = params['X-GS2-TIMESTAMP'] if 'X-GS2-TIMESTAMP' in params.keys() else None
            if timestamp is not None:
                self.__set_timestamp(timestamp)
            request_sign = params['X-GS2-REQUEST-SIGN'] if 'X-GS2-REQUEST-SIGN' in params.keys() else None
            if request_sign is not None:
                self.__set_request_sign(request_sign)
            request_id = params['X-GS2-REQUEST-ID'] if 'X-GS2-REQUEST-ID' in params.keys() else None
            if request_id is not None:
                self.__set_request_id(request_id)

    def __get_client_id(self):
        """
        GS2 クライアントIDを設定
        :return: GS2 クライアントID
        :rtype: str
        """
        return self.__client_id

    def __set_client_id(self, client_id):
        """
        GS2 クライアントIDを設定
        :param client_id: GS2クライアントID
        :type client_id: str
        """
        if not isinstance(client_id, str) and not isinstance(client_id, unicode):
            raise TypeError()
        self.__client_id = client_id

    def __with_client_id(self, client_id):
        """
        GS2 クライアントIDを設定
        :param client_id: GS2クライアントID
        :type client_id: str
        """
        self.__set_client_id(client_id)
        return self

    def __get_timestamp(self):
        """
        リクエスト時刻を設定
        :return: リクエスト時刻
        :rtype: str
        """
        return self.__timestamp

    def __set_timestamp(self, timestamp):
        """
        リクエスト時刻を設定
        :param timestamp: リクエスト時刻
        :type timestamp: str
        """
        if not isinstance(timestamp, str) and not isinstance(timestamp, unicode):
            raise TypeError()
        self.__timestamp = timestamp

    def __with_timestamp(self, timestamp):
        """
        リクエスト時刻を設定
        :param timestamp: リクエスト時刻
        :type timestamp: str
        """
        self.__set_timestamp(timestamp)
        return self

    def __get_request_sign(self):
        """
        署名を設定
        :return: 署名
        :rtype: str
        """
        return self.__request_sign

    def __set_request_sign(self, request_sign):
        """
        署名を設定
        :param request_sign: 署名
        :type request_sign: str
        """
        if not isinstance(request_sign, str) and not isinstance(request_sign, unicode):
            raise TypeError()
        self.__request_sign = request_sign

    def __with_request_sign(self, request_sign):
        """
        署名を設定
        :param request_sign: 署名
        :type request_sign: str
        """
        self.__set_request_sign(request_sign)
        return self

    def get_request_id(self):
        """
        リクエストIDを設定
        :return: リクエストID
        :rtype: str
        """
        return self.__request_id

    def set_request_id(self, request_id):
        """
        リクエストIDを設定
        :param request_id: リクエストID
        :type request_id: str
        """
        if not isinstance(request_id, str) and not isinstance(request_id, unicode):
            raise TypeError()
        self.__request_id = request_id

    def with_request_id(self, request_id):
        """
        リクエストIDを設定
        :param request_id: リクエストID
        :type request_id: str
        """
        self.set_request_id(request_id)
        return self