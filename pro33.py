import os
import sys

from huggingface_hub import InferenceClient
from transformers import (
    VisionEncoderDecoderModel,
    ViTImageProcessor,
    AutoTokenizer
)
from PIL import Image


# ============================================================
# SETTINGS
# ============================================================

HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    print("❌ Hugging Face token not found.")
    print()
    print("Run this in Terminal first:")
    print('export HF_TOKEN="hf_your_token_here"')
    sys.exit(1)


# Hugging Face models
TEXT_MODEL = "openai-community/gpt2"

# Current Hugging Face text-to-image model
IMAGE_MODEL = "black-forest-labs/FLUX.1-schnell"

# Assignment's requested captioning model
CAPTION_MODEL = "nlpconnect/vit-gpt2-image-captioning"


# ============================================================
# HUGGING FACE CLIENT
# ============================================================

client = InferenceClient(
    api_key=HF_TOKEN,
    provider="auto"
)


# ============================================================
# STEP 1 - GET USER PROMPT
# ============================================================

def get_user_prompt():

    print("\n======================================")
    print("       AI CREATIVE WORKFLOW")
    print("======================================")

    prompt = input("\nEnter a short idea: ").strip()

    if not prompt:
        print("❌ Please enter a prompt.")
        sys.exit(1)

    return prompt


# ============================================================
# STEP 2 - GPT-2 TEXT GENERATION
# ============================================================

def expand_prompt(user_prompt):

    print("\n🧠 Step 1: Expanding your prompt with GPT-2...")

    prompt = (
        "Expand the following short idea into a detailed "
        "visual description for an image:\n\n"
        + user_prompt
    )

    try:

        result = client.text_generation(
            prompt,
            model=TEXT_MODEL,
            max_new_tokens=80,
            temperature=0.8
        )

        expanded_text = result.strip()

        print("\n--------------------------------------")
        print("EXPANDED PROMPT")
        print("--------------------------------------")
        print(expanded_text)
        print("--------------------------------------")

        return expanded_text

    except Exception as error:

        print("\n❌ Text generation failed.")
        print("Error:", error)

        return None


# ============================================================
# STEP 3 - IMAGE GENERATION
# ============================================================

def generate_image(expanded_prompt):

    print("\n🎨 Step 2: Generating image...")

    try:

        image = client.text_to_image(
            prompt=expanded_prompt,
            model=IMAGE_MODEL
        )

        filename = "generated_image.png"

        image.save(filename)

        print("✅ Image saved as:", filename)

        return filename

    except Exception as error:

        print("\n❌ Image generation failed.")
        print("Error:", error)

        return None


# ============================================================
# STEP 4 - LOAD ViT-GPT2
# ============================================================

def load_caption_model():

    print("\n🤖 Loading ViT-GPT2 captioning model...")
    print("(The first run may take some time.)")

    try:

        model = VisionEncoderDecoderModel.from_pretrained(
            CAPTION_MODEL
        )

        processor = ViTImageProcessor.from_pretrained(
            CAPTION_MODEL
        )

        tokenizer = AutoTokenizer.from_pretrained(
            CAPTION_MODEL
        )

        return model, processor, tokenizer

    except Exception as error:

        print("\n❌ Could not load ViT-GPT2.")
        print("Error:", error)

        return None, None, None


# ============================================================
# STEP 5 - IMAGE CAPTIONING
# ============================================================

def caption_image(
    image_path,
    model,
    processor,
    tokenizer
):

    print("\n📝 Step 3: Creating image caption...")

    try:

        image = Image.open(image_path)

        # Convert image to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Process image
        pixel_values = processor(
            images=image,
            return_tensors="pt"
        ).pixel_values

        # Generate caption
        output_ids = model.generate(
            pixel_values,
            max_length=16,
            num_beams=4
        )

        # Convert tokens into text
        caption = tokenizer.batch_decode(
            output_ids,
            skip_special_tokens=True
        )[0].strip()

        print("\n--------------------------------------")
        print("IMAGE CAPTION")
        print("--------------------------------------")
        print(caption)
        print("--------------------------------------")

        return caption

    except Exception as error:

        print("\n❌ Caption generation failed.")
        print("Error:", error)

        return None


# ============================================================
# STEP 6 - MAIN WORKFLOW
# ============================================================

def main():

    # Get user's idea
    user_prompt = get_user_prompt()

    # Generate expanded text
    expanded_prompt = expand_prompt(user_prompt)

    if expanded_prompt is None:
        return

    # Generate image
    image_path = generate_image(expanded_prompt)

    if image_path is None:
        return

    # Load captioning model
    model, processor, tokenizer = load_caption_model()

    if model is None:
        return

    # Caption generated image
    caption = caption_image(
        image_path,
        model,
        processor,
        tokenizer
    )

    print("\n======================================")
    print("          WORKFLOW COMPLETE")
    print("======================================")

    print("\nFiles:")
    print("📁 generated_image.png")

    print("\nOriginal prompt:")
    print(user_prompt)

    print("\nExpanded prompt:")
    print(expanded_prompt)

    if caption:
        print("\nGenerated caption:")
        print(caption)

    print("\n✅ Finished!")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()