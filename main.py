# main.py (inside the execute function)

from openfabric import generate_image, generate_3d
import os

# The following block is removed because 'request' is not defined.
# Use the run_pipeline function below to process prompts.

# main.py

import logging
from llm import expand_prompt
from openfabric import generate_image, generate_3d
from memory import store_memory, retrieve_similar

def run_pipeline(prompt: str):
    """
    Runs the full pipeline: LLM expansion, image gen, 3D gen, and memory store.
    Returns the paths to the generated image and 3D model.
    """
    logging.info(f"Original prompt: {prompt}")
    # LLM expansion
    expanded = expand_prompt(prompt)
    logging.info(f"Expanded prompt: {expanded}")

    # Generate image from expanded prompt
    image_bytes = generate_image(expanded)
    img_path = 'assets/output.png'
    with open(img_path, 'wb') as f:
        f.write(image_bytes)
    logging.info(f"Saved image to {img_path}")

    # Generate 3D model from image
    model_bytes = generate_3d(image_bytes)
    model_path = 'assets/output.obj'
    with open(model_path, 'wb') as f:
        f.write(model_bytes)
    logging.info(f"Saved 3D model to {model_path}")

    # Store in memory for future reference
    store_memory(prompt, img_path, model_path)
    logging.info("Stored prompt in memory.")

    return img_path, model_path

# If using as a web service, call run_pipeline inside the execute() callback.
