"""
Maryam Journey - Build V4 Complete
Jalankan: python build_v4_complete.py
"""
import os, subprocess

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Build V4 Complete")
print("=" * 52)

# ═══════════════════════════════════════════════════
# 1. SaveManager.gd (Autoload)
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "managers", "SaveManager.gd"), """\
# =============================================================
#  scripts/managers/SaveManager.gd
#  Autoload — simpan & load progress ke file JSON
#  Daftarkan di: Project > Autoload > SaveManager
# =============================================================
extends Node

const SAVE_PATH : String = "user://maryam_save.json"


func save() -> void:
\tvar data : Dictionary = {
\t\t"player_name"        : GameManager.player_name,
\t\t"total_stars"        : GameManager.total_stars,
\t\t"unlocked_locations" : GameManager.unlocked_locations,
\t}
\tvar file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
\tif file:
\t\tfile.store_string(JSON.stringify(data, "\t"))
\t\tfile.close()
\t\tprint("[Save] Progress tersimpan.")
\telse:
\t\tpush_error("[Save] Gagal menyimpan: " + SAVE_PATH)


func load_save() -> bool:
\tif not FileAccess.file_exists(SAVE_PATH):
\t\tprint("[Save] Belum ada save file.")
\t\treturn false
\tvar file := FileAccess.open(SAVE_PATH, FileAccess.READ)
\tif not file:
\t\tpush_error("[Save] Gagal membuka save file.")
\t\treturn false
\tvar raw  : String     = file.get_as_text()
\tfile.close()
\tvar json := JSON.new()
\tif json.parse(raw) != OK:
\t\tpush_error("[Save] JSON rusak, save dihapus.")
\t\tdelete_save()
\t\treturn false
\tvar data : Dictionary = json.get_data()
\tGameManager.player_name        = data.get("player_name", "Maryam")
\tGameManager.total_stars        = data.get("total_stars", 0)
\tGameManager.unlocked_locations = data.get("unlocked_locations",
\t\t["masjid", "pondok", "taman", "kebun", "rumah"])
\tprint("[Save] Progress dimuat. Bintang: ", GameManager.total_stars)
\treturn true


func delete_save() -> void:
\tif FileAccess.file_exists(SAVE_PATH):
\t\tDirAccess.remove_absolute(SAVE_PATH)
\t\tprint("[Save] Save file dihapus.")


func has_save() -> bool:
\treturn FileAccess.file_exists(SAVE_PATH)
""")

# ═══════════════════════════════════════════════════
# 2. AudioManager.gd (Autoload)
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "managers", "AudioManager.gd"), """\
# =============================================================
#  scripts/managers/AudioManager.gd
#  Autoload — kelola musik & SFX
#  Daftarkan di: Project > Autoload > AudioManager
#  Nanti tinggal isi file audio di assets/audio/
# =============================================================
extends Node

# Path audio (isi saat sudah ada file)
const BGM_WORLD  : String = "res://assets/audio/music/bgm_world.ogg"
const SFX_JUMP   : String = "res://assets/audio/sfx/jump.wav"
const SFX_STAR   : String = "res://assets/audio/sfx/star.wav"
const SFX_ENTER  : String = "res://assets/audio/sfx/enter_location.wav"

var _bgm  : AudioStreamPlayer
var _sfx  : AudioStreamPlayer


func _ready() -> void:
\t_bgm = AudioStreamPlayer.new()
\t_bgm.bus = "Music"
\t_bgm.volume_db = -8.0
\tadd_child(_bgm)

\t_sfx = AudioStreamPlayer.new()
\t_sfx.bus = "SFX"
\tadd_child(_sfx)


func play_bgm(path: String) -> void:
\tif not ResourceLoader.exists(path):
\t\treturn
\tif _bgm.playing and _bgm.stream and _bgm.stream.resource_path == path:
\t\treturn
\t_bgm.stream = load(path)
\t_bgm.play()


func stop_bgm() -> void:
\t_bgm.stop()


func play_sfx(path: String) -> void:
\tif not ResourceLoader.exists(path):
\t\treturn
\t_sfx.stream = load(path)
\t_sfx.play()


func set_bgm_volume(db: float) -> void:
\t_bgm.volume_db = db


func set_sfx_volume(db: float) -> void:
\t_sfx.volume_db = db
""")

