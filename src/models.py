# Model configuration module for LangChain LLM setup.
# Handles environment variables and model initialization.

import os
from langchain_openai import ChatOpenAI
import src.config

# Valid DeepSeek model names
VALID_DEEPSEEK_MODELS = {"deepseek-chat", "deepseek-reasoner"}


def get_required_env_var(name: str) -> str:
    # Retrieve required environment variable or raise error if missing
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required environment variable: {name}")

    return value


# Load environment variables
api_key = get_required_env_var("DEEPSEEK_API_KEY")
base_url = get_required_env_var("DEEPSEEK_BASE_URL")
model_name = get_required_env_var("DEEPSEEK_MODEL")

# Validate model name
if model_name not in VALID_DEEPSEEK_MODELS:
    raise ValueError(
        "Invalid DEEPSEEK_MODEL. "
        f"Received '{model_name}', but expected one of: "
        f"{', '.join(sorted(VALID_DEEPSEEK_MODELS))}."
    )


# Initialize the ChatOpenAI model with DeepSeek configuration
llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model=model_name,
    streaming=True,
)

