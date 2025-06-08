# openfabric_main.py

from openfabric_pysdk.context import OpenfabricExecutionContext
from openfabric_pysdk.helper import Schema
from typing import List

# Simulated function to generate an image from text
def generate_image(prompt: str) -> bytes:
    print(f"[Text-to-Image] Generating image for prompt: '{prompt}'")
    # Simulated image bytes (just for mock purposes)
    return b'FAKE_IMAGE_BYTES'

# Simulated function to generate a 3D model from image bytes
def generate_3d(image_bytes: bytes) -> bytes:
    print("[Image-to-3D] Generating 3D model from image bytes")
    # Simulated 3D model bytes
    return b'FAKE_MODEL_BYTES'

# Main handler called by the Openfabric runtime
def on_input(context: OpenfabricExecutionContext, payload: List[Schema]):
    for item in payload:
        prompt = item.text

        # Step 1: Generate image from text
        image_bytes = generate_image(prompt)

        # Step 2: Generate 3D model from image
        model_bytes = generate_3d(image_bytes)

        # Prepare a simple response
        result_message = (
            f"Prompt: {prompt}\n"
            f"Generated image size: {len(image_bytes)} bytes\n"
            f"Generated 3D model size: {len(model_bytes)} bytes"
        )

        # Send response back
        context.send(Schema(output=result_message))

