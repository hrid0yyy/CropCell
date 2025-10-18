import json
import os
# from config import VEGETABLES_FILE
from config import FIRESTORE_DB

DEFAULT_VEG = {
    "potato": {"quantity": 0, "weight": 0.0},
    "onion": {"quantity": 0, "weight": 0.0},
    "tomato": {"quantity": 0, "weight": 0.0}
}

def load_vegetables():
    """Load vegetable data from Firestore."""
    if FIRESTORE_DB is None:
        return DEFAULT_VEG
    data = {**DEFAULT_VEG}
    try:
        for name in ["potato", "onion", "tomato"]:
            ref = FIRESTORE_DB.collection("vegetables").document(name)
            snap = ref.get()
            if snap.exists:
                row = snap.to_dict() or {}
                data[name] = {
                    "quantity": int(row.get("quantity") or 0),
                    "weight": float(row.get("weight") or 0.0),
                }
            else:
                ref.set(data[name])
        return data
    except Exception:
        return DEFAULT_VEG

def save_vegetables(vegetables):
    """Persist vegetables dict to Firestore."""
    if FIRESTORE_DB is None:
        return
    try:
        for name in ["potato", "onion", "tomato"]:
            FIRESTORE_DB.collection("vegetables").document(name).set({
                "quantity": int(vegetables[name]["quantity"]),
                "weight": float(vegetables[name]["weight"]),
            })
    except Exception:
        pass

def update_vegetable_data(potato_qty, potato_weight, onion_qty, onion_weight, tomato_qty, tomato_weight):
    """Update all vegetable data in Firestore."""
    vegetables = {
        "potato": {"quantity": int(potato_qty), "weight": float(potato_weight)},
        "onion": {"quantity": int(onion_qty), "weight": float(onion_weight)},
        "tomato": {"quantity": int(tomato_qty), "weight": float(tomato_weight)}
    }
    save_vegetables(vegetables)
    return vegetables
