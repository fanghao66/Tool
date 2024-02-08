# -*- coding: utf-8 -*-
import json
import logging
import os
import sys

# 将当前文件pai_app.py所在的文件夹添加到sys.path环境变量中
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import allspark


class MyProcessor(allspark.BaseProcessor):
    """ MyProcessor is a example
        you can send mesage like this to predict
        curl -v http://127.0.0.1:8080/api/predict/service_name -d '2 105'
    """

    def initialize(self):
        """
        仅初始化的时候调用，并且仅调用一次
        """
        print("开始模型初始化....")

        from model import Predictor

        model_dir = "../../model"  # 这个路径是一个固定的写法
        model_path = os.path.join(model_dir, 'model.pt')
        self.predictor = Predictor(model_path=model_path)

    def post_process(self, data):
        """ process after process
        """
        return bytes(data, encoding='utf8')

    def process(self, data):
        """ process the request data
        """
        try:
            print(f"每次调用服务接口均会执行该方法:{data}")
            data = str(data, encoding='utf-8')
            # 2. 调用模型
            result = self.predictor.predict(data)
            # 3. 拼接结果返回
            result = {
                'code': 200,
                'msg': '成功',
                'data': {
                    'x': data,
                    'y': result
                }
            }
        except Exception as e:
            logging.error("服务器异常", exc_info=e)
            result = {
                'code': 201,
                'msg': f'服务器异常:{e}'
            }

        # 4. 转换成结果字符串
        result = json.dumps(result, ensure_ascii=False)
        print(f"模型预测结果为:{result}")
        # 5. 结果返回
        return self.post_process(result), 200


if __name__ == '__main__':
    # parameter worker_threads indicates concurrency of processing
    runner = MyProcessor(worker_threads=10)
    runner.run()
