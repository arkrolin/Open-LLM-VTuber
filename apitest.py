from gradio_client import Client

client = Client("http://10.80.8.154:30413/")

try:
    result = client.predict(
        emo_control_method="Same as the voice reference",
        prompt=None,
        text="Hello!!",
        emo_ref_path=None,
        emo_weight=0.65,
        vec1=0,
        vec2=0,
        vec3=0,
        vec4=0,
        vec5=0,
        vec6=0,
        vec7=0,
        vec8=0,
        emo_text="",
        emo_random=False,
        max_text_tokens_per_segment=120,
        param_16=True,
        param_17=0.8,
        param_18=30,
        param_19=0.8,
        param_20=0,
        param_21=3,
        param_22=10,
        param_23=1500,
        api_name="/gen_single",
    )
    print(f"合成成功：{result}")
except Exception as e:
    print(f"合成失败：{e}")
