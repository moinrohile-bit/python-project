import requests

# Dictionary of API endpoints
ENDPOINTS = {
    "1": ("General", "https://uselessfacts.jsph.pl/random.json?language=en"),
    "2": ("Technology", "https://uselessfacts.jsph.pl/category/Technology.json?language=en"),
    "3": ("History", "https://uselessfacts.jsph.pl/category/History.json?language=en"),
    "4": ("Science", "https://uselessfacts.jsph.pl/category/Science.json?language=en"),
    "5": ("Sports", "https://uselessfacts.jsph.pl/category/Sports.json?language=en"),
    "6": ("Music", "https://uselessfacts.jsph.pl/category/Music.json?language=en"),
    "7": ("Movies", "https://uselessfacts.jsph.pl/category/Movies.json?language=en")
}


def get_fact(url):
    """Fetch and display a fact from the selected endpoint."""
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if "text" in data:
                print("\n==============================")
                print(" Random Fact")
                print("==============================")
                print(data["text"])
                print("==============================\n")
            else:
                print("No fact found in the response.")
        else:
            print(f"Error: Status Code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Error connecting to the API.")
        print(e)


def main():
    print("===================================")
    print(" Random Useless Facts Explorer")
    print("===================================")

    while True:
        print("\nChoose a category:")
        for key, (name, _) in ENDPOINTS.items():
            print(f"{key}. {name}")

        choice = input("\nEnter your choice (1-7): ").strip()

        if choice in ENDPOINTS:
            category, url = ENDPOINTS[choice]
            print(f"\nFetching a {category} fact...")
            get_fact(url)
        else:
            print("Invalid choice. Please try again.")
            continue

        again = input("Would you like another fact? (yes/no): ").strip().lower()

        if again not in ["yes", "y"]:
            print("\nThanks for using the Random Facts Explorer!")
            break


if __name__ == "__main__":
    main()