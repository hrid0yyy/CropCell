import json
import os
from config import SUPABASE, VEGETABLES_FILE

DEFAULT_VEG = {
    "potato": {"quantity": 0, "weight": 0.0},
    "onion": {"quantity": 0, "weight": 0.0},
    "tomato": {"quantity": 0, "weight": 0.0}
}

def load_vegetables():
    """Load all vegetable data (dynamic). Uses Supabase when available, else JSON fallback."""
    if SUPABASE is None:
        try:
            if os.path.exists(VEGETABLES_FILE):
                with open(VEGETABLES_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f) or {}
                # normalize
                norm = {}
                for name, v in (data.items() if isinstance(data, dict) else []):
                    if not name:
                        continue
                    q = int((v or {}).get("quantity") or 0)
                    w = float((v or {}).get("weight") or 0.0)
                    norm[name] = {"quantity": q, "weight": w}
                return norm or DEFAULT_VEG
        except Exception:
            return DEFAULT_VEG
        return DEFAULT_VEG

    try:
        res = SUPABASE.table("vegetables").select("name,quantity,weight").order("name").execute()
        rows = res.data or []
        data = {}
        for row in rows:
            name = (row.get("name") or "").strip()
            if not name:
                continue
            data[name] = {
                "quantity": int(row.get("quantity") or 0),
                "weight": float(row.get("weight") or 0.0),
            }
        return data
    except Exception:
        return DEFAULT_VEG

def save_vegetables(vegetables):
    """Persist vegetables dict to Supabase (or JSON fallback)."""
    if SUPABASE is None:
        try:
            os.makedirs(os.path.dirname(VEGETABLES_FILE), exist_ok=True)
            with open(VEGETABLES_FILE, "w", encoding="utf-8") as f:
                json.dump(vegetables, f, indent=2)
        except Exception:
            pass
        return

    try:
        rows = []
        for name, v in (vegetables or {}).items():
            if not name:
                continue
            rows.append({
                "name": name,
                "quantity": int((v or {}).get("quantity") or 0),
                "weight": float((v or {}).get("weight") or 0.0),
            })
        if rows:
            SUPABASE.table("vegetables").upsert(rows, on_conflict="name").execute()
    except Exception:
        pass

def update_vegetable_data(*args, **kwargs):
    """
    Update vegetable data.
    - New usage: update_vegetable_data({"carrot": {"quantity": 3, "weight": 1.2}, ...})
    - Legacy usage: update_vegetable_data(pq,pw,oq,ow,tq,tw)
    """
    # New dynamic form
    if args and isinstance(args[0], dict):
        raw = args[0] or {}
        vegetables = {}
        for name, v in raw.items():
            if not name:
                continue
            q = int((v or {}).get("quantity") or 0)
            w = float((v or {}).get("weight") or 0.0)
            vegetables[name] = {"quantity": q, "weight": w}
        save_vegetables(vegetables)
        return vegetables

    # Legacy fixed-args fallback
    try:
        potato_qty, potato_weight, onion_qty, onion_weight, tomato_qty, tomato_weight = args[:6]
    except Exception:
        return {}
    vegetables = {
        "potato": {"quantity": int(potato_qty), "weight": float(potato_weight)},
        "onion": {"quantity": int(onion_qty), "weight": float(onion_weight)},
        "tomato": {"quantity": int(tomato_qty), "weight": float(tomato_weight)}
    }
    save_vegetables(vegetables)
    return vegetables

def increment_vegetable(name: str, qty_inc: int, weight_inc: float):
    """Increment (or create) a vegetable row by name."""
    if SUPABASE is None:
        # Fallback: update JSON directly
        data = load_vegetables()
        name = (name or "").strip().lower()
        if not name:
            return None
        curr = data.get(name, {"quantity": 0, "weight": 0.0})
        new_q = int(curr.get("quantity", 0)) + int(qty_inc or 0)
        new_w = float(curr.get("weight", 0.0)) + float(weight_inc or 0.0)
        data[name] = {"quantity": new_q, "weight": new_w}
        save_vegetables(data)
        return {"name": name, "quantity": new_q, "weight": new_w}

    try:
        name = (name or "").strip().lower()
        if not name:
            return None

        # Get current values
        res = SUPABASE.table("vegetables").select("name,quantity,weight").eq("name", name).limit(1).execute()
        rows = res.data or []
        if rows:
            curr_q = int(rows[0].get("quantity") or 0)
            curr_w = float(rows[0].get("weight") or 0.0)
        else:
            curr_q = 0
            curr_w = 0.0

        new_q = curr_q + int(qty_inc or 0)
        new_w = curr_w + float(weight_inc or 0.0)

        # Upsert updated/new row
        SUPABASE.table("vegetables").upsert(
            {"name": name, "quantity": new_q, "weight": new_w},
            on_conflict="name"
        ).execute()

        return {"name": name, "quantity": new_q, "weight": new_w}
    except Exception:
        return None
