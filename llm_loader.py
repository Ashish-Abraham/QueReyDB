from langchain.llms import HuggingFacePipeline


def load_llm(model_name="mistralai/Mistral-7B-v0.1", max_new_tokens=100):
    """
    Loads the specified Hugging Face LLM model.

    Args:
        model_name (str, optional): The name of the Hugging Face model to load. Defaults to "mistralai/Mistral-7B-v0.1".
        max_new_tokens (int, optional): The maximum number of tokens to generate during text generation. Defaults to 100.

    Returns:
        HuggingFacePipeline: The loaded Hugging Face pipeline object.
    """

    pipe = pipeline(
        "text-generation",
        model=model_name,
        tokenizer=model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        max_new_tokens=max_new_tokens,
    )

    return HuggingFacePipeline(pipeline=pipe)

