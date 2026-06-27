# =============================================================
#  scripts/managers/SaveManager.gd
#  Autoload — simpan & load progress ke file JSON
#  Daftarkan di: Project > Autoload > SaveManager
# =============================================================
extends Node

const SAVE_PATH : String = "user://maryam_save.json"


func save() -> void:
	var data : Dictionary = {
		"player_name"        : GameManager.player_name,
		"total_stars"        : GameManager.total_stars,
		"unlocked_locations" : GameManager.unlocked_locations,
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(data, "	"))
		file.close()
		print("[Save] Progress tersimpan.")
	else:
		push_error("[Save] Gagal menyimpan: " + SAVE_PATH)


func load_save() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		print("[Save] Belum ada save file.")
		return false
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not file:
		push_error("[Save] Gagal membuka save file.")
		return false
	var raw  : String     = file.get_as_text()
	file.close()
	var json := JSON.new()
	if json.parse(raw) != OK:
		push_error("[Save] JSON rusak, save dihapus.")
		delete_save()
		return false
	var data : Dictionary = json.get_data()
	GameManager.player_name        = data.get("player_name", "Maryam")
	GameManager.total_stars        = data.get("total_stars", 0)
	GameManager.unlocked_locations = data.get("unlocked_locations",
		["masjid", "pondok", "taman", "kebun", "rumah"])
	print("[Save] Progress dimuat. Bintang: ", GameManager.total_stars)
	return true


func delete_save() -> void:
	if FileAccess.file_exists(SAVE_PATH):
		DirAccess.remove_absolute(SAVE_PATH)
		print("[Save] Save file dihapus.")


func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)
