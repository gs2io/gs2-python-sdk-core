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

from gs2_core_client.model import OnetimeTokenGs2Credential


class OnetimeGs2Credential(OnetimeTokenGs2Credential):

    def __init__(self, onetime_token):
        """
        コンストラクタ
        :param onetime_token: ワンタイムトークン
        :type onetime_token: str
        """
        super(OnetimeGs2Credential, self).__init__(onetime_token)
