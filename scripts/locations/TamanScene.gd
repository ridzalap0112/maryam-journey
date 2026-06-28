# =============================================================
#  scripts/locations/TamanScene.gd
#  Taman Logika — Cocokkan warna & bentuk
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

# Soal: cocokkan nama warna dengan warna yang benar
const SOAL : Array[Dictionary] = [
	{"nama": "MERAH",   "warna": Color(0.92, 0.20, 0.20, 1), "salah": [Color(0.20,0.55,0.92,1), Color(0.20,0.82,0.35,1), Color(0.92,0.78,0.10,1)]},
	{"nama": "BIRU",    "warna": Color(0.20, 0.50, 0.92, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.82,0.45,0.10,1), Color(0.55,0.20,0.82,1)]},
	{"nama": "HIJAU",   "warna": Color(0.15, 0.78, 0.35, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.92,0.78,0.10,1)]},
	{"nama": "KUNING",  "warna": Color(0.95, 0.82, 0.10, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.55,0.20,0.82,1)]},
	{"nama": "UNGU",    "warna": Color(0.55, 0.18, 0.85, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.15,0.78,0.35,1), Color(0.92,0.78,0.10,1)]},
	{"nama": "ORANYE",  "warna": Color(0.95, 0.52, 0.10, 1), "salah": [Color(0.20,0.50,0.92,1), Color(0.15,0.78,0.35,1), Color(0.55,0.18,0.85,1)]},
	{"nama": "PINK",    "warna": Color(0.95, 0.35, 0.65, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.95,0.52,0.10,1)]},
	{"nama": "COKLAT",  "warna": Color(0.55, 0.32, 0.12, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.15,0.78,0.35,1), Color(0.95,0.35,0.65,1)]},
]

var _idx_soal    : int  = 0
var _benar       : int  = 0
var _selesai     : bool = false

@onready var _lbl_soal      : Label  = $UI/SoalPanel/LblSoal
@onready var _lbl_warna     : Label  = $UI/SoalPanel/LblWarna
@onready var _kotak_soal    : Panel  = $UI/SoalPanel/KotakWarna
@onready var _lbl_progress  : Label  = $UI/TopBar/LblProgress
@onready var _lbl_feedback  : Label  = $UI/LblFeedback
@onready var _btn_back      : Button = $UI/TopBar/BtnBack
@onready var _panel_selesai : Panel  = $UI/PanelSelesai
@onready var _btn_keluar    : Button = $UI/PanelSelesai/VBox/BtnKeluar
@onready var _pilihan_box   : HBoxContainer = $UI/PilihanBox


func _ready() -> void:
	_panel_selesai.visible = false
	_lbl_feedback.visible  = false
	_btn_back.pressed.connect(_on_back)
	_btn_keluar.pressed.connect(_on_back)
	_tampil_soal()


func _tampil_soal() -> void:
	if _idx_soal >= SOAL.size():
		_selesai_semua()
		return

	var soal : Dictionary = SOAL[_idx_soal]
	_lbl_soal.text = "Pilih warna:"
	_lbl_warna.text = soal["nama"]
	_lbl_warna.add_theme_color_override("font_color", soal["warna"])
	_lbl_progress.text = str(_idx_soal + 1) + " / " + str(SOAL.size())
	_lbl_feedback.visible = false

	# Bersihkan pilihan lama
	for child in _pilihan_box.get_children():
		child.queue_free()

	# Buat 4 pilihan (1 benar + 3 salah) dan acak urutannya
	var semua : Array[Dictionary] = []
	semua.append({"warna": soal["warna"], "benar": true})
	for w : Color in soal["salah"]:
		semua.append({"warna": w, "benar": false})
	semua.shuffle()

	for item : Dictionary in semua:
		var btn     : Button       = Button.new()
		var w       : Color        = item["warna"]
		var is_benar : bool        = item["benar"]
		var sb      : StyleBoxFlat = StyleBoxFlat.new()
		sb.bg_color                   = w
		sb.corner_radius_top_left     = 20
		sb.corner_radius_top_right    = 20
		sb.corner_radius_bottom_left  = 20
		sb.corner_radius_bottom_right = 20
		sb.border_width_left          = 4
		sb.border_width_top           = 4
		sb.border_width_right         = 4
		sb.border_width_bottom        = 4
		sb.border_color               = Color(1,1,1,0.40)
		sb.shadow_color               = Color(0,0,0,0.30)
		sb.shadow_size                = 6
		btn.custom_minimum_size = Vector2(140, 140)
		btn.add_theme_stylebox_override("normal",  sb)
		btn.add_theme_stylebox_override("hover",   sb)
		btn.add_theme_stylebox_override("pressed", sb)
		btn.pressed.connect(func(): _on_pilih(is_benar))
		_pilihan_box.add_child(btn)


func _on_pilih(is_benar: bool) -> void:
	if _selesai:
		return
	_lbl_feedback.visible = true
	if is_benar:
		_benar += 1
		_lbl_feedback.text = "✅  Betul! Hebat Maryam!"
		_lbl_feedback.add_theme_color_override("font_color", Color(0.20, 0.90, 0.40, 1))
	else:
		_lbl_feedback.text = "❌  Coba lagi ya!"
		_lbl_feedback.add_theme_color_override("font_color", Color(0.95, 0.35, 0.35, 1))
	await get_tree().create_timer(0.8).timeout
	_idx_soal += 1
	_tampil_soal()


func _selesai_semua() -> void:
	_selesai = true
	GameManager.add_star(3)
	_panel_selesai.visible = true
	$UI/PanelSelesai/VBox/LblSkor.text = "Benar: " + str(_benar) + " / " + str(SOAL.size())


func _on_back() -> void:
	TransitionManager.go_to(WORLD_SCENE)
