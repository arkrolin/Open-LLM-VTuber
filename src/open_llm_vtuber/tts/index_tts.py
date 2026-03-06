"""IndexTTS text-to-speech engine implementation.

This module provides a TTS implementation using the IndexTTS Gradio API.
It communicates with an IndexTTS server via gradio_client.
"""

from loguru import logger
from gradio_client import Client

from .tts_interface import TTSInterface


class IndexTTS(TTSInterface):
    """IndexTTS engine for text-to-speech synthesis via Gradio API.

    This class implements the TTSInterface for IndexTTS, a voice synthesis
    system that communicates through Gradio's client API.
    """

    def __init__(
        self,
        api_url: str,
        emo_control_method: str = "Same as the voice reference",
        prompt: str | None = None,
        emo_ref_path: str | None = None,
        emo_weight: float = 0.65,
        vec1: float = 0,
        vec2: float = 0,
        vec3: float = 0,
        vec4: float = 0,
        vec5: float = 0,
        vec6: float = 0,
        vec7: float = 0,
        vec8: float = 0,
        emo_text: str = "",
        emo_random: bool = False,
        max_text_tokens_per_segment: int = 120,
        param_16: bool = True,
        param_17: float = 0.8,
        param_18: int = 30,
        param_19: float = 0.8,
        param_20: int = 0,
        param_21: int = 3,
        param_22: int = 10,
        param_23: int = 1500,
        api_name: str = "/gen_single",
    ):
        """Initialize IndexTTS engine.

        Args:
            api_url (str): URL of the IndexTTS Gradio API server
                (e.g., "http://10.80.8.154:30413/").
            emo_control_method (str): Emotion control method. Defaults to
                "Same as the voice reference".
            prompt (str | None): Prompt audio file path. Defaults to None.
            emo_ref_path (str | None): Emotion reference audio path.
                Defaults to None.
            emo_weight (float): Emotion weight. Defaults to 0.65.
            vec1-vec8 (int): Emotion vector parameters. Defaults to 0.
            emo_text (str): Emotion text description. Defaults to "".
            emo_random (bool): Enable random emotion variation. Defaults to False.
            max_text_tokens_per_segment (int): Maximum text tokens per segment.
                Defaults to 120.
            param_16 (bool): Parameter 16. Defaults to True.
            param_17 (float): Parameter 17. Defaults to 0.8.
            param_18 (int): Parameter 18. Defaults to 30.
            param_19 (float): Parameter 19. Defaults to 0.8.
            param_20 (int): Parameter 20. Defaults to 0.
            param_21 (int): Parameter 21. Defaults to 3.
            param_22 (int): Parameter 22. Defaults to 10.
            param_23 (int): Parameter 23. Defaults to 1500.
            api_name (str): The Gradio API endpoint name. Defaults to "/gen_single".
        """
        self.api_url = api_url
        self.emo_control_method = emo_control_method
        self.prompt = prompt
        self.emo_ref_path = emo_ref_path
        self.emo_weight = emo_weight
        self.vec1 = vec1
        self.vec2 = vec2
        self.vec3 = vec3
        self.vec4 = vec4
        self.vec5 = vec5
        self.vec6 = vec6
        self.vec7 = vec7
        self.vec8 = vec8
        self.emo_text = emo_text
        self.emo_random = emo_random
        self.max_text_tokens_per_segment = max_text_tokens_per_segment
        self.param_16 = param_16
        self.param_17 = param_17
        self.param_18 = param_18
        self.param_19 = param_19
        self.param_20 = param_20
        self.param_21 = param_21
        self.param_22 = param_22
        self.param_23 = param_23
        self.api_name = api_name

        try:
            self.client = Client(api_url)
            logger.info(f"✅ IndexTTS client initialized with URL: {api_url}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize IndexTTS client: {e}")
            raise

    def generate_audio(self, text: str, file_name_no_ext: str | None = None) -> str:
        """Generate speech audio file from text using IndexTTS.

        Args:
            text (str): The text to synthesize into speech.
            file_name_no_ext (str | None): Name for the output file without
                extension. If None, uses "temp". Defaults to None.

        Returns:
            str: Path to the generated audio file. Returns empty string on failure.
        """
        cache_file = self.generate_cache_file_name(
            file_name_no_ext, file_extension="wav"
        )

        try:
            if not self.api_url:
                logger.error("❌ API URL not configured. Check configuration file.")
                return ""

            logger.debug(f"🔊 Generating audio with IndexTTS for text: {text[:50]}...")

            # Call the Gradio API with the configured parameters
            result = self.client.predict(
                emo_control_method=self.emo_control_method,
                prompt=self.prompt,
                text=text,
                emo_ref_path=self.emo_ref_path,
                emo_weight=self.emo_weight,
                vec1=self.vec1,
                vec2=self.vec2,
                vec3=self.vec3,
                vec4=self.vec4,
                vec5=self.vec5,
                vec6=self.vec6,
                vec7=self.vec7,
                vec8=self.vec8,
                emo_text=self.emo_text,
                emo_random=self.emo_random,
                max_text_tokens_per_segment=self.max_text_tokens_per_segment,
                param_16=self.param_16,
                param_17=self.param_17,
                param_18=self.param_18,
                param_19=self.param_19,
                param_20=self.param_20,
                param_21=self.param_21,
                param_22=self.param_22,
                param_23=self.param_23,
                api_name=self.api_name,
            )

            # Handle different response formats from Gradio API
            source_file = None
            if isinstance(result, dict) and "value" in result:
                # Gradio returns a dict with 'value' key containing the file path
                source_file = result["value"]
                logger.debug(
                    f"📦 Gradio returned dict format, extracted path: {source_file}"
                )
            elif isinstance(result, str):
                # Direct string path
                source_file = result
                logger.debug(f"📦 Gradio returned string path: {source_file}")
            else:
                logger.error(
                    f"❌ Unexpected response format from IndexTTS API: {result}"
                )
                return ""

            # Copy the generated file to our cache location
            if source_file:
                import shutil

                shutil.copy(source_file, cache_file)
                logger.info(f"✅ Successfully generated audio file: {cache_file}")
                return cache_file
            else:
                logger.error("❌ No valid file path found in API response")
                return ""

        except Exception as e:
            logger.error(f"❌ Failed to generate audio with IndexTTS: {e}")
            return ""

    def remove_file(self, filepath: str, verbose: bool = True) -> None:
        """Remove audio file from cache.

        Args:
            filepath (str): Path to the file to remove.
            verbose (bool): Whether to log debug information. Defaults to True.
        """
        super().remove_file(filepath, verbose)
