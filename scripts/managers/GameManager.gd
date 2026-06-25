# =============================================================
#  scripts/managers/GameManager.gd
#  Autoload — tersedia di seluruh scene
# =============================================================
extends Node

var player_name        : String = "Maryam"
var total_stars        : int    = 0
var unlocked_locations : Array  = ["masjid"]

signal star_collected(total: int)
signal location_unlocked(location_name: String)


func _ready() -> void:
	print("[MaryamJourney] Assalamu'alaikum! Game dimulai.")


func add_star(amount: int = 1) -> void:
	total_stars += amount
	star_collected.emit(total_stars)
	print("[MaryamJourney] Bintang: ", total_stars)


func unlock_location(location_name: String) -> void:
	if location_name not in unlocked_locations:
		unlocked_locations.append(location_name)
		location_unlocked.emit(location_name)
		print("[MaryamJourney] Lokasi terbuka: ", location_name)


func is_location_unlocked(location_name: String) -> bool:
	return location_name in unlocked_locations
