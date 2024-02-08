# -*- coding: utf-8 -*-
import torch


class Predictor(object):
    def __init__(self, model_path):
        super(Predictor, self).__init__()
        self.model = torch.jit.load(model_path, map_location='cpu')
        self.model.eval()
        print(f"模型:{model_path}恢复成功!")

    @torch.no_grad()
    def predict(self, x: str) -> float:
        """
        针对给定的数据进行前向的预测过程
        NOTE: 每个样本一定是4维的特征，模型输出一定是一个数字
        :param x: 一个样本的4维特征组成的字符串，以符号","隔开，eg: 25,3.2,12.2,23.5
        :return: 预测的数字
        """
        print(f"输入数据:{x}")
        # 1. 入参数据解析
        arr = x.split(",")
        if len(arr) != 4:
            raise ValueError(f"入参异常，请给定以逗号隔开的四个数字，当前入参为:{x}")
        features = list(map(float, arr))

        # 2. 调用模型
        result = self.model(torch.tensor([features], dtype=torch.float32))  # [1,1]
        result = result[0][0].item()

        # 3. 结果返回
        return float(result)
