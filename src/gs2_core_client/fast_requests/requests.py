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


class HttpResponse(object):
    def __init__(self, status_code, headers, body):
        """
        HTTPレスポンス
        :param status_code: ステータスコード
        :type status_code: int
        :param headers: レスポンスヘッダ
        :type headers: dict
        :param body: レスポンスボディ
        :type body: unicode
        """
        self.__status_code = status_code
        self.__headers = headers
        self.__body = body

    @property
    def status_code(self):
        """
        ステータスコードを取得
        :return: ステータスコード
        :rtype: int
        """
        return self.__status_code

    @property
    def headers(self):
        """
        レスポンスヘッダを取得
        :return: レスポンスヘッダ
        :rtype: dict
        """
        return self.__headers

    @property
    def text(self):
        """
        レスポンスボディを取得
        :return: レスポンスボディ
        :rtype: unicode
        """
        return self.__body


def _get_protocol(url):
    """
    URLからプロトコルを取り出す
    :param url: URL
    :type url: str
    :return: プロトコル
    :rtype: str
    """
    return url[:url.find('://')]


def _get_host(url):
    """
    URLからホスト名を取り出す
    :param url: URL
    :type url: str
    :return: ホスト名
    :rtype: str
    """
    url_without_protocol = url[len(_get_protocol(url)) + 3:]
    colon_pos = url_without_protocol.find(':')
    slash_pos = url_without_protocol.find('/')
    question_pos = url_without_protocol.find('?')
    if colon_pos == -1 and slash_pos == -1 and question_pos == -1:
        return url_without_protocol
    elif colon_pos > -1 and slash_pos == -1 and question_pos == -1:
        return url_without_protocol[:colon_pos]
    elif colon_pos == -1 and slash_pos > -1:
        return url_without_protocol[:slash_pos]
    elif colon_pos == -1 and question_pos > -1:
        return url_without_protocol[:question_pos]
    elif colon_pos < slash_pos:
        return url_without_protocol[:colon_pos]
    elif colon_pos < question_pos:
        return url_without_protocol[:colon_pos]
    else:
        if slash_pos == -1:
            return url_without_protocol[:question_pos]
        else:
            return url_without_protocol[:slash_pos]


def _get_port(url):
    """
    URLからポート番号を取り出す
    :param url: URL
    :type url: str
    :return: ポート番号
    :rtype: int
    """
    url_without_protocol = url[len(_get_protocol(url)) + 3:]
    colon_pos = url_without_protocol.find(':')
    if colon_pos == -1:
        if _get_protocol(url) == 'http':
            return 80
        if _get_protocol(url) == 'https':
            return 443
    slash_pos = url_without_protocol.find('/')
    if slash_pos == -1:
        return int(url_without_protocol[colon_pos + 1:])
    return int(url_without_protocol[colon_pos + 1:slash_pos])


def _to_query_string(query_strings):
    """
    辞書配列からクエリストリングに変換
    :param query_strings: クエリストリング(辞書配列)
    :type query_strings: dict
    :return: クエリストリング(文字列)
    :rtype: unicode
    """
    from aws_sdk_for_serverless.common import url_encoder
    return '&'.join(
        map(lambda key: '{key}={value}'.format(
            key=key,
            value=url_encoder.encode(query_strings[key]),
        ), query_strings.keys())
    )


_connection_pool = {}


def _get_cache_key(url):
    protocol = _get_protocol(url)
    host = _get_host(url)
    port = _get_port(url)

    key = '{protocol}://{host}:{port}'.format(
        protocol=protocol,
        host=host,
        port=port,
    )

    return key


def _create_connection(url, timeout):
    """
    HTTPコネクションを作成する
    :param url: URL
    :type url: str
    :param timeout: タイムアウト時間(秒)
    :type timeout: float
    :return: (str, str, int)
    """
    import httplib

    protocol = _get_protocol(url)
    host = _get_host(url)
    port = _get_port(url)

    key = _get_cache_key(url)
    if key in _connection_pool.keys():
        return _connection_pool[key]

    if protocol == 'http':
        _connection_pool[key] = httplib.HTTPConnection(
            host,
            port=port,
            timeout=timeout,
        )
        return _connection_pool[key]
    elif protocol == 'https':
        _connection_pool[key] = httplib.HTTPSConnection(
            host,
            port=port,
            timeout=timeout,
        )
        return _connection_pool[key]
    else:
        raise AttributeError('invalid protocol')


def _purge_connection_cache(url):
    key = _get_cache_key(url)
    if key in _connection_pool.keys():
        del _connection_pool[key]


def get(
        url,
        params=None,
        headers=None,
        timeout=60,
):
    """
    GETリクエストを発行する
    :param url: URL
    :type url: str or unicode
    :param params: クエリストリング
    :type params: dict
    :param headers: リクエストヘッダ
    :type headers: dict
    :param timeout: タイムアウト時間(秒)
    :type timeout: float
    :return: レスポンス
    :rtype: HttpResponse
    """
    import socket
    from httplib import HTTPException

    if params is None:
        params = {}
    if headers is None:
        headers = {}

    if url.count('/') < 3:
        url += '/'
    host = _get_host(url)

    headers['Host'] = host
    headers['Connection'] = 'Keep-Alive'

    if params:
        url = '{url}?{query_strings}'.format(
            url=url,
            query_strings=_to_query_string(params),
        )

    exception = None
    for _ in range(3):
        connection = _create_connection(
            url=url,
            timeout=timeout,
        )
        try:
            connection.request(
                method='GET',
                url=url,
                headers=headers,
            )
            response = connection.getresponse()
            result = response.read()
            try:
                result = result.encode('utf-8')
            except UnicodeDecodeError:
                pass
            return HttpResponse(
                status_code=response.status,
                headers=dict(response.getheaders()),
                body=result
            )
        except (HTTPException, socket.error) as e:
            _purge_connection_cache(url)
            exception = e

    if exception is not None:
        raise exception


