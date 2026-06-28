extends Node

const SAVE_PATH : String = "user://maryam_save.json"


func save() -> void:
	var data := {
		"player_name"        : GameManager.player_name,
		"total_stars"        : GameManager.total_stars,
		"unlocked_locations" : GameManager.unlocked_locations,
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(data))
		file.close()


func load_save() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		return false
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not file:
		return false
	var raw  := file.get_as_text()
	file.close()
	var json := JSON.new()
	if json.parse(raw) != OK:
		delete_save()
		return false
	var data : Dictionary = json.get_data()
	GameManager.player_name        = data.get("player_name", "Maryam")
	GameManager.total_stars        = data.get("total_stars", 0)
	GameManager.unlocked_locations = data.get("unlocked_locations", ["masjid","pondok","taman","kebun","rumah"])
	return true


func delete_save() -> void:
	if FileAccess.file_exists(SAVE_PATH):
		DirAccess.remove_absolute(SAVE_PATH)


func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)
