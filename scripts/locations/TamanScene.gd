# =============================================================
#  scripts/locations/TamanScene.gd
#  Taman Logika — Warna & Angka
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

# ── Data Warna ───────────────────────────────────────────────
const SOAL_WARNA : Array[Dictionary] = [
	{"nama": "MERAH",  "warna": Color(0.92,0.20,0.20,1), "salah": [Color(0.20,0.55,0.92,1), Color(0.20,0.82,0.35,1), Color(0.92,0.78,0.10,1)]},
	{"nama": "BIRU",   "warna": Color(0.20,0.50,0.92,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.82,0.45,0.10,1), Color(0.55,0.20,0.82,1)]},
	{"nama": "HIJAU",  "warna": Color(0.15,0.78,0.35,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.92,0.78,0.10,1)]},
	{"nama": "KUNING", "warna": Color(0.95,0.82,0.10,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.55,0.20,0.82,1)]},
	{"nama": "UNGU",   "warna": Color(0.55,0.18,0.85,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.15,0.78,0.35,1), Color(0.92,0.78,0.10,1)]},
	{"nama": "ORANYE", "warna": Color(0.95,0.52,0.10,1), "salah": [Color(0.20,0.50,0.92,1), Color(0.15,0.78,0.35,1), Color(0.55,0.18,0.85,1)]},
	{"nama": "PINK",   "warna": Color(0.95,0.35,0.65,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.95,0.52,0.10,1)]},
	{"nama": "COKLAT", "warna": Color(0.55,0.32,0.12,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.15,0.78,0.35,1), Color(0.95,0.35,0.65,1)]},
]

# ── Data Angka ───────────────────────────────────────────────
const ANGKA : Array[Dictionary] = [
	{"angka": 1,  "arab": "١", "emoji": "🌙",  "nama": "Satu"},
	{"angka": 2,  "arab": "٢", "emoji": "⭐⭐", "nama": "Dua"},
	{"angka": 3,  "arab": "٣", "emoji": "🍎🍎🍎", "nama": "Tiga"},
	{"angka": 4,  "arab": "٤", "emoji": "🐟🐟🐟🐟", "nama": "Empat"},
	{"angka": 5,  "arab": "٥", "emoji": "🌺🌺🌺🌺🌺", "nama": "Lima"},
	{"angka": 6,  "arab": "٦", "emoji": "🐝🐝🐝🐝🐝🐝", "nama": "Enam"},
	{"angka": 7,  "arab": "٧", "emoji": "🌈", "nama": "Tujuh"},
	{"angka": 8,  "arab": "٨", "emoji": "🎵🎵🎵🎵🎵🎵🎵🎵", "nama": "Delapan"},
	{"angka": 9,  "arab": "٩", "emoji": "🌟🌟🌟🌟🌟🌟🌟🌟🌟", "nama": "Sembilan"},
	{"angka": 10, "arab": "١٠","emoji": "🎉", "nama": "Sepuluh"},
]

const WARNA_KARTU : Array[Color] = [
	Color(0.92,0.25,0.25,1), Color(0.92,0.55,0.15,1),
	Color(0.88,0.82,0.10,1), Color(0.22,0.80,0.35,1),
	Color(0.12,0.75,0.75,1), Color(0.18,0.50,0.92,1),
	Color(0.50,0.22,0.88,1), Color(0.88,0.22,0.60,1),
	Color(0.22,0.75,0.50,1), Color(0.92,0.50,0.15,1),
]

# ── State ─────────────────────────────────────────────────────
var _mode            : String = "menu"  # "menu" | "warna" | "angka"
var _idx_warna       : int    = 0
var _benar_warna     : int    = 0
var _selesai_warna   : bool   = false
var _angka_klik      : Array  = []
var _selesai_angka   : bool   = false

# ── Node refs ─────────────────────────────────────────────────
@onready var _btn_back       : Button        = $UI/TopBar/BtnBack
@onready var _lbl_progress   : Label         = $UI/TopBar/LblProgress

# Panel Menu
@onready var _panel_menu     : Panel         = $UI/PanelMenu
@onready var _btn_warna      : Button        = $UI/PanelMenu/VBox/BtnWarna
@onready var _btn_angka      : Button        = $UI/PanelMenu/VBox/BtnAngka

# Panel Warna
@onready var _panel_warna    : Panel         = $UI/PanelWarna
@onready var _lbl_soal_w     : Label         = $UI/PanelWarna/LblSoal
@onready var _lbl_nama_w     : Label         = $UI/PanelWarna/LblNamaWarna
@onready var _lbl_feedback_w : Label         = $UI/PanelWarna/LblFeedback
@onready var _pilihan_w      : HBoxContainer = $UI/PanelWarna/PilihanBox

