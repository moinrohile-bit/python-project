import requests
import base64
import os
import re
import time
from PIL import Image
from colorama import init, Fore, Style

# ========================= CONFIGURATION =========================

HF_API_KEY = "add api"

init(autoreset=True)

ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

VISION_MODELS = [
    "moonshotai/Kimi-K2.6:novita",
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct:sambanova",
    "meta-llama/Llama-3.2-11B-Vision-Instruct:sambanova",
]

TEXT_MODELS = [
    "Qwen/Qwen2.5-7B-Instruct:together",
    "Qwen/Qwen2.5-14B-Instruct:together",
    "Qwen/Qwen2.5-32B-Instruct:together",
    "mistralai/Mistral-7B-Instruct-v0.3:together",
    "mistralai/Mixtral-8x7B-Instruct-v0.1:together",
]

# ========================= UTILITIES =========================

def _data_url(path: str):
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def query_hf_api(payload):
    try:
        response = requests.post(
            ROUTER_URL,
            headers=HEADERS,
            json=payload,
            timeout=120
        )
    except requests.RequestException as e:
        return None, str(e)

    if response.status_code != 200:
        try:
            err = response.json()
            return None, err.get("error", {}).get("message", response.text)
        except Exception:
            return None, response.text

    return response.json(), None


def _extract_text(data):
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""


def _run_models(models, messages, max_tokens=200, temperature=0.3):

    last_error = ""

    for model in models:

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        data, err = query_hf_api(payload)

        if err:
            last_error = err
            continue

        text = _extract_text(data)

        if text:
            return text, None

        last_error = "Empty response."

    return None, last_error


def _words(text):
    return re.findall(r"\S+", text.strip())


def _exact_n_words(text, n):
    return " ".join(_words(text)[:n])


def _ensure_sentence_end(text):
    text = text.strip()
    if text and text[-1] not in ".!?":
        text += "."
    return text

# ========================= TEXT GENERATION =========================

def generate_text(prompt, max_new_tokens=220):

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    result, err = _run_models(
        TEXT_MODELS,
        messages,
        max_tokens=max_new_tokens,
        temperature=0.2
    )

    if result:
        return result

    raise Exception(err)


def generate_exact_sentence(prompt, n_words, max_new_tokens, tries=6):

    for _ in range(tries):

        response = generate_text(prompt, max_new_tokens)

        words = _words(response)

        if len(words) == n_words:
            return _ensure_sentence_end(response)

        if len(words) > n_words:
            return _ensure_sentence_end(" ".join(words[:n_words]))

        prompt = (
            f"Rewrite to EXACTLY {n_words} words.\n\n"
            + response
        )

        time.sleep(1)

    words = _words(response)

    if len(words) >= n_words:
        return _ensure_sentence_end(" ".join(words[:n_words]))

    return _ensure_sentence_end(response)

# ========================= IMAGE CAPTION =========================

def get_basic_caption(image_path):

    print(Fore.YELLOW + "Generating image caption...")

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this image in one complete sentence."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": _data_url(image_path)
                    }
                }
            ]
        }
    ]

    caption, err = _run_models(
        VISION_MODELS,
        messages,
        max_tokens=80,
        temperature=0.2
    )

    if caption:
        return caption

    return "[Error] " + err

# ========================= MENU =========================

def print_menu():

    print(
        Style.BRIGHT + Fore.GREEN +
"""
================ IMAGE TO TEXT =================

1. Caption (5 words)
2. Description (30 words)
3. Summary (50 words)
4. Exit

===============================================
"""
    )

# ========================= MAIN =========================

def main():

    image_path = input(
        Fore.CYAN +
        "Enter image path: "
    )

    if not os.path.exists(image_path):
        print(Fore.RED + "Image not found.")
        return

    try:
        Image.open(image_path)
    except Exception:
        print(Fore.RED + "Invalid image.")
        return

    basic_caption = get_basic_caption(image_path)

    print(
        Fore.YELLOW +
        "\nBasic Caption:\n" +
        Style.BRIGHT +
        basic_caption +
        "\n"
    )

    while True:

        print_menu()

        choice = input(
            Fore.BLUE +
            "Choice (1-4): "
        )

        if choice == "1":

            if basic_caption.startswith("[Error]"):
                print(basic_caption)
                continue

            output = _ensure_sentence_end(
                _exact_n_words(basic_caption, 5)
            )

            print(
                Fore.GREEN +
                "\nCaption:\n" +
                Fore.YELLOW +
                output +
                "\n"
            )

        elif choice == "2":

            if basic_caption.startswith("[Error]"):
                print(basic_caption)
                continue

            prompt = (
                "Rewrite the following into EXACTLY 30 words. "
                "One sentence only.\n\n"
                + basic_caption
            )

            try:
                result = generate_exact_sentence(
                    prompt,
                    30,
                    220
                )

                print(
                    Fore.GREEN +
                    "\nDescription:\n" +
                    Fore.YELLOW +
                    result +
                    "\n"
                )

            except Exception as e:
                print(e)

        elif choice == "3":

            if basic_caption.startswith("[Error]"):
                print(basic_caption)
                continue

            prompt = (
                "Write EXACTLY 50 words. "
                "One complete sentence.\n\n"
                + basic_caption
            )

            try:

                result = generate_exact_sentence(
                    prompt,
                    50,
                    280,
                    tries=7
                )

                print(
                    Fore.GREEN +
                    "\nSummary:\n" +
                    Fore.YELLOW +
                    result +
                    "\n"
                )

            except Exception as e:
                print(e)

        elif choice == "4":

            print(Fore.GREEN + "Goodbye!")
            break

        else:
            print(Fore.RED + "Invalid choice.")

if __name__ == "__main__":
    main()