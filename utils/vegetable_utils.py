import json
import os
from config import VEGETABLES_FILE

def load_vegetables():
    """Load vegetable data from JSON file"""
    if os.path.exists(VEGETABLES_FILE):
        with open(VEGETABLES_FILE, 'r') as f:
            return json.load(f)
    return {
        "potato": {"quantity": 0, "weight": 0.0},
        "onion": {"quantity": 0, "weight": 0.0},
        "tomato": {"quantity": 0, "weight": 0.0}
    }

def save_vegetables(vegetables):
    """Save vegetable data to JSON file"""
    with open(VEGETABLES_FILE, 'w') as f:
        json.dump(vegetables, f, indent=2)

def update_vegetable_data(potato_qty, potato_weight, onion_qty, onion_weight, tomato_qty, tomato_weight):
    """Update all vegetable data"""
    vegetables = {
        "potato": {"quantity": int(potato_qty), "weight": float(potato_weight)},
        "onion": {"quantity": int(onion_qty), "weight": float(onion_weight)},
        "tomato": {"quantity": int(tomato_qty), "weight": float(tomato_weight)}
    }
    save_vegetables(vegetables)
    return vegetables
