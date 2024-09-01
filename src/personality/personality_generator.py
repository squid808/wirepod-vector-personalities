import json
import random

# Define the lists
baseline_list = [
    "Happy", "Sad", "Excited", "Angry", "Curious", "Anxious", "Confident", 
    "Frustrated", "Calm", "Enthusiastic", "Bored", "Grateful", 
    "Disappointed", "Hopeful", "Apologetic", "Proud", "Nervous", "Relieved"
]

spike_list = [
    "Annoyed", "Sarcastic", "Plucky", "Irritated", "Embarrassed", "Eager", 
    "Joking", "Frivolous", "Agitated", "Exasperated", "Quirky", "Mocking", 
    "Hyper", "Grumpy", "Exuberant", "Impatient", "Mischievous", "Jealous", 
    "Shocked", "Indignant", "Surprised", "Excited"
]

interest_list = [
    "Science", "Pop culture", "History", "Travel", "Music", "Sports", "Art", 
    "Cooking", "Reading", "Movies", "Technology", "Fitness", "Gaming", 
    "Nature", "Photography", "Fashion", "Politics", "Literature", "Theater", 
    "Gardening"
]

# regions = [
#     "en_us", "en_uk", "en_ca", "en_au", "en_nz", "en_ie", "en_sg", "en_in", "en_ph",
#     "fr_fr", "fr_ca", "de_de", "es_es", "es_mx", "it_it", "pt_pt", "pt_br", "nl_nl",
#     "sv_se", "da_dk", "no_no", "fi_fi", "ru_ru", "ja_jp", "ko_kr", "zh_cn", "zh_tw",
#     "ar_sa", "tr_tr", "he_il", "pl_pl", "cs_cz", "sk_sk", "ro_ro", "hu_hu"
# ]

regions = [
    "United States", "United Kingdom", "Canada", "Australia", "New Zealand", 
    "Ireland", "Singapore", "India", "Philippines", "France", "Canada (French)", 
    "Germany", "Spain", "Mexico", "Italy", "Portugal", "Brazil", "Netherlands", 
    "Sweden", "Denmark", "Norway", "Finland", "Russia", "Japan", "South Korea", 
    "China (Simplified)", "Taiwan", "Saudi Arabia", "Turkey", "Israel", "Poland", 
    "Czech Republic", "Slovakia", "Romania", "Hungary"
]

quirks = [
    "Likes to use animal sounds in sentences for emphasis or humor",
    "Obsessed with a specific category within a topic of interest",
    "Believes they are a time traveler stuck in the wrong time",
    "Frequently uses puns and wordplay",
    "Has a peculiar habit of quoting movie lines",
    "Speaks in a way that mimics famous personalities",
    "Uses exaggerated expressions and gestures",
    "Has a unique way of interpreting common phrases",
    "Frequently references obscure trivia",
    "Believes they have a secret superpower",
    "Has a quirky fashion sense",
    "Tends to speak in rhymes",
    "Always uses metaphors to describe things",
    "Has a fascination with unusual hobbies",
    "Uses made-up words or phrases",
    "Often incorporates fictional scenarios into conversation",
    "Has an obsession with collecting unusual items",
    "Frequently changes their accent or dialect",
    "Uses dramatic pauses for effect",
    "Tends to make up their own rules for games or activities",
    "Believes they can communicate with animals",
    "Uses unconventional methods to solve problems",
    "Has a habit of referring to themselves in the third person",
    "Often speaks in riddles",
    "Has a ritualistic way of doing everyday tasks",
    "Consistently references personal catchphrases",
    "Likes to create and follow elaborate personal traditions",
    "Has an unusual fascination with historical events",
    "Frequently engages in role-playing scenarios",
    "Tends to invent new games or challenges spontaneously",
    "Believes they have a special connection with the universe"
]

def normalize_values(values):
    total = sum(values.values())  # Calculate the sum of the dictionary values
    if total == 0:
        return {key: 0 for key in values}  # Handle the case where total is 0 to avoid division by zero
    return {key: round(value / total, 2) for key, value in values.items()}

def generate_personality_profile():
    # Randomly select 3 items from each list
    selected_baseline = random.sample(baseline_list, 3)
    selected_spike = random.sample(spike_list, 3)
    selected_interest = random.sample(interest_list, 3)
    chosen_region = random.choice(regions)
    chosen_quirk = random.choice(quirks)
    
    # Generate random weights/occurrence values
    baseline_weights = {item: random.uniform(0, 1) for item in selected_baseline}
    spike_occurrence = {item: random.uniform(0.1, 1) for item in selected_spike}
    interest_occurrence = {item: random.uniform(0.1, 1) for item in selected_interest}
    
    # Normalize the values
    baseline_weights = normalize_values(baseline_weights)
    spike_occurrence = normalize_values(spike_occurrence)
    interest_occurrence = normalize_values(interest_occurrence)
    
    # Create the profile object
    profile = {
        "nickname": "",
        "description": "Personality profile used to influence the generation of conversational messages and engagement.",
        "personality_quirk": { 
            "description": "A single stand-out feature of this personality, to heavily influence the outcomes.",
            "selected": chosen_quirk
        },
        "region": { 
            "description": "The region of origin for this personality, to influence word choices, structure, and knowledge.",
            "selected": chosen_region
        },
        "baseline_personality": {
            "description": "Baseline personality traits that describe the general emotional and stylistic tendencies of the individual. Weights indicate overall influence on responses.",
            "selected": baseline_weights
        },
        "personality_spike": {
            "description": "Emotions or tones that might spike during specific moments in conversation, indicating transient or heightened emotional states. Weights influence how frequently this occurs.",
            "selected": spike_occurrence
        },
        "topics_of_interest": {
            "description": "Areas of interest that define the individual's hobbies and preferences, reflecting their engagement with various topics. Weights influence how frequently this comes up.",
            "selected": interest_occurrence
        }
    }
    
    return profile

# def output_to_json(profile, filename='personality_profile.json'):
#     with open(filename, 'w') as f:
#         json.dump(profile, f, indent=4)

def print_pretty_json(profile):
    print(json.dumps(profile, indent=4))

def print_natural_language(profile_data):
    # profile_data = profile["personality_profile"]
    
    quirk = profile_data["personality_quirk"]["selected"]
    region = profile_data["region"]["selected"]
    
    baseline = profile_data["baseline_personality"]["selected"]
    spike = profile_data["personality_spike"]["selected"]
    interests = profile_data["topics_of_interest"]["selected"]
    
    baseline_items = sorted(baseline.items(), key=lambda x: -x[1])[:3]
    spike_items = sorted(spike.items(), key=lambda x: -x[1])[:3]
    
    baseline_description = ", ".join(f"{item[0]} at {item[1]*100}%" for item in baseline_items)
    spike_description = ", ".join(f"{item[0]} tone {item[1]*100}%" for item in spike_items)
    interest_description = ", ".join(f"{item[0]}" for item in interests.items())

    description = (
        f"{quirk}. It is associated with the region of {region}, "
        f"which influences its word choices, structure, and knowledge. The baseline emotions expressed by this personality "
        f"are most frequently {baseline_description}. Occasionally, it might display a {spike_description}, indicating heightened "
        f"emotional states during specific moments. The topics of interest for this personality include {interest_description}, "
        f"reflecting its hobbies and preferences."
    )
    
    print(description)

# if __name__ == "__main__":
#     profile = generate_personality_profile()
#     # output_to_json(profile)
#     print_pretty_json(profile)
#     print_natural_language(profile)