from gradio_client import Client

client = Client("http://10.80.8.154:30641/")

try:
    # 示例1: 使用情绪向量控制 - 快乐+平静的混合
    result = client.predict(
        emo_control_method="Use emotion vectors",  # 使用向量控制
        prompt=None,
        text="现在语音情感应该是快乐和平静的混合，适合轻松愉快的场景。让我们试一试",
        emo_ref_path=None,
        emo_weight=0.7,  # 提高情绪影响权重
        vec1=0.4,  # Happy
        vec2=0,  # Angry
        vec3=0,  # Sad
        vec4=0,  # Afraid
        vec5=0,  # Disgusted
        vec6=0,  # Melancholic
        vec7=0,  # Surprised
        vec8=0.3,  # Calm
        emo_text="cheerful and peaceful",  # 文本描述辅助
        emo_random=False,
        max_text_tokens_per_segment=480,
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
    print(f"合成成功:{result}")
except Exception as e:
    print(f"合成失败:{e}")
