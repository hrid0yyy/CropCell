import json
import os
from config import RFID_CARDS_FILE, REDIS

def load_rfid_cards():
	"""Load verified RFID cards"""
	if REDIS:
		try:
			return sorted(list(REDIS.smembers("rfid_cards")))
		except Exception:
			pass
	if os.path.exists(RFID_CARDS_FILE):
		with open(RFID_CARDS_FILE, 'r') as f:
			return json.load(f)
	return []

def save_rfid_cards(cards):
	"""Persist RFID cards (JSON fallback only)"""
	with open(RFID_CARDS_FILE, 'w') as f:
		json.dump(cards, f, indent=2)

def add_rfid_card(rfid_number):
	"""Add a new RFID card"""
	if REDIS:
		try:
			return REDIS.sadd("rfid_cards", rfid_number) == 1
		except Exception:
			pass
	cards = load_rfid_cards()
	if rfid_number not in cards:
		cards.append(rfid_number)
		save_rfid_cards(cards)
		return True
	return False

def remove_rfid_card(rfid_number):
	"""Remove an RFID card"""
	if REDIS:
		try:
			REDIS.srem("rfid_cards", rfid_number)
			return True
		except Exception:
			return False
	cards = load_rfid_cards()
	if rfid_number in cards:
		cards.remove(rfid_number)
		save_rfid_cards(cards)
		return True
	return False

def is_rfid_verified(rfid_number):
	"""Check if RFID card is verified"""
	if REDIS:
		try:
			return bool(REDIS.sismember("rfid_cards", rfid_number))
		except Exception:
			pass
	cards = load_rfid_cards()
	return rfid_number in cards
