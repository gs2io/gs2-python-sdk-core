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

from gs2_core_client.model.RequestError import RequestError


class Gs2Exception(IOError):

    def __init__(self, message):
        super(Gs2Exception, self).__init__(message)

        self.__errors = []

        errors = None

        try:
            import json
            _ = json.loads(message)
            if isinstance(_, dict):
                errors = json.loads(_['message'])
        except ValueError:
            pass

        if isinstance(errors, list):
            for error in errors:
                if isinstance(error, dict):
                    try:
                        self.__errors.append(RequestError(component=error['component'], message=error['message']))
                    except ValueError:
                        pass

    def get_errors(self):
        """
        エラー一覧を取得する
        :return: エラー一覧
        :rtype: list[RequestError]
        """
        return self.__errors

    def __getitem__(self, key):
        if key == 'errors':
            return self.get_errors()
        return super(object, self).__getitem__(key)

    def get(self, key, default=None):
        if key == 'errors':
            return self.get_errors()
        try:
            return super(object, self).__getitem__(key)
        except ValueError:
            return default
