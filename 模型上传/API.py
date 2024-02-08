from flask import Flask, request, jsonify
import flask
import os
import shutil
app = Flask(__name__)
app.json.ensure_ascii = False  # 当前flask版本有效，给定json格式数据返回的时候，针对中文不进行编码处理
# 给定返回结果的时候，对象如何转换为json字符串；默认情况下，自定义对象是无法转换的；不同flask版本，最终解决代码可能不一样

model_root_dir = 'model'

@app.route("/uploader", methods=['POST'])
def uploader():
    """
    上传文件到服务器上
    :return:
    """
    _args = flask.request.values
    for c in ['name', 'version']:
        if c not in _args:
            return flask.jsonify({"code": 201, "msg": f"必须给定{c}参数!"})
    name = _args.get("name")#模型名称
    version = _args.get('version')#模型版本号
    sub_dirs = _args.get('sub_dir_names', '')  # 子文件夹的名称字符串列表，使用","分割开的一个字符串
    sub_dirs = [sub_dir.strip() for sub_dir in sub_dirs.split(",")]
    filename = _args.get("filename")  # 上传新的文件名称
    file = flask.request.files['file']  # 获取待上传的对象
    if filename is None:
        # 当没有给定上传文件重名称的时候，直接使用上传文件的原本名称
        filename = file.filename
    #给定的储存模型的文件夹+模型名称+模型版本+子文件夹
    _dir = os.path.join(model_root_dir, name, version, *sub_dirs)
    # 创建输出的_dir文件夹
    os.makedirs(_dir, exist_ok=True)
    #拼接出要保存的文件全路径
    save_path = os.path.join(_dir, filename)
    if os.path.exists(save_path):
        return flask.jsonify({
            "code": 202,
            "msg": f"文件路径已存在，请重新给定name、version和filename参数值，当前参数为:{name} -- {version} -- {filename}"
        })
    file.save(os.path.abspath(save_path))  # 保存操作
    return flask.jsonify({"code": 200, "name": name, "version": version, "filename": filename})

@app.route("/deleter", methods=['GET'])
def deleter():
    """
    删除服务器上的文件
    eg: s.get("http://127.0.0.1:9999/deleter", params={"version":version, "name":name})
    最终删除的文件是:
    {global_config.model_root_dir}/{name}/{version}
    :return:
    """
    _args = flask.request.values
    for c in ['name', 'version']:
        if c not in _args:
            return flask.jsonify({"code": 201, "msg": f"必须给定{c}参数!"})
    name = _args.get("name")
    version = _args.get('version')
    sub_dirs = _args.get('sub_dir_names', '')  # 子文件夹的名称字符串列表，使用","分割开的一个字符串
    sub_dirs = [sub_dir.strip() for sub_dir in sub_dirs.split(",")]

    _dir = os.path.join(model_root_dir, name, version, *sub_dirs)

    filename = _args.get("filename")
    if filename is None:
        # 删除文件夹
        _file = _dir
    else:
        # 删除的具体filename文件
        _file = os.path.join(_dir, filename)
    shutil.rmtree(_file)  # 删除操作
    return flask.jsonify({"code": 200, "msg": f"文件删除成功:{_file}"})