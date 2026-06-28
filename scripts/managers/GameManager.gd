extends Node

var player_name        : String = "Maryam"
var total_stars        : int    = 0
var unlocked_locations : Array  = ["masjid","pondok","taman","kebun","rumah"]

signal star_collected(total: int)
signal location_unlocked(location_name: String)


func _ready() -> void:
	print("[MaryamJourney] Assalamu'alaikum!")


func add_star(amount: int = 1) -> void:
	total_stars += amount
	star_collected.emit(total_stars)
	SaveManager.save()


func unlock_location(loc: String) -> void:
	if loc not in unlocked_locations:
		unlocked_locations.append(loc)
		location_unlocked.emit(loc)
		SaveManager.save()


func is_location_unlocked(loc: String) -> bool:
	return loc in unlocked_locations
