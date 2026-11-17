# Choose ONE provider by importing it:

#Change groq --> hf to use hugging face API
#Change hf --> groq to use groq API
from groq import generate_response
# from groq import generate_response


def bias_mitigation_activity():
    print("\n=== BIAS MITIGATION ACTIVITY ===\n")
    prompt = input("Enter a prompt to explore bias (e.g., 'Describe the ideal doctor'): ").strip()
    if not prompt:
        print("Please enter a prompt to run the activity.")
        return

    initial_response = generate_response(prompt, temperature=0.3, max_tokens=1024)
    print(f"\nInitial AI Response: {initial_response}")

    modified_prompt = input(
        "Modify the prompt to make it more neutral (e.g., 'Describe the qualities of a doctor'): "
    ).strip()
    if modified_prompt:
        modified_response = generate_response(modified_prompt, temperature=0.3, max_tokens=1024)
        print(f"\nModified AI Response (Neutral): {modified_response}")
    else:
        print("No modified prompt entered. Skipping neutral response.")

def token_limit_activity():
    print("\n=== TOKEN LIMIT ACTIVITY ===\n")
    long_prompt = input(
        "Enter a long prompt (more than 300 words, e.g., a detailed story or description): "
    ).strip()

    if long_prompt:
        long_response = generate_response(long_prompt, temperature=0.3, max_tokens=1024)
        preview = (long_response[:500] + "...") if len(long_response) > 500 else long_response
        print(f"\nResponse to Long Prompt: {preview}")
    else:
        print("No long prompt entered. Skipping long prompt response.")

    short_prompt = input("Now, condense the prompt to be more concise: ").strip()
    if short_prompt:
        short_response = generate_response(short_prompt, temperature=0.3, max_tokens=1024)
        print(f"\nResponse to Condensed Prompt: {short_response}")
    else:
        print("No condensed prompt entered. Skipping condensed prompt response.")

def run_activity():
    print("\n=== AI Learning Activity ===")
    print("Choose an activity:")
    print("1) Bias Mitigation")
    print("2) Token Limits")
    choice = input("> ").strip()

    if choice == "1":
        bias_mitigation_activity()
    elif choice == "2":
        token_limit_activity()
    else:
        print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    run_activity()