# Panel Angka
@onready var _panel_angka    : Panel         = $UI/PanelAngka
@onready var _grid_angka     : GridContainer = $UI/PanelAngka/GridAngka
@onready var _lbl_info_a     : Label         = $UI/PanelAngka/InfoPanel/LblInfo

# Panel Selesai
@onready var _panel_selesai  : Panel         = $UI/PanelSelesai
@onready var _lbl_selesai    : Label         = $UI/PanelSelesai/VBox/LblSelesai
@onready var _lbl_bintang    : Label         = $UI/PanelSelesai/VBox/LblBintang
@onready var _btn_menu_lagi  : Button        = $UI/PanelSelesai/VBox/BtnMenuLagi
@onready var _btn_keluar     : Button        = $UI/PanelSelesai/VBox/BtnKeluar


func _ready() -> void:
	_panel_menu.visible    = true
	_panel_warna.visible   = false
	_panel_angka.visible   = false
	_panel_selesai.visible = false
	_lbl_progress.text     = "🧩 Taman Logika"
	_btn_back.pressed.connect(_on_back)
	_btn_warna.pressed.connect(_start_warna)
	_btn_angka.pressed.connect(_start_angka)
	_btn_menu_lagi.pressed.connect(_kembali_menu)
	_btn_keluar.pressed.connect(_on_back)


# ── MENU ─────────────────────────────────────────────────────
func _kembali_menu() -> void:
	_panel_menu.visible    = true
	_panel_warna.visible   = false
	_panel_angka.visible   = false
	_panel_selesai.visible = false
	_lbl_progress.text     = "🧩 Taman Logika"


# ── MODUL WARNA ──────────────────────────────────────────────
func _start_warna() -> void:
	_idx_warna     = 0
	_benar_warna   = 0
	_selesai_warna = false
	_panel_menu.visible  = false
	_panel_warna.visible = true
	_tampil_soal_warna()


func _tampil_soal_warna() -> void:
	if _idx_warna >= SOAL_WARNA.size():
		_selesai("warna")
		return
	var soal : Dictionary = SOAL_WARNA[_idx_warna]
	_lbl_soal_w.text = "Pilih warna:"
	_lbl_nama_w.text = soal["nama"]
	_lbl_nama_w.add_theme_color_override("font_color", soal["warna"])
	_lbl_progress.text = "Warna " + str(_idx_warna + 1) + " / " + str(SOAL_WARNA.size())
	_lbl_feedback_w.visible = false
	for c in _pilihan_w.get_children():
		c.queue_free()
	var pilihan : Array[Dictionary] = []
	pilihan.append({"warna": soal["warna"], "benar": true})
	for w : Color in soal["salah"]:
		pilihan.append({"warna": w, "benar": false})
	pilihan.shuffle()
	for item : Dictionary in pilihan:
		var btn      : Button       = Button.new()
		var w        : Color        = item["warna"]
		var is_benar : bool         = item["benar"]
		var sb       : StyleBoxFlat = StyleBoxFlat.new()
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
		btn.pressed.connect(func(): _on_pilih_warna(is_benar))
		_pilihan_w.add_child(btn)


func _on_pilih_warna(is_benar: bool) -> void:
	if _selesai_warna:
		return
	_lbl_feedback_w.visible = true
	if is_benar:
		_benar_warna += 1
		_lbl_feedback_w.text = "✅  Betul! Hebat Maryam!"
		_lbl_feedback_w.add_theme_color_override("font_color", Color(0.20,0.90,0.40,1))
	else:
		_lbl_feedback_w.text = "❌  Coba lagi ya!"
		_lbl_feedback_w.add_theme_color_override("font_color", Color(0.95,0.35,0.35,1))
	await get_tree().create_timer(0.8).timeout
	_idx_warna += 1
	_tampil_soal_warna()


# ── MODUL ANGKA ──────────────────────────────────────────────
func _start_angka() -> void:
	_angka_klik   = []
	_selesai_angka = false
	_panel_menu.visible  = false
	_panel_angka.visible = true
	_lbl_info_a.text     = "Sentuh angka untuk belajar!"
	_lbl_progress.text   = "0 / 10 angka"
	_build_kartu_angka()