# ═══════════════════════════════════════════════════
# 3. TransitionManager.gd (Autoload)
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "managers", "TransitionManager.gd"), """\
# =============================================================
#  scripts/managers/TransitionManager.gd
#  Autoload — fade in/out saat pindah scene
#  Daftarkan di: Project > Autoload > TransitionManager
# =============================================================
extends CanvasLayer

var _overlay  : ColorRect
var _tween    : Tween
var _is_busy  : bool = false

signal transition_done


func _ready() -> void:
\t_overlay = ColorRect.new()
\t_overlay.color = Color(0, 0, 0, 0)
\t_overlay.anchors_preset = Control.PRESET_FULL_RECT
\t_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
\tadd_child(_overlay)


func go_to(scene_path: String) -> void:
\tif _is_busy:
\t\treturn
\t_is_busy = true
\tawait _fade(1.0)
\tSaveManager.save()
\tget_tree().change_scene_to_file(scene_path)
\tawait get_tree().process_frame
\tawait _fade(0.0)
\t_is_busy = false
\ttransition_done.emit()


func _fade(target_alpha: float) -> void:
\tif _tween and _tween.is_valid():
\t\t_tween.kill()
\t_tween = create_tween()
\t_tween.tween_property(_overlay, "color:a", target_alpha, 0.45)\
\t\t.set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
\tawait _tween.finished
""")

# ═══════════════════════════════════════════════════
# 4. GameManager.gd (update — tambah reference ke save)
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "managers", "GameManager.gd"), """\
# =============================================================
#  scripts/managers/GameManager.gd
#  Autoload global
# =============================================================
extends Node

var player_name        : String = "Maryam"
var total_stars        : int    = 0
var unlocked_locations : Array  = ["masjid", "pondok", "taman", "kebun", "rumah"]

signal star_collected(total: int)
signal location_unlocked(location_name: String)


func _ready() -> void:
\tprint("[MaryamJourney] Assalamu'alaikum!")


func add_star(amount: int = 1) -> void:
\ttotal_stars += amount
\tstar_collected.emit(total_stars)
\tSaveManager.save()


func unlock_location(location_name: String) -> void:
\tif location_name not in unlocked_locations:
\t\tunlocked_locations.append(location_name)
\t\tlocation_unlocked.emit(location_name)
\t\tSaveManager.save()


func is_location_unlocked(location_name: String) -> bool:
\treturn location_name in unlocked_locations
""")

# ═══════════════════════════════════════════════════
# 5. Player.gd (tambah boundary)
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "player", "Player.gd"), """\
# =============================================================
#  scripts/player/Player.gd  —  Godot 4.7
# =============================================================
extends CharacterBody2D

const SPEED       : float = 200.0
const GRAVITY     : float = 800.0
const JUMP_FORCE  : float = -420.0

# Boundary dunia (sesuai WorldMap 4800px, ground Y=580)
const WORLD_LEFT  : float = 40.0
const WORLD_RIGHT : float = 4760.0
const WORLD_TOP   : float = 60.0
const FLOOR_Y     : float = 548.0

@onready var _sprite : AnimatedSprite2D = $AnimatedSprite2D

var _anim_current : String = ""


func _ready() -> void:
\tassert(_sprite != null, "AnimatedSprite2D tidak ditemukan!")
\tadd_to_group("player")
\t_play_anim("idle")


func _physics_process(delta: float) -> void:
\t_apply_gravity(delta)
\t_handle_movement()
\t_handle_jump()
\tmove_and_slide()
\t_enforce_boundary()
\t_update_animation()


func _apply_gravity(delta: float) -> void:
\tif not is_on_floor():
\t\tvelocity.y += GRAVITY * delta
\t\tvelocity.y = min(velocity.y, 1400.0)


func _handle_movement() -> void:
\tvar dir := Input.get_axis("move_left", "move_right")
\tvelocity.x = dir * SPEED
\tif dir != 0.0:
\t\t_sprite.flip_h = dir < 0.0


func _handle_jump() -> void:
\tif is_on_floor() and Input.is_action_just_pressed("jump"):
\t\tvelocity.y = JUMP_FORCE


func _enforce_boundary() -> void:
\tvar pos := global_position
\t# Kiri
\tif pos.x < WORLD_LEFT:
\t\tpos.x = WORLD_LEFT
\t\tvelocity.x = 0.0
\t# Kanan
\tif pos.x > WORLD_RIGHT:
\t\tpos.x = WORLD_RIGHT
\t\tvelocity.x = 0.0
\t# Atas
\tif pos.y < WORLD_TOP:
\t\tpos.y = WORLD_TOP
\t\tvelocity.y = 0.0
\t# Jatuh darurat (tembus lantai)
\tif pos.y > FLOOR_Y + 40.0:
\t\tpos.y = FLOOR_Y
\t\tvelocity.y = 0.0
\tglobal_position = pos


func _update_animation() -> void:
\tvar next : String
\tif not is_on_floor():
\t\tnext = "jump"
\telif abs(velocity.x) > 10.0:
\t\tnext = "walk"
\telse:
\t\tnext = "idle"
\t_play_anim(next)


func _play_anim(anim_name: String) -> void:
\tif _anim_current == anim_name:
\t\treturn
\tif _sprite.sprite_frames and _sprite.sprite_frames.has_animation(anim_name):
\t\t_anim_current = anim_name
\t\t_sprite.play(anim_name)
""")

