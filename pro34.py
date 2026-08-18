#!/usr/bin/env python3

import sys
from pathlib import Path

from PIL import Image
from transformers import (
    pipeline,
    GPT2LMHeadModel,
    GPT2Tokenizer
)
from colorama import Fore, Style, init


# Initialize colored terminal output
init(autoreset=True)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

IMAGE_CAPTION_MODEL = "Salesforce/vit-gpt2-image-captioning"
GPT2_MODEL = "gpt2"


# --------------------------------------------------
# COLORED OUTPUT FUNCTIONS
# --------------------------------------------------

def print_success(message):
    print(Fore.GREEN + "[✓] " + message + Style.RESET_ALL)


def print_error(message):
    print(Fore.RED + "[✗] " + message + Style.RESET_ALL)


def print_info(message):
    print(Fore.CYAN + "[*] " + message + Style.RESET_ALL)


def print_warning(message):
    print(Fore.YELLOW + "[!] " + message + Style.RESET_ALL)


# --------------------------------------------------
# BASIC IMAGE CAPTION
# --------------------------------------------------

def get_basic_caption(image_path):
    try:
        print_info("Loading image captioning model...")
        
        captioner = pipeline(
            "image-to-text",
            model=IMAGE_CAPTION_MODEL
        )

        image = Image.open(image_path).convert("RGB")

        print_info("Generating image caption...")

        result = captioner(
            image,
            max_new_tokens=20
        )

        caption = result[0]["generated_text"].strip()

        return caption

    except Exception as e:
        print_error(f"Failed to generate caption: {e}")
        return None


# --------------------------------------------------
# GPT-2 LONG DESCRIPTION
# --------------------------------------------------

def get_long_description(caption):
    try:
        print_info("Loading GPT-2 model...")

        tokenizer = GPT2Tokenizer.from_pretrained(GPT2_MODEL)
        model = GPT2LMHeadModel.from_pretrained(GPT2_MODEL)

        prompt = (
            "Write a detailed image description of about 30 words "
            "based on this caption:\n\n"
            f"Caption: {caption}\n\n"
            "Description:"
        )

        inputs = tokenizer(
            prompt,
            return_tensors="pt"
        )

        print_info("Generating longer description...")

        output = model.generate(
            **inputs,
            max_new_tokens=60,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            no_repeat_ngram_size=2,
            pad_token_id=tokenizer.eos_token_id
        )

        generated_text = tokenizer.decode(
            output[0],
            skip_special_tokens=True
        )

        # Remove the original prompt
        if "Description:" in generated_text:
            description = generated_text.split(
                "Description:",
                1
            )[1].strip()
        else:
            description = generated_text.strip()

        # Clean up extra whitespace
        description = " ".join(description.split())

        # Limit approximately to 30 words
        words = description.split()

        if len(words) > 30:
            description = " ".join(words[:30])

        return description

    except Exception as e:
        print_error(f"Failed to generate long description: {e}")
        return None


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    print()
    print(Fore.CYAN + "=" * 55)
    print("       IMAGE CAPTION GENERATOR")
    print("=" * 55 + Style.RESET_ALL)
    print()

    # --------------------------------------------------
    # Get image path
    # --------------------------------------------------

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input(
            "Enter the image path: "
        ).strip()

    # Remove quotes if the user pasted a quoted path
    image_path = image_path.strip('"').strip("'")

    path = Path(image_path)

    # --------------------------------------------------
    # Check image exists
    # --------------------------------------------------

    if not path.exists():
        print_error(
            f"Image not found: {image_path}"
        )
        return

    if not path.is_file():
        print_error(
            "The specified path is not a file."
        )
        return

    # --------------------------------------------------
    # Open image
    # --------------------------------------------------

    try:
        image = Image.open(path)
        image.verify()

        print_success(
            f"Image opened successfully: {path.name}"
        )

    except Exception as e:
        print_error(
            f"Unable to open image: {e}"
        )
        return

    # --------------------------------------------------
    # Generate basic caption
    # --------------------------------------------------

    caption = get_basic_caption(str(path))

    if not caption:
        print_error(
            "Could not generate a caption."
        )
        return

    print()
    print(Fore.GREEN + "Basic Caption:" + Style.RESET_ALL)
    print(Fore.WHITE + caption)
    print()

    # --------------------------------------------------
    # Ask for longer description
    # --------------------------------------------------

    while True:

        choice = input(
            "Do you want a longer description? (y/n): "
        ).strip().lower()

        if choice in ("y", "yes"):
            break

        if choice in ("n", "no"):
            print_info(
                "Finished. No longer description requested."
            )
            return

        print_warning(
            "Please enter y or n."
        )

    # --------------------------------------------------
    # Generate longer description
    # --------------------------------------------------

    description = get_long_description(caption)

    if description:

        print()
        print(
            Fore.GREEN
            + "Long Description (~30 words):"
            + Style.RESET_ALL
        )

        print(Fore.WHITE + description)
        print()

        print_success(
            "Image description generated successfully!"
        )

    else:
        print_error(
            "Could not generate the longer description."
        )


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()