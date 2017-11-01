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

from abc import abstractmethod


class IGs2Credential(object):

    @abstractmethod
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
        pass