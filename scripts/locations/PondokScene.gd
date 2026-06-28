# =============================================================
#  scripts/locations/PondokScene.gd
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

const HURUF : Array[Dictionary] = [
	{"huruf": "A", "kata": "Apel",    "emoji": "🍎"},
	{"huruf": "B", "kata": "Buku",    "emoji": "📚"},
	{"huruf": "C", "kata": "Cincin",  "emoji": "💍"},
	{"huruf": "D", "kata": "Domba",   "emoji": "🐑"},
	{"huruf": "E", "kata": "Elang",   "emoji": "🦅"},
	{"huruf": "F", "kata": "Foto",    "emoji": "📷"},
	{"huruf": "G", "kata": "Gajah",   "emoji": "🐘"},
	{"huruf": "H", "kata": "Harimau", "emoji": "🐯"},
	{"huruf": "I", "kata": "Ikan",    "emoji": "🐟"},
	{"huruf": "J", "kata": "Jeruk",   "emoji": "🍊"},
	{"huruf": "K", "kata": "Kucing",  "emoji": "🐱"},
	{"huruf": "L", "kata": "Lampu",   "emoji": "💡"},
	{"huruf": "M", "kata": "Mangga",  "emoji": "🥭"},
	{"huruf": "N", "kata": "Nanas",   "emoji": "🍍"},
	{"huruf": "O", "kata": "Onta",    "emoji": "🐪"},
	{"huruf": "P", "kata": "Pisang",  "emoji": "🍌"},
	{"huruf": "Q", "kata": "Quran",   "emoji": "📖"},
	{"huruf": "R", "kata": "Roti",    "emoji": "🍞"},
	{"huruf": "S", "kata": "Singa",   "emoji": "🦁"},
	{"huruf": "T", "kata": "Topi",    "emoji": "🎩"},
	{"huruf": "U", "kata": "Ulat",    "emoji": "🐛"},
	{"huruf": "V", "kata": "Vas",     "emoji": "🏺"},
	{"huruf": "W", "kata": "Wortel",  "emoji": "🥕"},
	{"huruf": "X", "kata": "Xilofon", "emoji": "🎵"},
	{"huruf": "Y", "kata": "Yogurt",  "emoji": "🥛"},
	{"huruf": "Z", "kata": "Zebra",   "emoji": "🦓"},
]

const WARNA : Array[Color] = [
	Color(0.95,0.35,0.35,1), Color(0.95,0.55,0.20,1),
	Color(0.92,0.80,0.12,1), Color(0.55,0.88,0.22,1),
	Color(0.18,0.80,0.50,1), Color(0.12,0.78,0.80,1),
	Color(0.18,0.55,0.95,1), Color(0.42,0.28,0.92,1),
	Color(0.65,0.22,0.92,1), Color(0.92,0.22,0.65,1),
	Color(0.95,0.35,0.35,1), Color(0.95,0.55,0.20,1),
	Color(0.92,0.80,0.12,1), Color(0.55,0.88,0.22,1),
	Color(0.18,0.80,0.50,1), Color(0.12,0.78,0.80,1),
	Color(0.18,0.55,0.95,1), Color(0.42,0.28,0.92,1),
	Color(0.65,0.22,0.92,1), Color(0.92,0.22,0.65,1),
	Color(0.95,0.35,0.35,1), Color(0.95,0.55,0.20,1),
	Color(0.92,0.80,0.12,1), Color(0.55,0.88,0.22,1),
	Color(0.18,0.80,0.50,1), Color(0.12,0.78,0.80,1),
]

var _sudah_klik : int   = 0
var _klik_list  : Array = []
var _selesai    : bool  = false

@onready var _grid          : GridContainer = $UI/Scroll/Grid
@onready var _lbl_progress  : Label         = $UI/TopBar/LblProgress
@onready var _lbl_info      : Label         = $UI/InfoPanel/LblInfo
@onready var _btn_back      : Button        = $UI/TopBar/BtnBack
@onready var _panel_selesai : Panel         = $UI/PanelSelesai
@onready var _btn_keluar    : Button        = $UI/PanelSelesai/VBox/BtnKeluar


func _ready() -> void:
	_lbl_progress.text     = "0 / 26 huruf"
	_lbl_info.text         = "Sentuh huruf untuk belajar!"
	_panel_selesai.visible = false
	_btn_back.pressed.connect(_on_back)
	_btn_keluar.pressed.connect(_on_back)
	_build_kartu()


func _build_kartu() -> void:
	for i in HURUF.size():
		var data  : Dictionary = HURUF[i]
		var warna : Color      = WARNA[i]
		var btn   : Button     = Button.new()
		var idx   : int        = i

		btn.custom_minimum_size = Vector2(100, 100)

		var lbl_huruf : Label = Label.new()
		lbl_huruf.text = data["huruf"]
		lbl_huruf.add_theme_font_size_override("font_size", 38)
		lbl_huruf.add_theme_color_override("font_color", Color(1,1,1,1))
		lbl_huruf.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl_huruf.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

		var lbl_kata : Label = Label.new()
		lbl_kata.text = data["emoji"] + " " + data["kata"]
		lbl_kata.add_theme_font_size_override("font_size", 10)
		lbl_kata.add_theme_color_override("font_color", Color(1,1,1,0.90))
		lbl_kata.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl_kata.vertical_alignment   = VERTICAL_ALIGNMENT_BOTTOM
		lbl_kata.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		lbl_kata.offset_bottom = -6.0

		var sb : StyleBoxFlat = StyleBoxFlat.new()
		sb.bg_color                       = warna
		sb.corner_radius_top_left         = 16
		sb.corner_radius_top_right        = 16
		sb.corner_radius_bottom_left      = 16
		sb.corner_radius_bottom_right     = 16
		sb.border_width_left              = 3
		sb.border_width_top               = 3
		sb.border_width_right             = 3
		sb.border_width_bottom            = 3
		sb.border_color                   = Color(1,1,1,0.35)
		sb.shadow_color                   = Color(0,0,0,0.25)
		sb.shadow_size                    = 4

		var sb_done : StyleBoxFlat = StyleBoxFlat.new()
		sb_done.bg_color                   = Color(warna.r*0.50, warna.g*0.50, warna.b*0.50, 1)
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
		btn.add_child(lbl_huruf)
		btn.add_child(lbl_kata)
		btn.pressed.connect(func(): _on_kartu(idx, btn, sb_done))
		_grid.add_child(btn)


func _on_kartu(idx: int, btn: Button, sb_done: StyleBoxFlat) -> void:
	if _selesai:
		return
	var data : Dictionary = HURUF[idx]
	_lbl_info.text = data["huruf"] + "  —  " + data["emoji"] + "  " + data["kata"]

	if idx not in _klik_list:
		_klik_list.append(idx)
		_sudah_klik += 1
		btn.add_theme_stylebox_override("normal", sb_done)
		var chk : Label = Label.new()
		chk.text = "✓"
		chk.add_theme_font_size_override("font_size", 14)
		chk.add_theme_color_override("font_color", Color(1,1,1,0.95))
		chk.position = Vector2(76, 4)
		btn.add_child(chk)
		_lbl_progress.text = str(_sudah_klik) + " / 26 huruf"

	if _sudah_klik >= 26 and not _selesai:
		_selesai = true
		await get_tree().create_timer(0.5).timeout
		_show_selesai()


func _show_selesai() -> void:
	GameManager.add_star(3)
	_panel_selesai.visible = true


func _on_back() -> void:
	TransitionManager.go_to(WORLD_SCENE)