# ═══════════════════════════════════════════════════
# 6. LocationZone.gd (tambah transisi scene)
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "locations", "LocationZone.gd"), """\
# =============================================================
#  scripts/locations/LocationZone.gd
# =============================================================
extends Area2D

@export var location_name : String = "Lokasi"
@export var location_key  : String = "masjid"
@export var scene_path    : String = ""

@onready var _panel : Panel = $LabelPanel
@onready var _label : Label = $LabelPanel/Label
@onready var _hint  : Label = $LabelPanel/Hint

var _inside   : bool  = false
var _bob_time : float = 0.0


func _ready() -> void:
\t_label.text = location_name
\t_hint.text  = "▼ Tekan Enter"
\t_panel.visible = false
\tbody_entered.connect(_on_entered)
\tbody_exited.connect(_on_exited)


func _process(delta: float) -> void:
\tif not _inside:
\t\treturn
\t_bob_time += delta
\t_panel.position.y = -140.0 + sin(_bob_time * 2.8) * 6.0
\tif Input.is_action_just_pressed("interact"):
\t\t_enter()


func _on_entered(body: Node2D) -> void:
\tif body.is_in_group("player"):
\t\t_inside   = true
\t\t_bob_time = 0.0
\t\t_panel.position.y = -140.0
\t\t_panel.visible = true
\t\tif not GameManager.is_location_unlocked(location_key):
\t\t\t_hint.text = "🔒 Terkunci"
\t\telse:
\t\t\t_hint.text = "▼ Tekan Enter"


func _on_exited(body: Node2D) -> void:
\tif body.is_in_group("player"):
\t\t_inside = false
\t\t_panel.visible = false


func _enter() -> void:
\tif not GameManager.is_location_unlocked(location_key):
\t\treturn
\tif scene_path == "" or not ResourceLoader.exists(scene_path):
\t\tprint("[Zone] Scene belum ada: ", scene_path)
\t\treturn
\tTransitionManager.go_to(scene_path)
""")

# ═══════════════════════════════════════════════════
# 7. HUD.gd (update)
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "ui", "HUD.gd"), """\
# =============================================================
#  scripts/ui/HUD.gd
# =============================================================
extends CanvasLayer

@onready var _star_label : Label = $StarPanel/StarLabel
@onready var _name_label : Label = $NameLabel


func _ready() -> void:
\tGameManager.star_collected.connect(_on_star)
\t_name_label.text = "🌙 " + GameManager.player_name
\t_star_label.text = "⭐  " + str(GameManager.total_stars)


func _on_star(total: int) -> void:
\t_star_label.text = "⭐  " + str(total)
""")

