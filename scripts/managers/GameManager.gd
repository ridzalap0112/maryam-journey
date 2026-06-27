# =============================================================
#  scripts/managers/GameManager.gd
#  Autoload global
# =============================================================
extends Node

var player_name        : String = "Maryam"
var total_stars        : int    = 0
var unlocked_locations : Array  = ["masjid", "pondok", "taman", "kebun", "rumah"]

signal star_collected(total: int)
signal location_unlocked(location_name: String)


func _ready() -> void:
	print("[MaryamJourney] Assalamu'alaikum!")


func add_star(amount: int = 1) -> void:
	total_stars += amount
	star_collected.emit(total_stars)
	SaveManager.save()


func unlock_location(location_name: String) -> void:
	if location_name not in unlocked_locations:
		unlocked_locations.append(location_name)
		location_unlocked.emit(location_name)
		SaveManager.save()


func is_location_unlocked(location_name: String) -> bool:
	return location_name in unlocked_locations
