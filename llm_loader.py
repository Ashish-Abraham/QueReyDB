from transformers import pipeline
from langchain.llms import HuggingFacePipeline
import torch
import os
from dotenv import load_dotenv
from huggingface_hub import login

# Load .env file
load_dotenv()

def authenticate_huggingface():
    """
    Authenticates Hugging Face using the token from the .env file.
    """
    token = os.getenv("HUGGINGFACE_TOKEN")
    if not token:
        raise EnvironmentError("Hugging Face token not found in .env file. Please add HUGGINGFACE_TOKEN.")
    
    login(token=token)
    print("Successfully authenticated Hugging Face.")

def load_llm(model_name="mistralai/Mistral-7B-v0.1", max_new_tokens=100):
    """
    Loads the specified Hugging Face LLM model.

    Args:
        model_name (str, optional): The name of the Hugging Face model to load. Defaults to "mistralai/Mistral-7B-v0.1".
        max_new_tokens (int, optional): The maximum number of tokens to generate during text generation. Defaults to 100.

    Returns:
        HuggingFacePipeline: The loaded Hugging Face pipeline object.
    """

    try:
        # Authenticate with Hugging Face before loading the model
        authenticate_huggingface()

        # Load the pipeline
        pipe = pipeline(
            "text-generation",
            model=model_name,
            tokenizer=model_name,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            max_new_tokens=max_new_tokens,
            model_kwargs={"load_in_8bit": torch.cuda.is_available()}
        )

        return HuggingFacePipeline(pipeline=pipe)

    except Exception as e:
        raise RuntimeError(f"Failed to load LLM model '{model_name}': {e}")