# ═══════════════════════════════════════════════════
# 8. MainMenu.tscn + MainMenu.gd
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "ui", "MainMenu.gd"), """\
# =============================================================
#  scripts/ui/MainMenu.gd
# =============================================================
extends Node2D

@onready var _btn_start    : Button = $UI/CenterBox/VBox/BtnStart
@onready var _btn_continue : Button = $UI/CenterBox/VBox/BtnContinue
@onready var _btn_reset    : Button = $UI/CenterBox/VBox/BtnReset
@onready var _lbl_stars    : Label  = $UI/CenterBox/VBox/LblStars

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"


func _ready() -> void:
\tvar has_save := SaveManager.has_save()
\t_btn_continue.visible = has_save
\t_btn_reset.visible    = has_save
\tif has_save:
\t\tSaveManager.load_save()
\t\t_lbl_stars.text = "⭐ " + str(GameManager.total_stars) + " bintang tersimpan"
\telse:
\t\t_lbl_stars.text = "Petualangan baru menantimu!"

\t_btn_start.pressed.connect(_on_start)
\t_btn_continue.pressed.connect(_on_continue)
\t_btn_reset.pressed.connect(_on_reset)


func _on_start() -> void:
\tSaveManager.delete_save()
\tGameManager.total_stars        = 0
\tGameManager.unlocked_locations = ["masjid", "pondok", "taman", "kebun", "rumah"]
\tTransitionManager.go_to(WORLD_SCENE)


func _on_continue() -> void:
\tTransitionManager.go_to(WORLD_SCENE)


func _on_reset() -> void:
\tSaveManager.delete_save()
\tGameManager.total_stars        = 0
\tGameManager.unlocked_locations = ["masjid", "pondok", "taman", "kebun", "rumah"]
\t_btn_continue.visible = false
\t_btn_reset.visible    = false
\t_lbl_stars.text       = "Petualangan baru menantimu!"
""")