func _build_kartu_angka() -> void:
	for c in _grid_angka.get_children():
		c.queue_free()
	for i in ANGKA.size():
		var data  : Dictionary = ANGKA[i]
		var warna : Color      = WARNA_KARTU[i]
		var btn   : Button     = Button.new()
		var idx   : int        = i
		btn.custom_minimum_size = Vector2(108, 108)

		var lbl_angka : Label = Label.new()
		lbl_angka.text = str(data["angka"])
		lbl_angka.add_theme_font_size_override("font_size", 42)
		lbl_angka.add_theme_color_override("font_color", Color(1,1,1,1))
		lbl_angka.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl_angka.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		lbl_angka.offset_bottom = -28.0

		var lbl_nama : Label = Label.new()
		lbl_nama.text = data["nama"]
		lbl_nama.add_theme_font_size_override("font_size", 11)
		lbl_nama.add_theme_color_override("font_color", Color(1,1,1,0.90))
		lbl_nama.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl_nama.vertical_alignment   = VERTICAL_ALIGNMENT_BOTTOM
		lbl_nama.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		lbl_nama.offset_bottom = -4.0

		var sb : StyleBoxFlat = StyleBoxFlat.new()
		sb.bg_color                   = warna
		sb.corner_radius_top_left     = 16
		sb.corner_radius_top_right    = 16
		sb.corner_radius_bottom_left  = 16
		sb.corner_radius_bottom_right = 16
		sb.border_width_left          = 3
		sb.border_width_top           = 3
		sb.border_width_right         = 3
		sb.border_width_bottom        = 3
		sb.border_color               = Color(1,1,1,0.35)
		sb.shadow_color               = Color(0,0,0,0.25)
		sb.shadow_size                = 4

		var sb_done : StyleBoxFlat = StyleBoxFlat.new()
		sb_done.bg_color                   = Color(warna.r*0.50,warna.g*0.50,warna.b*0.50,1)
		sb_done.corner_radius_top_left     = 16
		sb_done.corner_radius_top_right    = 16
		sb_done.corner_radius_bottom_left  = 16
		sb_done.corner_radius_bottom_right = 16
		sb_done.border_width_left          = 3
		sb_done.border_width_top           = 3
		sb_done.border_width_right         = 3
		sb_done.border_width_bottom        = 3
		sb_done.border_color               = Color(1,1,1,0.85)

		btn.add_theme_stylebox_override("normal",  sb)
		btn.add_theme_stylebox_override("hover",   sb_done)
		btn.add_theme_stylebox_override("pressed", sb_done)
		btn.add_child(lbl_angka)
		btn.add_child(lbl_nama)
		btn.pressed.connect(func(): _on_kartu_angka(idx, btn, sb_done, data))
		_grid_angka.add_child(btn)


func _on_kartu_angka(idx: int, btn: Button, sb_done: StyleBoxFlat, data: Dictionary) -> void:
	if _selesai_angka:
		return
	_lbl_info_a.text = str(data["angka"]) + "  —  " + data["nama"] + "  " + data["emoji"]
	if idx not in _angka_klik:
		_angka_klik.append(idx)
		btn.add_theme_stylebox_override("normal", sb_done)
		var chk : Label = Label.new()
		chk.text = "✓"
		chk.add_theme_font_size_override("font_size", 14)
		chk.add_theme_color_override("font_color", Color(1,1,1,0.95))
		chk.position = Vector2(84, 4)
		btn.add_child(chk)
		_lbl_progress.text = str(_angka_klik.size()) + " / 10 angka"
	if _angka_klik.size() >= 10 and not _selesai_angka:
		_selesai_angka = true
		await get_tree().create_timer(0.5).timeout
		_selesai("angka")


# ── SELESAI ──────────────────────────────────────────────────
func _selesai(mode: String) -> void:
	GameManager.add_star(3)
	_panel_warna.visible   = false
	_panel_angka.visible   = false
	_panel_selesai.visible = true
	if mode == "warna":
		_lbl_selesai.text  = "🌈 Maryam Kenal Semua Warna!"
		_lbl_bintang.text  = "Benar: " + str(_benar_warna) + " / " + str(SOAL_WARNA.size()) + "\n⭐ ⭐ ⭐  +3 Bintang!"
	else:
		_lbl_selesai.text  = "🔢 Maryam Bisa Berhitung!"
		_lbl_bintang.text  = "Angka 1 sampai 10 sudah dikuasai!\n⭐ ⭐ ⭐  +3 Bintang!"


func _on_back() -> void:
	TransitionManager.go_to(WORLD_SCENE)
