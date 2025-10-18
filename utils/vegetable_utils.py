from config import SUPABASE

DEFAULT_VEG = {
    "potato": {"quantity": 0, "weight": 0.0},
    "onion": {"quantity": 0, "weight": 0.0},
    "tomato": {"quantity": 0, "weight": 0.0}
}

def load_vegetables():
    """Load vegetable data from Supabase and ensure defaults exist."""
    if SUPABASE is None:
        return DEFAULT_VEG
    try:
        names = ["potato", "onion", "tomato"]
        res = SUPABASE.table("vegetables").select("name,quantity,weight").in_("name", names).execute()
        data = {**DEFAULT_VEG}
        rows = res.data or []
        for row in rows:
            n = row.get("name")
            if n in data:
                data[n] = {
                    "quantity": int(row.get("quantity") or 0),
                    "weight": float(row.get("weight") or 0.0),
                }
        # Upsert missing defaults
        missing = []
        present = {r.get("name") for r in rows}
        for n in names:
            if n not in present:
                missing.append({"name": n, **data[n]})
        if missing:
            SUPABASE.table("vegetables").upsert(missing, on_conflict="name").execute()
        return data
    except Exception:
        return DEFAULT_VEG

def save_vegetables(vegetables):
    """Persist vegetables dict to Supabase."""
    if SUPABASE is None:
        return
    rows = [
        {"name": "potato", "quantity": int(vegetables["potato"]["quantity"]), "weight": float(vegetables["potato"]["weight"])},
        {"name": "onion", "quantity": int(vegetables["onion"]["quantity"]), "weight": float(vegetables["onion"]["weight"])},
        {"name": "tomato", "quantity": int(vegetables["tomato"]["quantity"]), "weight": float(vegetables["tomato"]["weight"])},
    ]
    try:
        SUPABASE.table("vegetables").upsert(rows, on_conflict="name").execute()
    except Exception:
        pass

def update_vegetable_data(potato_qty, potato_weight, onion_qty, onion_weight, tomato_qty, tomato_weight):
    """Update all vegetable data in Supabase."""
    vegetables = {
        "potato": {"quantity": int(potato_qty), "weight": float(potato_weight)},
        "onion": {"quantity": int(onion_qty), "weight": float(onion_weight)},
        "tomato": {"quantity": int(tomato_qty), "weight": float(tomato_weight)}
    }
    save_vegetables(vegetables)
    return vegetables