write(os.path.join(BASE, "scenes", "ui", "MainMenu.tscn"), """\
[gd_scene load_steps=5 format=3]

[ext_resource type="Script" path="res://scripts/ui/MainMenu.gd" id="1_menu"]

[sub_resource type="StyleBoxFlat" id="SB_btn"]
bg_color = Color(0.10, 0.08, 0.25, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.84, 0.12, 1.0)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12
content_margin_left = 24.0
content_margin_right = 24.0
content_margin_top = 10.0
content_margin_bottom = 10.0

[sub_resource type="StyleBoxFlat" id="SB_btn_hover"]
bg_color = Color(0.20, 0.16, 0.40, 0.98)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.92, 0.40, 1.0)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12
content_margin_left = 24.0
content_margin_right = 24.0
content_margin_top = 10.0
content_margin_bottom = 10.0

[sub_resource type="StyleBoxFlat" id="SB_card"]
bg_color = Color(0.05, 0.04, 0.18, 0.88)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.84, 0.12, 0.80)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20

[node name="MainMenu" type="Node2D"]
script = ExtResource("1_menu")

[node name="Sky" type="ColorRect" parent="."]
color = Color(0.16, 0.12, 0.36, 1)
size = Vector2(1280, 720)

[node name="GlowTop" type="Polygon2D" parent="."]
color = Color(0.30, 0.20, 0.60, 0.35)
polygon = PackedVector2Array(0,0, 1280,0, 1280,400, 0,400)

[node name="Star1" type="Polygon2D" parent="."]
color = Color(1,1,1,0.90)
polygon = PackedVector2Array(120,80, 122,86, 128,86, 123,90, 125,96, 120,92, 115,96, 117,90, 112,86, 118,86)

[node name="Star2" type="Polygon2D" parent="."]
color = Color(1,1,0.8,0.80)
polygon = PackedVector2Array(300,40, 301,44, 305,44, 302,47, 303,51, 300,48, 297,51, 298,47, 295,44, 299,44)

[node name="Star3" type="Polygon2D" parent="."]
color = Color(1,1,1,0.85)
polygon = PackedVector2Array(600,60, 602,66, 608,66, 603,70, 605,76, 600,72, 595,76, 597,70, 592,66, 598,66)

[node name="Star4" type="Polygon2D" parent="."]
color = Color(1,1,0.8,0.75)
polygon = PackedVector2Array(900,35, 901,39, 905,39, 902,42, 903,46, 900,43, 897,46, 898,42, 895,39, 899,39)

[node name="Star5" type="Polygon2D" parent="."]
color = Color(1,1,1,0.88)
polygon = PackedVector2Array(1100,90, 1102,96, 1108,96, 1103,100, 1105,106, 1100,102, 1095,106, 1097,100, 1092,96, 1098,96)

[node name="Star6" type="Polygon2D" parent="."]
color = Color(1,1,0.8,0.70)
polygon = PackedVector2Array(200,150, 201,153, 204,153, 202,155, 203,158, 200,156, 197,158, 198,155, 196,153, 199,153)

[node name="Star7" type="Polygon2D" parent="."]
color = Color(1,1,1,0.82)
polygon = PackedVector2Array(1050,140, 1051,143, 1054,143, 1052,145, 1053,148, 1050,146, 1047,148, 1048,145, 1046,143, 1049,143)

[node name="MoonGlow" type="Polygon2D" parent="."]
color = Color(1.0, 0.95, 0.70, 0.15)
polygon = PackedVector2Array(1050,20, 1160,20, 1200,100, 1010,100)

[node name="Moon" type="Polygon2D" parent="."]
color = Color(1.0, 0.96, 0.80, 1.0)
polygon = PackedVector2Array(1100,30, 1108,34, 1118,34, 1124,42, 1124,54, 1118,62, 1108,66, 1100,70, 1090,62, 1082,54, 1080,42, 1086,34, 1096,34)

[node name="MoonInner" type="Polygon2D" parent="."]
color = Color(0.16, 0.12, 0.36, 1)
polygon = PackedVector2Array(1110,36, 1116,40, 1120,48, 1120,56, 1116,64, 1110,70, 1106,60, 1106,46)

[node name="HillFar" type="Polygon2D" parent="."]
color = Color(0.14, 0.24, 0.18, 0.80)
polygon = PackedVector2Array(0,720, 0,560, 180,480, 400,520, 640,470, 880,510, 1100,475, 1280,500, 1280,720)

[node name="HillNear" type="Polygon2D" parent="."]
color = Color(0.12, 0.20, 0.14, 1)
polygon = PackedVector2Array(0,720, 0,610, 120,570, 300,590, 520,558, 760,585, 1000,555, 1280,575, 1280,720)

[node name="MasjidSil" type="Node2D" parent="."]
position = Vector2(80, 0)

[node name="Body" type="ColorRect" parent="MasjidSil"]
color = Color(0.10, 0.16, 0.12, 1)
position = Vector2(20, 520)
size = Vector2(100, 200)

[node name="Dome" type="Polygon2D" parent="MasjidSil"]
color = Color(0.08, 0.14, 0.10, 1)
polygon = PackedVector2Array(20,524, 36,492, 56,478, 70,474, 84,478, 104,492, 120,524)

[node name="Minaret" type="ColorRect" parent="MasjidSil"]
color = Color(0.10, 0.16, 0.12, 1)
position = Vector2(128, 500)
size = Vector2(18, 220)

[node name="MinaretTop" type="Polygon2D" parent="MasjidSil"]
color = Color(0.08, 0.14, 0.10, 1)
polygon = PackedVector2Array(128,504, 137,482, 146,504)

[node name="MasjidSil2" type="Node2D" parent="."]
position = Vector2(1060, 0)

[node name="Body" type="ColorRect" parent="MasjidSil2"]
color = Color(0.10, 0.16, 0.12, 1)
position = Vector2(20, 530)
size = Vector2(90, 190)

[node name="Dome" type="Polygon2D" parent="MasjidSil2"]
color = Color(0.08, 0.14, 0.10, 1)
polygon = PackedVector2Array(20,534, 34,504, 52,490, 65,486, 78,490, 96,504, 110,534)

[node name="Minaret" type="ColorRect" parent="MasjidSil2"]
color = Color(0.10, 0.16, 0.12, 1)
position = Vector2(4, 510)
size = Vector2(16, 210)

[node name="MinaretTop" type="Polygon2D" parent="MasjidSil2"]
color = Color(0.08, 0.14, 0.10, 1)
polygon = PackedVector2Array(4,514, 12,492, 20,514)

[node name="UI" type="CanvasLayer" parent="."]

[node name="CenterBox" type="CenterContainer" parent="UI"]
anchors_preset = 15
offset_right = 1280.0
offset_bottom = 720.0

[node name="VBox" type="VBoxContainer" parent="UI/CenterBox"]
custom_minimum_size = Vector2(420, 0)
theme_override_constants/separation = 18

[node name="Card" type="Panel" parent="UI/CenterBox/VBox"]
custom_minimum_size = Vector2(420, 280)
theme_override_styles/panel = SubResource("SB_card")

[node name="InnerVBox" type="VBoxContainer" parent="UI/CenterBox/VBox/Card"]
anchors_preset = 15
offset_left = 24.0
offset_top = 24.0
offset_right = -24.0
offset_bottom = -24.0
theme_override_constants/separation = 12

[node name="LblTitle" type="Label" parent="UI/CenterBox/VBox/Card/InnerVBox"]
text = "🌙 Maryam Journey"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 36

[node name="LblSubtitle" type="Label" parent="UI/CenterBox/VBox/Card/InnerVBox"]
text = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 18
theme_override_colors/font_color = Color(1.0, 0.90, 0.40, 1)

[node name="LblDesc" type="Label" parent="UI/CenterBox/VBox/Card/InnerVBox"]
text = "Jelajahi dunia bersama Maryam\nBelajar, bermain, dan tumbuh bersama Islam 🌟"
horizontal_alignment = 1
autowrap_mode = 3
theme_override_font_sizes/font_size = 14
theme_override_colors/font_color = Color(0.85, 0.85, 0.95, 1)

[node name="LblStars" type="Label" parent="UI/CenterBox/VBox/Card/InnerVBox"]
name = "LblStars"
text = "Petualangan baru menantimu!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 13
theme_override_colors/font_color = Color(1.0, 0.84, 0.12, 1)

[node name="BtnStart" type="Button" parent="UI/CenterBox/VBox/Card/InnerVBox"]
text = "✨  Mulai Petualangan Baru"
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_btn_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 16

[node name="BtnContinue" type="Button" parent="UI/CenterBox/VBox/Card/InnerVBox"]
text = "▶  Lanjutkan Petualangan"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_btn_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 16

[node name="BtnReset" type="Button" parent="UI/CenterBox/VBox/Card/InnerVBox"]
text = "🗑  Hapus Progress"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_btn_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 13
theme_override_colors/font_color = Color(1, 0.5, 0.5, 1)
""")

