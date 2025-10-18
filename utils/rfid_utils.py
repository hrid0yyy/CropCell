import json
import os
from config import RFID_CARDS_FILE, REDIS, SUPABASE

def load_rfid_cards():
    """Load verified RFID cards from Supabase."""
    if SUPABASE is None:
        return []
    try:
        res = SUPABASE.table("rfid_cards").select("rfid_number").execute()
        data = res.data or []
        return sorted([row["rfid_number"] for row in data])
    except Exception:
        return []

def save_rfid_cards(cards):
    """Persist RFID cards (JSON fallback only)"""
    with open(RFID_CARDS_FILE, 'w') as f:
        json.dump(cards, f, indent=2)

def add_rfid_card(rfid_number: str):
    """Add a new RFID card to Supabase."""
    if SUPABASE is None:
        return False
    try:
        exists = SUPABASE.table("rfid_cards").select("rfid_number").eq("rfid_number", rfid_number).limit(1).execute()
        if exists.data:
            return False
        SUPABASE.table("rfid_cards").insert({"rfid_number": rfid_number}).execute()
        return True
    except Exception:
        return False

def remove_rfid_card(rfid_number: str):
    """Remove an RFID card from Supabase."""
    if SUPABASE is None:
        return False
    try:
        SUPABASE.table("rfid_cards").delete().eq("rfid_number", rfid_number).execute()
        return True
    except Exception:
        return False

def is_rfid_verified(rfid_number: str):
    """Check if RFID card is verified via Supabase."""
    if SUPABASE is None:
        return False
    try:
        res = SUPABASE.table("rfid_cards").select("rfid_number").eq("rfid_number", rfid_number).limit(1).execute()
        return bool(res.data)
    except Exception:
        return False
