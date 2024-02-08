# -*- coding: utf-8 -*-
import json
'''远程端调试：
    1.登录客户端地址+部署名称；
    2.获取密钥
    3.
'''

def invoke_local():
    pass


def invoke_remote():
    from eas_prediction import PredictClient
    from eas_prediction import StringRequest, StringResponse

    client = PredictClient('http://1360076292613174.cn-hangzhou.pai-eas.aliyuncs.com', 'test3_fanghao777')
    client.set_token('NTlkYTBiNTIzMGY2NDVjNzQ4ZmU5ODhkZTVhMGI5NTkxOGRmYTBlMQ==')
    client.init()

    request = StringRequest('1,2,3,4')
    for x in range(0, 10000):
        resp = client.predict(request)
        if x % 100 == 0:
            resp = str(resp.response_data, encoding='utf-8')
            resp = json.loads(resp)
            print(x, "\t\t\t", resp)

    client.destroy()


if __name__ == '__main__':
    # invoke_local()
    invoke_remote()
