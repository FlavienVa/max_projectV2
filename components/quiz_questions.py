QUIZ_QUESTIONS = [
    {
        "question": "What kind of scenery do you prefer?",
        "options": ["Mountains", "Cities", "Countryside"],
        "weights": {
            "Mountains": {"Nature": 1, "Relax": 0, "City": 0},
            "Cities": {"Nature": 0, "Relax": 0, "City": 1},
            "Countryside": {"Nature": 0.5, "Relax": 1, "City": 0}
        }
    },
    {
        "question": "Who are you traveling with?",
        "options": ["Family", "Couple", "Friends"],
        "weights": {
            "Family": {"Nature": 0.5, "Relax": 1, "City": 0.5},
            "Couple": {"Nature": 0.5, "Relax": 1, "City": 0.5},
            "Friends": {"Nature": 1, "Relax": 0.5, "City": 1}
        }
    },
    {
        "question": "What is your age group?",
        "options": ["18-30", "30-50", "50+"],
        "weights": {
            "18-30": {"Nature": 1, "Relax": 0.5, "City": 1},
            "30-50": {"Nature": 0.5, "Relax": 1, "City": 0.5},
            "50+": {"Nature": 0.5, "Relax": 1, "City": 0.5}
        }
    },
    {
        "question": "Preferred travel style?",
        "options": ["Relaxation", "Adventure", "Culture"],
        "weights": {
            "Relaxation": {"Nature": 0.5, "Relax": 1, "City": 0.5},
            "Adventure": {"Nature": 1, "Relax": 0, "City": 0.5},
            "Culture": {"Nature": 0, "Relax": 0.5, "City": 1}
        }
    },
    {
        "question": "Travel pace?",
        "options": ["Fast-paced", "Mix of both", "Slow and immersive"],
        "weights": {
            "Fast-paced": {"Nature": 0.5, "Relax": 0, "City": 1},
            "Mix of both": {"Nature": 1, "Relax": 0.5, "City": 0.5},
            "Slow and immersive": {"Nature": 0.5, "Relax": 1, "City": 0}
        }
    },
    {
        "question": "Preferred transportation?",
        "options": ["Hiking/VTT", "Private car", "Public transport"],
        "weights": {
            "Hiking/VTT": {"Nature": 1, "Relax": 0, "City": 0},
            "Private car": {"Nature": 0.5, "Relax": 1, "City": 0.5},
            "Public transport": {"Nature": 0, "Relax": 0.5, "City": 1}
        }
    },
    {
        "question": "Evening plans?",
        "options": ["Camping", "Spa", "Partying"],
        "weights": {
            "Camping": {"Nature": 1, "Relax": 0, "City": 0},
            "Spa": {"Nature": 0, "Relax": 1, "City": 0.5},
            "Partying": {"Nature": 0, "Relax": 0, "City": 1}
        }
    },
    {
        "question": "When are you planning to travel?",
        "options": ["Summer", "Winter"],
        "weights": {
            "Summer": {"Nature": 1, "Relax": 0.5, "City": 0.5},
            "Winter": {"Nature": 1, "Relax": 0.5, "City": 0.5}
        }
    }
] 