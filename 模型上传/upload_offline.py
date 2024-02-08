import json
import requests
import torch
import os
import json
model_dir="fm"
def upload(model_dir):
    """
    将本地文件夹中的内容上传到服务器上
    :param model_dir: 本地待上传的文件夹路径
    :return:
    """
    base_url = "http://127.0.0.1:5051"
    name = 'fm'  # 当前必须为fm
    sess = requests.session()

    # 1. version信息恢复
    extra_files = {
        'model_version': ''
    }
    spu_net = torch.jit.load(os.path.join(model_dir, "spu_model.pt"), map_location='cpu', _extra_files=extra_files)
    spu_net.eval()
    #将读取的模型信息转化成字符串
    for k in extra_files:
        extra_files[k] = str(extra_files[k], encoding='utf-8')
    model_version = "fm_20240121_155900"
    extra_files['model_version'] = model_version
    print(extra_files)
    json.dump(dict(extra_files), open(os.path.join(model_dir, 'info.json'), 'w', encoding='utf-8'))
    model_version = extra_files['model_version']

    # 删除文件夹
    sess.get(f"{base_url}/deleter", params={"version": model_version, "name": name})

    # 2. 上传文件
    def upload_file(_f, pname=None, fname=None, sub_dir_names=None):
        data = {
            "version": model_version,
            "name": pname or name
        }
        if fname is not None:
            data['filename'] = fname
        if sub_dir_names is not None:
            data['sub_dir_names'] = sub_dir_names
        res1 = sess.post(
            url=f"{base_url}/uploader",
            data=data,
            files={
                "file": open(_f, 'rb')
            }
        )
        if res1.status_code == 200:
            _data = res1.json()
            if _data['code'] != 200:
                raise ValueError(f"上传文件失败，异常信息为:{_data['msg']}")
            else:
                print(f"上传成功，version:'{_data['version']}'，filename:'{_data['filename']}'")
        else:
            raise ValueError("网络异常!")
    #文件上传函数，用于上传指定文件路径的文件夹或者模型，_f表示待上传文件夹路径，pname表示
    def upload(_f, pname=None, fname=None, sub_dir_names=None):
        '''
        :param _f:给定需要上传本地文件路径（文件或者文件夹）
        :param pname:pname为模型名称（上传文件的父文件夹）
        :param fname: 上传后给定的新文件名称
        :param sub_dir_names:
        :return:
        '''
        #如果路径给定的是一个文件，则直接进行操作
        if os.path.isfile(_f):
            upload_file(_f, pname, fname, sub_dir_names)
        #如果路径给定的是一个文件夹，则上传文件夹中的所有文件
        else:
            #1.获取当前文件夹名
            cur_dir_name = os.path.basename(_f)
            #选择外部给定的名称，或者当前自身的名称
            fname = fname or cur_dir_name
            #保存文件读取的路径，保证文件夹结构的完整
            if sub_dir_names is None:
                sub_dir_names = f"{fname}"
            else:
                sub_dir_names = f"{sub_dir_names},{fname}"
            # 子文件的处理
            for _name in os.listdir(_f):
                upload(
                    _f=os.path.join(_f, _name),
                    pname=pname,
                    fname=None,  # 子文件无法重命名
                    sub_dir_names=sub_dir_names
                )

    upload(_f=os.path.join(model_dir, "model.pt"))
    upload(_f=os.path.join(model_dir, "spu_model.pt"))
    upload(_f=os.path.join(model_dir, "user_model.pt"))
    upload(_f=os.path.join(model_dir, "spu_embedding.npz"))
    upload(_f=os.path.join(model_dir, "dict"))
    upload(_f=os.path.join(model_dir, "info.json"))
upload(model_dir)
