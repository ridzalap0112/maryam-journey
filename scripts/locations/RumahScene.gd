# =============================================================
#  scripts/locations/RumahScene.gd
#  Rumah Maryam — Progress & koleksi bintang
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

const LOKASI_INFO : Array[Dictionary] = [
	{"nama": "🕌 Masjid An-Nur",  "key": "masjid", "maks": 3},
	{"nama": "📚 Pondok Baca",    "key": "pondok", "maks": 3},
	{"nama": "🧩 Taman Logika",   "key": "taman",  "maks": 3},
	{"nama": "🌿 Kebun Karakter", "key": "kebun",  "maks": 3},
]

@onready var _lbl_nama      : Label  = $UI/Card/LblNama
@onready var _lbl_total     : Label  = $UI/Card/LblTotal
@onready var _lbl_pesan     : Label  = $UI/Card/LblPesan
@onready var _vbox_lokasi   : VBoxContainer = $UI/Card/VBoxLokasi
@onready var _btn_back      : Button = $UI/TopBar/BtnBack


func _ready() -> void:
	_btn_back.pressed.connect(_on_back)
	_build_ui()


func _build_ui() -> void:
	var total : int = GameManager.total_stars
	_lbl_nama.text  = "Assalamu'alaikum, " + GameManager.player_name + "! 🌙"
	_lbl_total.text = "⭐  Total Bintang: " + str(total)

	if total >= 12:
		_lbl_pesan.text = "Subhanallah! Kamu sudah menyelesaikan semuanya! 🏆"
		_lbl_pesan.add_theme_color_override("font_color", Color(1.0, 0.85, 0.10, 1))
	elif total >= 6:
		_lbl_pesan.text = "Alhamdulillah! Terus semangat belajar ya! 💪"
		_lbl_pesan.add_theme_color_override("font_color", Color(0.55, 0.95, 0.55, 1))
	else:
		_lbl_pesan.text = "Bismillah! Ayo mulai petualangan belajar! 🌟"
		_lbl_pesan.add_theme_color_override("font_color", Color(0.80, 0.85, 1.0, 1))

	# Bersihkan dulu
	for c in _vbox_lokasi.get_children():
		c.queue_free()

	# Tampilkan progress tiap lokasi
	for info : Dictionary in LOKASI_INFO:
		var row : HBoxContainer = HBoxContainer.new()
		row.custom_minimum_size = Vector2(0, 48)

		var lbl_nama : Label = Label.new()
		lbl_nama.text = info["nama"]
		lbl_nama.custom_minimum_size = Vector2(280, 0)
		lbl_nama.add_theme_font_size_override("font_size", 16)
		lbl_nama.add_theme_color_override("font_color", Color(0.90, 0.94, 1.0, 1))
		lbl_nama.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

		var lbl_stars : Label = Label.new()
		var bintang_lokasi : int = _hitung_bintang(info["key"])
		var bintang_str    : String = ""
		for s in info["maks"]:
			if s < bintang_lokasi:
				bintang_str += "⭐"
			else:
				bintang_str += "☆"
		lbl_stars.text = bintang_str
		lbl_stars.add_theme_font_size_override("font_size", 22)
		lbl_stars.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

		row.add_child(lbl_nama)
		row.add_child(lbl_stars)
		_vbox_lokasi.add_child(row)


func _hitung_bintang(key: String) -> int:
	# Sederhana: kalau sudah pernah masuk lokasi, dapat 3 bintang
	# Nanti bisa dikembangkan dengan tracking per lokasi
	if GameManager.total_stars > 0:
		match key:
			"masjid": return 3 if GameManager.total_stars >= 3 else 0
			"pondok": return 3 if GameManager.total_stars >= 6 else 0
			"taman":  return 3 if GameManager.total_stars >= 9 else 0
			"kebun":  return 3 if GameManager.total_stars >= 12 else 0
	return 0


func _on_back() -> void:
	TransitionManager.go_to(WORLD_SCENE)
