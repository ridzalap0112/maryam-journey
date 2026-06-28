"""
Maryam Journey - Fix PondokScene.gd
python fix_pondok.py
"""
import os, subprocess, sys

BASE = os.getcwd()
SCRIPT_PATH = os.path.abspath(__file__)

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n📚 Fix PondokScene.gd")
print("=" * 48)

write(os.path.join(BASE, "scripts", "locations", "PondokScene.gd"), """\
# =============================================================
#  scripts/locations/PondokScene.gd
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

const HURUF : Array[Dictionary] = [
\t{"huruf": "A", "kata": "Apel",    "emoji": "🍎"},
\t{"huruf": "B", "kata": "Buku",    "emoji": "📚"},
\t{"huruf": "C", "kata": "Cincin",  "emoji": "💍"},
\t{"huruf": "D", "kata": "Domba",   "emoji": "🐑"},
\t{"huruf": "E", "kata": "Elang",   "emoji": "🦅"},
\t{"huruf": "F", "kata": "Foto",    "emoji": "📷"},
\t{"huruf": "G", "kata": "Gajah",   "emoji": "🐘"},
\t{"huruf": "H", "kata": "Harimau", "emoji": "🐯"},
\t{"huruf": "I", "kata": "Ikan",    "emoji": "🐟"},
\t{"huruf": "J", "kata": "Jeruk",   "emoji": "🍊"},
\t{"huruf": "K", "kata": "Kucing",  "emoji": "🐱"},
\t{"huruf": "L", "kata": "Lampu",   "emoji": "💡"},
\t{"huruf": "M", "kata": "Mangga",  "emoji": "🥭"},
\t{"huruf": "N", "kata": "Nanas",   "emoji": "🍍"},
\t{"huruf": "O", "kata": "Onta",    "emoji": "🐪"},
\t{"huruf": "P", "kata": "Pisang",  "emoji": "🍌"},
\t{"huruf": "Q", "kata": "Quran",   "emoji": "📖"},
\t{"huruf": "R", "kata": "Roti",    "emoji": "🍞"},
\t{"huruf": "S", "kata": "Singa",   "emoji": "🦁"},
\t{"huruf": "T", "kata": "Topi",    "emoji": "🎩"},
\t{"huruf": "U", "kata": "Ulat",    "emoji": "🐛"},
\t{"huruf": "V", "kata": "Vas",     "emoji": "🏺"},
\t{"huruf": "W", "kata": "Wortel",  "emoji": "🥕"},
\t{"huruf": "X", "kata": "Xilofon", "emoji": "🎵"},
\t{"huruf": "Y", "kata": "Yogurt",  "emoji": "🥛"},
\t{"huruf": "Z", "kata": "Zebra",   "emoji": "🦓"},
]

const WARNA : Array[Color] = [
\tColor(0.95,0.35,0.35,1), Color(0.95,0.55,0.20,1),
\tColor(0.92,0.80,0.12,1), Color(0.55,0.88,0.22,1),
\tColor(0.18,0.80,0.50,1), Color(0.12,0.78,0.80,1),
\tColor(0.18,0.55,0.95,1), Color(0.42,0.28,0.92,1),
\tColor(0.65,0.22,0.92,1), Color(0.92,0.22,0.65,1),
\tColor(0.95,0.35,0.35,1), Color(0.95,0.55,0.20,1),
\tColor(0.92,0.80,0.12,1), Color(0.55,0.88,0.22,1),
\tColor(0.18,0.80,0.50,1), Color(0.12,0.78,0.80,1),
\tColor(0.18,0.55,0.95,1), Color(0.42,0.28,0.92,1),
\tColor(0.65,0.22,0.92,1), Color(0.92,0.22,0.65,1),
\tColor(0.95,0.35,0.35,1), Color(0.95,0.55,0.20,1),
\tColor(0.92,0.80,0.12,1), Color(0.55,0.88,0.22,1),
\tColor(0.18,0.80,0.50,1), Color(0.12,0.78,0.80,1),
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
\t_lbl_progress.text     = "0 / 26 huruf"
\t_lbl_info.text         = "Sentuh huruf untuk belajar!"
\t_panel_selesai.visible = false
\t_btn_back.pressed.connect(_on_back)
\t_btn_keluar.pressed.connect(_on_back)
\t_build_kartu()


func _build_kartu() -> void:
\tfor i in HURUF.size():
\t\tvar data  : Dictionary = HURUF[i]
\t\tvar warna : Color      = WARNA[i]
\t\tvar btn   : Button     = Button.new()
\t\tvar idx   : int        = i

\t\tbtn.custom_minimum_size = Vector2(100, 100)

\t\tvar lbl_huruf : Label = Label.new()
\t\tlbl_huruf.text = data["huruf"]
\t\tlbl_huruf.add_theme_font_size_override("font_size", 38)
\t\tlbl_huruf.add_theme_color_override("font_color", Color(1,1,1,1))
\t\tlbl_huruf.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\t\tlbl_huruf.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

\t\tvar lbl_kata : Label = Label.new()
\t\tlbl_kata.text = data["emoji"] + " " + data["kata"]
\t\tlbl_kata.add_theme_font_size_override("font_size", 10)
\t\tlbl_kata.add_theme_color_override("font_color", Color(1,1,1,0.90))
\t\tlbl_kata.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\t\tlbl_kata.vertical_alignment   = VERTICAL_ALIGNMENT_BOTTOM
\t\tlbl_kata.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
\t\tlbl_kata.offset_bottom = -6.0

\t\tvar sb : StyleBoxFlat = StyleBoxFlat.new()
\t\tsb.bg_color                       = warna
\t\tsb.corner_radius_top_left         = 16
\t\tsb.corner_radius_top_right        = 16
\t\tsb.corner_radius_bottom_left      = 16
\t\tsb.corner_radius_bottom_right     = 16
\t\tsb.border_width_left              = 3
\t\tsb.border_width_top               = 3
\t\tsb.border_width_right             = 3
\t\tsb.border_width_bottom            = 3
\t\tsb.border_color                   = Color(1,1,1,0.35)
\t\tsb.shadow_color                   = Color(0,0,0,0.25)
\t\tsb.shadow_size                    = 4

\t\tvar sb_done : StyleBoxFlat = StyleBoxFlat.new()
\t\tsb_done.bg_color                   = Color(warna.r*0.50, warna.g*0.50, warna.b*0.50, 1)
\t\tsb_done.corner_radius_top_left     = 16
\t\tsb_done.corner_radius_top_right    = 16
\t\tsb_done.corner_radius_bottom_left  = 16
\t\tsb_done.corner_radius_bottom_right = 16
\t\tsb_done.border_width_left          = 3
\t\tsb_done.border_width_top           = 3
\t\tsb_done.border_width_right         = 3
\t\tsb_done.border_width_bottom        = 3
\t\tsb_done.border_color               = Color(1,1,1,0.85)

\t\tbtn.add_theme_stylebox_override("normal",  sb)
\t\tbtn.add_theme_stylebox_override("hover",   sb_done)
\t\tbtn.add_theme_stylebox_override("pressed", sb_done)
\t\tbtn.add_child(lbl_huruf)
\t\tbtn.add_child(lbl_kata)
\t\tbtn.pressed.connect(func(): _on_kartu(idx, btn, sb_done))
\t\t_grid.add_child(btn)


func _on_kartu(idx: int, btn: Button, sb_done: StyleBoxFlat) -> void:
\tif _selesai:
\t\treturn
\tvar data : Dictionary = HURUF[idx]
\t_lbl_info.text = data["huruf"] + "  —  " + data["emoji"] + "  " + data["kata"]

\tif idx not in _klik_list:
\t\t_klik_list.append(idx)
\t\t_sudah_klik += 1
\t\tbtn.add_theme_stylebox_override("normal", sb_done)
\t\tvar chk : Label = Label.new()
\t\tchk.text = "✓"
\t\tchk.add_theme_font_size_override("font_size", 14)
\t\tchk.add_theme_color_override("font_color", Color(1,1,1,0.95))
\t\tchk.position = Vector2(76, 4)
\t\tbtn.add_child(chk)
\t\t_lbl_progress.text = str(_sudah_klik) + " / 26 huruf"

\tif _sudah_klik >= 26 and not _selesai:
\t\t_selesai = true
\t\tawait get_tree().create_timer(0.5).timeout
\t\t_show_selesai()


func _show_selesai() -> void:
\tGameManager.add_star(3)
\t_panel_selesai.visible = true


func _on_back() -> void:
\tTransitionManager.go_to(WORLD_SCENE)
""")

try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m", "fix: PondokScene typed Array[Dictionary] and Array[Color]"], cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️  Git: {e}")

try:
    os.remove(SCRIPT_PATH)
    print("  ✅  Script dihapus otomatis")
except:
    pass

print("\n  Godot → Reload → F5 → Pondok Baca berjalan! 🌙\n")