def post(
        url,
        params=None,
        headers=None,
        data=None,
        json=None,
        timeout=60,
):
    """
    POSTリクエストを発行する
    :param url: URL
    :type url: str or unicode
    :param params: クエリストリング
    :type params: dict
    :param headers: リクエストヘッダ
    :type headers: dict
    :param data: リクエストボディ(バイナリ)
    :type data: bytes
    :param json: リクエストボディ(dict)
    :type json: dict
    :param timeout: タイムアウト時間(秒)
    :type timeout: float
    :return: レスポンス
    :rtype: HttpResponse
    """
    import socket
    from httplib import HTTPException
    import simplejson

    if params is None:
        params = {}
    if headers is None:
        headers = {}
    if json is not None:
        data = simplejson.dumps(json)
    if data is None:
        data = ''

    if url.count('/') < 3:
        url += '/'
    host = _get_host(url)

    headers['Host'] = host
    headers['Connection'] = 'Keep-Alive'

    if params:
        url = '{url}?{query_strings}'.format(
            url=url,
            query_strings=_to_query_string(params),
        )

    exception = None
    for _ in range(3):
        connection = _create_connection(
            url=url,
            timeout=timeout,
        )
        try:
            connection.request(
                method='POST',
                url=url,
                headers=headers,
                body=data,
            )
            response = connection.getresponse()
            result = response.read()
            try:
                result = result.encode('utf-8')
            except UnicodeDecodeError:
                pass
            return HttpResponse(
                status_code=response.status,
                headers=dict(response.getheaders()),
                body=result
            )
        except (HTTPException, socket.error) as e:
            _purge_connection_cache(url)
            exception = e

    if exception is not None:
        raise exception


def put(
        url,
        params=None,
        headers=None,
        data=None,
        json=None,
        timeout=60,
):
    """
    POSTリクエストを発行する
    :param url: URL
    :type url: str or unicode
    :param params: クエリストリング
    :type params: dict
    :param headers: リクエストヘッダ
    :type headers: dict
    :param data: リクエストボディ(バイナリ)
    :type data: bytes
    :param json: リクエストボディ(dict)
    :type json: dict
    :param timeout: タイムアウト時間(秒)
    :type timeout: float
    :return: レスポンス
    :rtype: HttpResponse
    """
    import socket
    from httplib import HTTPException
    import simplejson

    if params is None:
        params = {}
    if headers is None:
        headers = {}
    if json is not None:
        data = simplejson.dumps(json)
    if data is None:
        data = ''

    if url.count('/') < 3:
        url += '/'
    host = _get_host(url)

    headers['Host'] = host
    headers['Connection'] = 'Keep-Alive'

    if params:
        url = '{url}?{query_strings}'.format(
            url=url,
            query_strings=_to_query_string(params),
        )

    exception = None
    for _ in range(3):
        connection = _create_connection(
            url=url,
            timeout=timeout,
        )
        try:
            connection.request(
                method='PUT',
                url=url,
                headers=headers,
                body=data,
            )
            response = connection.getresponse()
            result = response.read()
            try:
                result = result.encode('utf-8')
            except UnicodeDecodeError:
                pass
            return HttpResponse(
                status_code=response.status,
                headers=dict(response.getheaders()),
                body=result
            )
        except (HTTPException, socket.error) as e:
            _purge_connection_cache(url)
            exception = e

    if exception is not None:
        raise exception


def delete(
        url,
        params=None,
        headers=None,
        timeout=60,
):
    """
    DELETEリクエストを発行する
    :param url: URL
    :type url: str or unicode
    :param params: クエリストリング
    :type params: dict
    :param headers: リクエストヘッダ
    :type headers: dict
    :param timeout: タイムアウト時間(秒)
    :type timeout: float
    :return: レスポンス
    :rtype: HttpResponse
    """
    import socket
    from httplib import HTTPException

    if params is None:
        params = {}
    if headers is None:
        headers = {}

    if url.count('/') < 3:
        url += '/'
    host = _get_host(url)

    headers['Host'] = host
    headers['Connection'] = 'Keep-Alive'

    if params:
        url = '{url}?{query_strings}'.format(
            url=url,
            query_strings=_to_query_string(params),
        )

    exception = None
    for _ in range(3):
        connection = _create_connection(
            url=url,
            timeout=timeout,
        )
        try:
            connection.request(
                method='DELETE',
                url=url,
                headers=headers,
            )
            response = connection.getresponse()
            result = response.read()
            try:
                result = result.encode('utf-8')
            except UnicodeDecodeError:
                pass
            return HttpResponse(
                status_code=response.status,
                headers=dict(response.getheaders()),
                body=result
            )
        except (HTTPException, socket.error) as e:
            _purge_connection_cache(url)
            exception = e

    if exception is not None:
        raise exception
