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


class RequestError(object):

    def __init__(self, component, message):
        """
        コンストラクタ
        :param component: コンポーネント
        :type component: unicode
        :param message: メッセージ
        :type message: unicode
        """
        self.__component = component
        self.__message = message

    def get_component(self):
        """
        コンポーネントを取得する
        :return: コンポーネント
        :rtype: unicode
        """
        return self.__component
    
    def get_message(self):
        """
        メッセージを取得する
        :return: メッセージ
        :rtype: unicode
        """
        return self.__message

    def __getitem__(self, key):
        if key == 'component':
            return self.get_component()
        if key == 'message':
            return self.get_message()
        return super(object, self).__getitem__(key)

    def get(self, key, default=None):
        if key == 'component':
            return self.get_component()
        if key == 'message':
            return self.get_message()
        try:
            return super(object, self).__getitem__(key)
        except ValueError:
            return default
