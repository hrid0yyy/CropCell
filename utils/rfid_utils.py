import json
import os
from datetime import datetime
from config import FIRESTORE_DB

def load_rfid_cards():
    """Load verified RFID cards from Firestore."""
    if FIRESTORE_DB is None:
        return []
    try:
        docs = FIRESTORE_DB.collection("rfid_cards").stream()
        return [doc.id for doc in docs]
    except Exception:
        return []

def save_rfid_cards(cards):
    """No-op retained for compatibility (Firestore used instead)."""
    pass

def add_rfid_card(rfid_number):
    """Add a new RFID card to Firestore."""
    if FIRESTORE_DB is None:
        return False
    try:
        doc_ref = FIRESTORE_DB.collection("rfid_cards").document(rfid_number)
        if doc_ref.get().exists:
            return False
        doc_ref.set({"rfid_number": rfid_number, "created_at": datetime.utcnow().isoformat()})
        return True
    except Exception:
        return False

def remove_rfid_card(rfid_number):
    """Remove an RFID card from Firestore."""
    if FIRESTORE_DB is None:
        return False
    try:
        FIRESTORE_DB.collection("rfid_cards").document(rfid_number).delete()
        return True
    except Exception:
        return False

def is_rfid_verified(rfid_number):
    """Check if RFID card is verified via Firestore."""
    if FIRESTORE_DB is None:
        return False
    try:
        return FIRESTORE_DB.collection("rfid_cards").document(rfid_number).get().exists
    except Exception:
        return False
