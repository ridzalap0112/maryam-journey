# =============================================================
#  scripts/locations/MasjidScene.gd
#  Scene interior Masjid An-Nur — Belajar Hijaiyah
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

# 28 huruf Hijaiyah lengkap
const HIJAIYAH : Array = [
	{"arab": "ا", "nama": "Alif",  "warna": Color(0.95,0.30,0.30,1)},
	{"arab": "ب", "nama": "Ba",    "warna": Color(0.95,0.50,0.20,1)},
	{"arab": "ت", "nama": "Ta",    "warna": Color(0.95,0.75,0.15,1)},
	{"arab": "ث", "nama": "Tsa",   "warna": Color(0.60,0.85,0.25,1)},
	{"arab": "ج", "nama": "Jim",   "warna": Color(0.20,0.78,0.45,1)},
	{"arab": "ح", "nama": "Ha",    "warna": Color(0.15,0.75,0.75,1)},
	{"arab": "خ", "nama": "Kha",   "warna": Color(0.20,0.55,0.95,1)},
	{"arab": "د", "nama": "Dal",   "warna": Color(0.40,0.30,0.90,1)},
	{"arab": "ذ", "nama": "Dzal",  "warna": Color(0.65,0.25,0.90,1)},
	{"arab": "ر", "nama": "Ra",    "warna": Color(0.90,0.25,0.65,1)},
	{"arab": "ز", "nama": "Zai",   "warna": Color(0.95,0.30,0.30,1)},
	{"arab": "س", "nama": "Sin",   "warna": Color(0.95,0.55,0.18,1)},
	{"arab": "ش", "nama": "Syin",  "warna": Color(0.90,0.78,0.12,1)},
	{"arab": "ص", "nama": "Shad",  "warna": Color(0.55,0.88,0.20,1)},
	{"arab": "ض", "nama": "Dhad",  "warna": Color(0.18,0.80,0.48,1)},
	{"arab": "ط", "nama": "Tha",   "warna": Color(0.12,0.78,0.78,1)},
	{"arab": "ظ", "nama": "Zha",   "warna": Color(0.18,0.58,0.95,1)},
	{"arab": "ع", "nama": "Ain",   "warna": Color(0.38,0.28,0.92,1)},
	{"arab": "غ", "nama": "Ghain", "warna": Color(0.62,0.22,0.92,1)},
	{"arab": "ف", "nama": "Fa",    "warna": Color(0.92,0.22,0.62,1)},
	{"arab": "ق", "nama": "Qaf",   "warna": Color(0.95,0.32,0.32,1)},
	{"arab": "ك", "nama": "Kaf",   "warna": Color(0.95,0.52,0.18,1)},
	{"arab": "ل", "nama": "Lam",   "warna": Color(0.88,0.80,0.10,1)},
	{"arab": "م", "nama": "Mim",   "warna": Color(0.52,0.88,0.18,1)},
	{"arab": "ن", "nama": "Nun",   "warna": Color(0.15,0.82,0.50,1)},
	{"arab": "و", "nama": "Wau",   "warna": Color(0.12,0.80,0.80,1)},
	{"arab": "ه", "nama": "Ha",    "warna": Color(0.18,0.60,0.95,1)},
	{"arab": "ي", "nama": "Ya",    "warna": Color(0.60,0.22,0.92,1)},
]

# State
var _total_kartu    : int  = 28
var _sudah_diklik   : int  = 0
var _kartu_selesai  : Array = []
var _selesai_semua  : bool = false

# Node refs
@onready var _kartu_container : GridContainer = $UI/Scroll/Grid
@onready var _lbl_progress    : Label         = $UI/TopBar/LblProgress
@onready var _lbl_nama        : Label         = $UI/NamaPanel/LblNama
@onready var _btn_back        : Button        = $UI/TopBar/BtnBack
@onready var _panel_selesai   : Panel         = $UI/PanelSelesai
@onready var _btn_keluar      : Button        = $UI/PanelSelesai/VBox/BtnKeluar


