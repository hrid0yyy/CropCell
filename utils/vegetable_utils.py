import json
import os
from config import VEGETABLES_FILE, REDIS

DEFAULT_VEG = {
    "potato": {"quantity": 0, "weight": 0.0},
    "onion": {"quantity": 0, "weight": 0.0},
    "tomato": {"quantity": 0, "weight": 0.0}
}

def load_vegetables():
    """Load vegetable data (Redis or JSON)"""
    if REDIS:
        try:
            data_str = REDIS.get("vegetables")
            if data_str:
                return json.loads(data_str)
            REDIS.set("vegetables", json.dumps(DEFAULT_VEG))
            return DEFAULT_VEG
        except Exception:
            pass
    if os.path.exists(VEGETABLES_FILE):
        with open(VEGETABLES_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_VEG

def save_vegetables(vegetables):
    """Save vegetable data (Redis or JSON)"""
    if REDIS:
        try:
            REDIS.set("vegetables", json.dumps(vegetables))
            return
        except Exception:
            pass
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
