import json, os

def load_leaderboard():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json") as f:
            return json.load(f)
    return []

def add_score(name, score, distance):
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": distance})
    board.sort(key=lambda x: x["score"], reverse=True)
    with open("leaderboard.json", "w") as f:
        json.dump(board[:10], f)

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json") as f:
            return json.load(f)
    return {"sound": True, "difficulty": "normal"}

def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f)