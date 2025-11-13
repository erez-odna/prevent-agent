from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from utils.file_utils import read_json_from_file
from settings import AppSettings

AppSettings.loadenv()


# Make sure your environment variables are set:
# For Claude: ANTHROPIC_API_KEY
# For ChatGPT: OPENAI_API_KEY


class LlmChatModelFactory:
    def __init__(self):
        self.models = read_json_from_file(
            Path(__file__).parent.joinpath("llm_models.json")
        )

    def create_model(self, model_key):
        model = self.models[model_key]
        if model_key == "claude":
            return ChatAnthropic(model=model)
        if model_key == "gpt":
            return ChatOpenAI(model=model)
        return None
