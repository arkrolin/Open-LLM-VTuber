from gradio_client import Client

client = Client("http://10.80.8.154:30413/")

try:
    result = client.predict(
        "Same as the voice reference",  # 情感模式直接传数字 0 最稳妥
        None,  # prompt 传 None，触发后端默认 bingzhi.wav
        "你好，我是兵智。这次变量未定义的错误已经修复了，我们可以正常通话了。",
        None,  # emo_ref_path
        0.65,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        "",
        False,
        120,
        True,
        0.8,
        30,
        0.8,
        0,
        3,
        10,
        1500,
        api_name="/gen_single",
    )
    print(f"合成成功：{result}")
except Exception as e:
    print(f"合成失败：{e}")
