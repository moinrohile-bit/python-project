import time

def chatbot():
    print("🤖 Hello! I am your Interactive Chatbot.")
    print("Type 'exit' anytime to end the chat.\n")

    while True:
        name = input("What is your name? ").strip()

        if name.lower() == "exit":
            print("👋 Goodbye!")
            break

        print(f"\nNice to meet you, {name}!")

        mood = input("How are you feeling today? (happy/sad/angry/excited): ").lower()

        # Emotion-based responses
        if mood == "happy":
            print("😊 That's awesome! Keep smiling!")
        elif mood == "sad":
            print("💙 I'm sorry to hear that. Hope things get better soon.")
        elif mood == "angry":
            print("😌 Take a deep breath. Everything will be okay.")
        elif mood == "excited":
            print("🎉 Wow! Your excitement is contagious!")
        else:
            print("🤔 Interesting feeling!")

        # Conversation topics
        print("\nLet's talk about something!")
        print("1. Movies")
        print("2. Music")
        print("3. Sports")
        print("4. Technology")

        choice = input("Choose a topic (1-4): ")

        if choice == "1":
            movie = input("🎬 What is your favorite movie? ")
            print(f"Cool! '{movie}' sounds like a great movie.")
        
        elif choice == "2":
            music = input("🎵 Who is your favorite singer or band? ")
            print(f"Nice! I should listen to {music} sometime.")
        
        elif choice == "3":
            sport = input("⚽ What is your favorite sport? ")
            print(f"{sport} is fun to watch and play!")
        
        elif choice == "4":
            tech = input("💻 What technology do you like most? ")
            print(f"{tech} is really interesting!")
        
        else:
            print("❌ Invalid choice.")

        # Small delay for realism
        time.sleep(1)

        # Repeat or end
        again = input("\nDo you want to chat again? (yes/no): ").lower()

        if again != "yes":
            print("\n👋 Thanks for chatting! Have a great day!")
            break

        print("\n" + "-" * 40 + "\n")

chatbot()