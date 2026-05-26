import random

def get_ai_move(player_history):
    choices = ["rock", "paper", "scissors"]
    counters = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    
    # If not enough data, make a random choice
    if len(player_history) < 3:
        return random.choice(choices)
    
    # Simple AI Strategy: Find the player's most frequent move and counter it
    rock_count = player_history.count("rock")
    paper_count = player_history.count("paper")
    scissors_count = player_history.count("scissors")
    
    most_frequent = "rock"
    max_count = rock_count
    
    if paper_count > max_count:
        most_frequent = "paper"
        max_count = paper_count
    if scissors_count > max_count:
        most_frequent = "scissors"
        
    return counters[most_frequent]

def determine_winner(player, ai):
    if player == ai:
        return "tie"
    
    winning_combos = {
        ("rock", "scissors"): "player",
        ("paper", "rock"): "player",
        ("scissors", "paper"): "player"
    }
    
    if (player, ai) in winning_combos:
        return "player"
    return "ai"

def play_game():
    print("Welcome to Rock, Paper, Scissors vs AI!")
    print("Type 'rock', 'paper', or 'scissors' to play. Type 'quit' to exit.\n")
    
    player_history = []
    scores = {"player": 0, "ai": 0, "ties": 0}
    valid_moves = ["rock", "paper", "scissors"]
    
    while True:
        player_move = input("Your move: ").strip().lower()
        
        if player_move == "quit":
            print("\nGame Over! Final Scores:")
            print(f"Player: {scores['player']} | AI: {scores['ai']} | Ties: {scores['ties']}")
            break
            
        if player_move not in valid_moves:
            print("Invalid move. Please try again.")
            continue
            
        ai_move = get_ai_move(player_history)
        player_history.append(player_move)
        
        print(f"AI chose: {ai_move}")
        
        result = determine_winner(player_move, ai_move)
        if result == "tie":
            print("It's a tie!")
            scores["ties"] += 1
        elif result == "player":
            print("You win this round!")
            scores["player"] += 1
        else:
            print("AI wins this round!")
            scores["ai"] += 1
            
        print(f"Score -> You: {scores['player']} | AI: {scores['ai']}\n")

if __name__ == "__main__":
    play_game()