func _ready() -> void:
	_lbl_progress.text  = "0 / 28 huruf"
	_lbl_nama.text      = "Sentuh huruf untuk belajar!"
	_panel_selesai.visible = false
	_btn_back.pressed.connect(_on_back)
	_btn_keluar.pressed.connect(_on_back)
	_build_kartu()


func _build_kartu() -> void:
	for i in HIJAIYAH.size():
		var data   : Dictionary = HIJAIYAH[i]
		var btn    := Button.new()
		var idx    := i

		btn.custom_minimum_size = Vector2(90, 90)
		btn.text                = data["arab"]
		btn.tooltip_text        = data["nama"]

		# Style normal
		var sb_normal := StyleBoxFlat.new()
		sb_normal.bg_color             = data["warna"]
		sb_normal.corner_radius_top_left    = 14
		sb_normal.corner_radius_top_right   = 14
		sb_normal.corner_radius_bottom_left = 14
		sb_normal.corner_radius_bottom_right= 14
		sb_normal.border_width_left   = 3
		sb_normal.border_width_top    = 3
		sb_normal.border_width_right  = 3
		sb_normal.border_width_bottom = 3
		sb_normal.border_color        = Color(1,1,1,0.40)
		sb_normal.content_margin_left   = 4
		sb_normal.content_margin_right  = 4
		sb_normal.content_margin_top    = 4
		sb_normal.content_margin_bottom = 4

		# Style sudah diklik (lebih gelap)
		var sb_done := StyleBoxFlat.new()
		sb_done.bg_color = Color(
			data["warna"].r * 0.55,
			data["warna"].g * 0.55,
			data["warna"].b * 0.55,
			1.0
		)
		sb_done.corner_radius_top_left    = 14
		sb_done.corner_radius_top_right   = 14
		sb_done.corner_radius_bottom_left = 14
		sb_done.corner_radius_bottom_right= 14
		sb_done.border_width_left   = 3
		sb_done.border_width_top    = 3
		sb_done.border_width_right  = 3
		sb_done.border_width_bottom = 3
		sb_done.border_color        = Color(1,1,1,0.80)

		btn.add_theme_stylebox_override("normal",   sb_normal)
		btn.add_theme_stylebox_override("hover",    sb_done)
		btn.add_theme_stylebox_override("pressed",  sb_done)
		btn.add_theme_font_size_override("font_size", 36)
		btn.add_theme_color_override("font_color", Color(1,1,1,1))

		btn.pressed.connect(func(): _on_kartu_pressed(idx, btn, sb_done))
		_kartu_container.add_child(btn)


func _on_kartu_pressed(idx: int, btn: Button, sb_done: StyleBoxFlat) -> void:
	if _selesai_semua:
		return
	var data : Dictionary = HIJAIYAH[idx]
	AudioManager.play_sfx("click")
	_lbl_nama.text = data["arab"] + "  —  " + data["nama"]

	# Tandai selesai jika belum
	if idx not in _kartu_selesai:
		_kartu_selesai.append(idx)
		_sudah_diklik += 1
		btn.add_theme_stylebox_override("normal", sb_done)
		# Tambah centang kecil
		var lbl_check := Label.new()
		lbl_check.text = "✓"
		lbl_check.add_theme_font_size_override("font_size", 14)
		lbl_check.add_theme_color_override("font_color", Color(1,1,1,0.9))
		lbl_check.position = Vector2(66, 4)
		btn.add_child(lbl_check)
		_lbl_progress.text = str(_sudah_diklik) + " / 28 huruf"

	if _sudah_diklik >= _total_kartu and not _selesai_semua:
		_selesai_semua = true
		await get_tree().create_timer(0.5).timeout
		_show_selesai()


func _show_selesai() -> void:
	AudioManager.play_sfx("star")
	GameManager.add_star(3)
	_panel_selesai.visible = true


func _on_back() -> void:
	TransitionManager.go_to(WORLD_SCENE)
