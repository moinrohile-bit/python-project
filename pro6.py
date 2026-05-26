import random
import pandas as pd
from textblob import TextBlob
from colorama import Fore, Back, Style, init
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize colorama for Mac Terminal formatting
init(autoreset=True)

# 1. Prepare Dataset using Pandas
movies_data = {
    "title": ["Inception", "The Dark Knight", "Interstellar", "Pulp Fiction", "The Hangover", 
              "Spirited Away", "Toy Story", "The Notebook", "The Conjuring", "Superbad"],
    "genre": ["Sci-Fi Action", "Action Crime Thriller", "Sci-Fi Drama Adventure", "Crime Drama", "Comedy", 
              "Animation Fantasy Family", "Animation Comedy Family", "Romance Drama", "Horror Mystery", "Comedy"],
    "description": ["A mind-bending psychological thriller about dreams within dreams and heist action.",
                    "A dark, intense superhero crime drama about chaos, justice, and the Joker.",
                    "An emotional cosmic journey through space and time to save humanity.",
                    "A quirky, violent crime story with dark humor and interconnected timelines.",
                    "A hilarious, wild comedy about a chaotic bachelor party road trip in Las Vegas.",
                    "A beautiful, magical fantasy adventure about a girl saving her parents in a spirit world.",
                    "A heartwarming, fun animated story about toys that come alive and friendship.",
                    "A deeply emotional, sad romantic drama about lifelong love and memories.",
                    "A terrifying, spooky haunted house horror film based on true paranormal events.",
                    "A crude, laugh-out-loud funny high school teenage comedy about buying alcohol."],
    "sentiment_target": [0.1, -0.3, 0.2, -0.2, 0.6, 0.4, 0.7, 0.3, -0.6, 0.5] # Ideal polarity match
}

df = pd.DataFrame(movies_data)

# Combine features for machine learning similarity matrix
df['combined_features'] = df['genre'] + " " + df['description']

def display_movie(row):
    """Formats and displays the movie details beautifully using colorama."""
    print("\n" + Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + Style.BRIGHT + f" 🎬  RECOMMENDATION: {row['title'].upper()}")
    print(Fore.CYAN + "=" * 50)
    print(f"{Fore.GREEN}🔹 Genre:{Style.RESET_ALL}       {row['genre']}")
    print(f"{Fore.GREEN}🔹 Description:{Style.RESET_ALL} {row['description']}")
    print(Fore.CYAN + "=" * 50 + "\n")

def get_ai_recommendation(user_query):
    """AI Engine using Sklearn (TF-IDF + Cosine Similarity) and TextBlob (Sentiment Analysis)"""
    # Sentiment Analysis with TextBlob
    blob = TextBlob(user_query)
    user_polarity = blob.sentiment.polarity
    
    # TF-IDF & Similarity Matrix with Sklearn
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    
    user_vector = tfidf.transform([user_query])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    
    # Combine content similarity and sentiment alignment score
    final_scores = []
    for idx, score in enumerate(similarity_scores):
        sentiment_diff = abs(df.iloc[idx]['sentiment_target'] - user_polarity)
        sentiment_score = 1 - sentiment_diff  # Closer sentiment = higher score
        
        # Weighted score: 70% textual content match, 30% sentiment tone match
        combined_score = (score * 0.7) + (sentiment_score * 0.3)
        final_scores.append((combined_score, idx))
        
    final_scores.sort(key=lambda x: x[0], reverse=True)
    best_match_idx = final_scores[0][1]
    
    return df.iloc[best_match_idx]

def main():
    print(Fore.MAGENTA + Style.BRIGHT + "===============================================")
    print(Fore.MAGENTA + Style.BRIGHT + "   SMART MOVIE RECOMMENDATION SYSTEM (MAC)     ")
    print(Fore.MAGENTA + Style.BRIGHT + "===============================================\n")
    
    while True:
        print(Fore.WHITE + "Choose an option:")
        print(f"{Fore.YELLOW}1.{Fore.RESET} AI-Based Recommendation (Matches your mood & keywords)")
        print(f"{Fore.YELLOW}2.{Fore.RESET} Random Recommendation")
        print(f"{Fore.YELLOW}3.{Fore.RESET} Exit")
        
        choice = input(Fore.BLUE + "\nEnter option (1-3): ").strip()
        
        if choice == '1':
            user_input = input(Fore.GREEN + "\nDescribe your mood or what you want to watch: ")
            if not user_input.strip():
                print(Fore.RED + "Input cannot be empty!")
                continue
            
            print(Fore.YELLOW + "\n🤖 AI is analyzing your sentiment and calculating text similarity...")
            rec = get_ai_recommendation(user_input)
            display_movie(rec)
            
        elif choice == '2':
            print(Fore.YELLOW + "\n🎲 Picking a random movie from the database...")
            random_idx = random.randint(0, len(df) - 1)
            rec = df.iloc[random_idx]
            display_movie(rec)
            
        elif choice == '3':
            print(Fore.MAGENTA + "\nGoodbye! Enjoy your movie night. 🍿")
            break
        else:
            print(Fore.RED + "\n❌ Invalid option. Please choose 1, 2, or 3.\n")

if __name__ == "__main__":
    main()
