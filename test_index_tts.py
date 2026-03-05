"""Test script for IndexTTS integration.

This script demonstrates how to use the IndexTTS TTS engine through the TTSFactory.
"""

from src.open_llm_vtuber.tts.tts_factory import TTSFactory

# Example 1: Using IndexTTS via TTSFactory with default parameters
print("🚀 Testing IndexTTS integration...\n")

# Create an IndexTTS instance with default settings
tts_engine = TTSFactory.get_tts_engine(
    "index_tts",
    api_url="http://10.80.8.154:30413/",
    emo_control_method="Same as the voice reference",
    prompt=None,
    emo_ref_path=None,
    emo_weight=0.65,
)

print(f"✅ IndexTTS engine created successfully!")
print(f"Engine type: {type(tts_engine)}")
print(f"API URL: {tts_engine.api_url}")
print(f"Emotion Control Method: {tts_engine.emo_control_method}")
print(f"Emotion Weight: {tts_engine.emo_weight}")

# Example 2: Generate audio with default settings
print("\n📝 Generating audio with default settings...\n")

try:
    result = tts_engine.generate_audio("Hello, this is a test of IndexTTS.")
    if result:
        print(f"✅ Audio generated successfully: {result}")
    else:
        print("❌ Failed to generate audio")
except Exception as e:
    print(f"❌ Error during audio generation: {e}")

# Example 3: Create engine with custom emotion parameters
print("\n🎨 Testing with custom emotion vector parameters...\n")

tts_engine_custom = TTSFactory.get_tts_engine(
    "index_tts",
    api_url="http://10.80.8.154:30413/",
    emo_control_method="Same as the voice reference",
    emo_weight=0.8,
    vec1=5,
    vec2=3,
    vec3=2,
    vec4=1,
    vec5=0,
    vec6=0,
    vec7=0,
    vec8=0,
)

print(f"✅ Custom IndexTTS engine created!")
print(f"Emotion Weight: {tts_engine_custom.emo_weight}")
print(f"Emotion Vectors: vec1={tts_engine_custom.vec1}, vec2={tts_engine_custom.vec2}")

try:
    result = tts_engine_custom.generate_audio(
        "This is a test with custom emotion vectors."
    )
    if result:
        print(f"✅ Audio generated successfully: {result}")
    else:
        print("❌ Failed to generate audio")
except Exception as e:
    print(f"❌ Error during audio generation: {e}")

print("\n✨ All tests completed!")
