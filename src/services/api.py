import random
import uuid
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# === TEAM SETUP ===
teams = [
    {"id": f"T{str(i).zfill(3)}", "name": name}
    for i, name in enumerate([
        "Barcelona", "Real Madrid", "Atletico", "Sevilla", "Valencia", "Betis",
        "Villarreal", "Getafe", "Osasuna", "Granada", "Celta Vigo", "Athletic Club",
        "Mallorca", "Almeria", "Rayo Vallecano", "Cadiz", "Girona"
    ])
]
team_id_to_name = {t["id"]: t["name"] for t in teams}

# === MATCH STATS LIST ===
stats_list = [
    "goal", "corners", "shots", "shots_on_target", "shots_off_target",
    "blocked_shots", "fouls_committed", "fouls_suffered",
    "yellow_cards", "red_cards", "offsides", "throw_ins",
    "free_kicks_won", "goalkeeper_saves", "clearances",
    "dribbles_completed", "crosses_completed", "passes_attempted", "passes_completed"
]

# === INTEGER STAT GENERATOR ===
def gen_stat(max_val):
    return random.randint(0, max_val)

# === CREATE A SINGLE MATCH RECORD ===
def create_match(home, away):
    match = {
        "match_id": str(uuid.uuid4())[:8],
        "home_team_id": home["id"],
        "home_team_name": home["name"],
        "away_team_id": away["id"],
        "away_team_name": away["name"]
    }

    for stat in stats_list:
        if stat == "goal":
            max_val = 5
        elif stat == "red_cards":
            max_val = 2
        elif stat == "yellow_cards":
            max_val = 6
        elif stat in ["passes_attempted", "passes_completed"]:
            max_val = 500
        else:
            max_val = 30

        home_fh = gen_stat(max_val)
        away_fh = gen_stat(max_val)
        home_sh = gen_stat(max_val)
        away_sh = gen_stat(max_val)

        home_ft = home_fh + home_sh
        away_ft = away_fh + away_sh

        match[f"home_fh_{stat}"] = home_fh
        match[f"away_fh_{stat}"] = away_fh
        match[f"home_sh_{stat}"] = home_sh
        match[f"away_sh_{stat}"] = away_sh
        match[f"home_ft_{stat}"] = home_ft
        match[f"away_ft_{stat}"] = away_ft
        match[f"fh_{stat}_total"] = home_fh + away_fh
        match[f"sh_{stat}_total"] = home_sh + away_sh
        match[f"ft_{stat}_total"] = home_ft + away_ft

    # === MARKET TARGETS ===
    match["BTTS"] = int(match["home_ft_goal"] > 0 and match["away_ft_goal"] > 0)
    match["Over_1_5_goals"] = int(match["ft_goal_total"] > 1)
    match["Corners_Over_6_5"] = int(match["ft_corners_total"] > 6)
    match["Corners_Under_7_5"] = int(match["ft_corners_total"] < 8)
    return match

# === CREATE AND SAVE DATASET ===
def generate_and_save_dataset(filename="match_dataset.csv", num_matches=1000):
    matches = []
    for _ in range(num_matches):
        home, away = random.sample(teams, 2)
        matches.append(create_match(home, away))
    df = pd.DataFrame(matches)
    df.to_csv(filename, index=False)
    print(f"✅ Dataset saved to {filename}")

# === LOAD DATASET ===
def load_dataset(filename="match_dataset.csv"):
    df = pd.read_csv(filename)
    print(f"✅ Dataset loaded from {filename}")
    return df

# === TRAIN MODELS ===
def train_models(df):
    labels = ["BTTS", "Over_1_5_goals", "Corners_Over_6_5", "Corners_Under_7_5"]
    exclude_cols = ["match_id", "home_team_id", "home_team_name", "away_team_id", "away_team_name"] + labels
    features = [col for col in df.columns if col not in exclude_cols]

    models = {}
    for label in labels:
        X = df[features]
        y = df[label]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        acc = clf.score(X_test, y_test)
        print(f"📊 {label} model accuracy: {acc:.2f}")
        models[label] = clf

    return models, features

# === PREDICT + PRINT MATCH DETAILS ===
def predict_markets(home_id, away_id, df, models, features):
    relevant_matches = df[
        (df["home_team_id"].isin([home_id, away_id])) |
        (df["away_team_id"].isin([home_id, away_id]))
    ]

    home_matches = relevant_matches[
        (relevant_matches["home_team_id"] == home_id) | (relevant_matches["away_team_id"] == home_id)
    ]
    away_matches = relevant_matches[
        (relevant_matches["home_team_id"] == away_id) | (relevant_matches["away_team_id"] == away_id)
    ]

    if home_matches.empty or away_matches.empty:
        return "❌ Not enough data for prediction."

    avg_home = home_matches[features].mean()
    avg_away = away_matches[features].mean()
    combined_features = ((avg_home + avg_away) / 2).to_frame().T

    home_name = team_id_to_name[home_id]
    away_name = team_id_to_name[away_id]

    print(f"\n📊 Average Full-Time Stats for {home_name}:")
    for col in features:
        if col.startswith("home_ft_"):
            stat = col.replace("home_ft_", "")
            print(f"   {stat}: {int(avg_home[col])}")

    print(f"\n📊 Average Full-Time Stats for {away_name}:")
    for col in features:
        if col.startswith("away_ft_"):
            stat = col.replace("away_ft_", "")
            print(f"   {stat}: {int(avg_away[col])}")

    print(f"\n⚽ Combined FT Totals:")
    for col in features:
        if col.startswith("ft_") and col.endswith("_total"):
            stat = col.replace("ft_", "").replace("_total", "")
            print(f"   {stat}: {int(combined_features[col].values[0])}")

    print(f"\n🎯 Market Predictions:")
    results = {}
    for label, model in models.items():
        proba = model.predict_proba(combined_features)
        if proba.shape[1] == 1:
            prob = 100.0 if model.classes_[0] == 1 else 0.0
        else:
            prob = proba[0][1] * 100
        results[label] = prob
        print(f"   {label}: {prob:.2f}%")

    return results

# === MAIN ===
if __name__ == "__main__":
    generate_and_save_dataset()  # Step 1: create .csv
    df = load_dataset()          # Step 2: load dataset
    models, feature_cols = train_models(df)  # Step 3: train models

    # Step 4: Predict for match
    home_id = "T000"  # Barcelona
    away_id = "T001"  # Real Madrid
    predict_markets(home_id, away_id, df, models, feature_cols)