# ═══════════════════════════════════════════════════
# 9. Patch project.godot
# ═══════════════════════════════════════════════════
proj_path = os.path.join(BASE, "project.godot")
with open(proj_path, "r", encoding="utf-8") as f:
    proj = f.read()

changed = False

# Ganti main scene ke MainMenu
if 'run/main_scene="res://scenes/world/WorldMap.tscn"' in proj:
    proj = proj.replace(
        'run/main_scene="res://scenes/world/WorldMap.tscn"',
        'run/main_scene="res://scenes/ui/MainMenu.tscn"'
    )
    changed = True
    print("  ✅  Main scene → MainMenu.tscn")

# Tambah autoload baru
new_autoloads = [
    ('SaveManager',       'res://scripts/managers/SaveManager.gd'),
    ('AudioManager',      'res://scripts/managers/AudioManager.gd'),
    ('TransitionManager', 'res://scripts/managers/TransitionManager.gd'),
]
for name, path in new_autoloads:
    entry = f'{name}="*{path}"'
    if name not in proj:
        proj = proj.replace(
            '[autoload]',
            f'[autoload]\n\n{entry}'
        )
        changed = True
        print(f"  ✅  Autoload {name} ditambahkan")
    else:
        print(f"  ⏭️   Autoload {name} sudah ada")

if changed:
    with open(proj_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(proj)

# ═══════════════════════════════════════════════════
# 10. Git commit
# ═══════════════════════════════════════════════════
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "feat: boundary, main menu, save system, audio manager, transition"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git error: {e} — commit manual jika perlu")

print("\n" + "=" * 52)
print("  SELESAI! Sekarang:")
print("  1. Godot → Project → Reload Current Project")
print("  2. Tekan F5 — Main Menu muncul pertama!")
print("  3. Klik 'Mulai Petualangan Baru'")
print("  4. Jalan ke ujung kiri/kanan — ada boundary!")
print("  5. Progress tersimpan otomatis saat pindah scene")
print("=" * 52 + "\n")
