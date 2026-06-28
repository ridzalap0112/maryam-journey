"""
Maryam Journey - Fix Spawn Position
Keluar dari lokasi → spawn tepat di depan bangunan itu
python fix_spawn_position.py
"""
import os, subprocess

BASE = os.getcwd()
SCRIPT_PATH = os.path.abspath(__file__)

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Fix Spawn Position")
print("=" * 48)

# ── 1. GameManager.gd — tambah last_position ─────────────────
write(os.path.join(BASE, "scripts", "managers", "GameManager.gd"), """\
# =============================================================
#  scripts/managers/GameManager.gd
# =============================================================
extends Node

var player_name        : String  = "Maryam"
var total_stars        : int     = 0
var unlocked_locations : Array   = ["masjid","pondok","taman","kebun","rumah"]
var last_x             : float   = 200.0

signal star_collected(total: int)
signal location_unlocked(location_name: String)


func _ready() -> void:
\tprint("[MaryamJourney] Assalamu'alaikum!")


func add_star(amount: int = 1) -> void:
\ttotal_stars += amount
\tstar_collected.emit(total_stars)
\tSaveManager.save()


func unlock_location(loc: String) -> void:
\tif loc not in unlocked_locations:
\t\tunlocked_locations.append(loc)
\t\tlocation_unlocked.emit(loc)
\t\tSaveManager.save()


func is_location_unlocked(loc: String) -> bool:
\treturn loc in unlocked_locations


func set_last_position(x: float) -> void:
\tlast_x = x
\tSaveManager.save()
""")

# ── 2. SaveManager.gd — simpan & load last_x ─────────────────
write(os.path.join(BASE, "scripts", "managers", "SaveManager.gd"), """\
# =============================================================
#  scripts/managers/SaveManager.gd
# =============================================================
extends Node

const SAVE_PATH : String = "user://maryam_save.json"


func save() -> void:
\tvar data := {
\t\t"player_name"        : GameManager.player_name,
\t\t"total_stars"        : GameManager.total_stars,
\t\t"unlocked_locations" : GameManager.unlocked_locations,
\t\t"last_x"             : GameManager.last_x,
\t}
\tvar file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
\tif file:
\t\tfile.store_string(JSON.stringify(data))
\t\tfile.close()


func load_save() -> bool:
\tif not FileAccess.file_exists(SAVE_PATH):
\t\treturn false
\tvar file := FileAccess.open(SAVE_PATH, FileAccess.READ)
\tif not file:
\t\treturn false
\tvar raw  := file.get_as_text()
\tfile.close()
\tvar json := JSON.new()
\tif json.parse(raw) != OK:
\t\tdelete_save()
\t\treturn false
\tvar data : Dictionary = json.get_data()
\tGameManager.player_name        = data.get("player_name", "Maryam")
\tGameManager.total_stars        = data.get("total_stars", 0)
\tGameManager.unlocked_locations = data.get("unlocked_locations",
\t\t["masjid","pondok","taman","kebun","rumah"])
\tGameManager.last_x             = data.get("last_x", 200.0)
\treturn true


func delete_save() -> void:
\tif FileAccess.file_exists(SAVE_PATH):
\t\tDirAccess.remove_absolute(SAVE_PATH)


func has_save() -> bool:
\treturn FileAccess.file_exists(SAVE_PATH)
""")

# ── 3. LocationZone.gd — simpan posisi sebelum masuk scene ───
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
\t_label.text    = location_name
\t_hint.text     = "▼ Tekan Enter"
\t_panel.visible = false
\tbody_entered.connect(_on_entered)
\tbody_exited.connect(_on_exited)


func _process(delta: float) -> void:
\tif not _inside:
\t\treturn
\t_bob_time       += delta
\t_panel.position.y = -140.0 + sin(_bob_time * 2.8) * 6.0
\tif Input.is_action_just_pressed("interact"):
\t\t_enter()


func _on_entered(body: Node2D) -> void:
\tif not body.is_in_group("player"):
\t\treturn
\t_inside           = true
\t_bob_time         = 0.0
\t_panel.position.y = -140.0
\t_panel.visible    = true
\tif not GameManager.is_location_unlocked(location_key):
\t\t_hint.text = "🔒 Terkunci"
\telse:
\t\t_hint.text = "▼ Tekan Enter"


func _on_exited(body: Node2D) -> void:
\tif body.is_in_group("player"):
\t\t_inside        = false
\t\t_panel.visible = false


func _enter() -> void:
\tif not GameManager.is_location_unlocked(location_key):
\t\treturn
\tif scene_path == "" or not ResourceLoader.exists(scene_path):
\t\tprint("[Zone] Scene belum ada: ", location_name)
\t\treturn
\t# Simpan posisi player sekarang sebelum pindah scene
\tvar player := get_tree().get_first_node_in_group("player")
\tif player:
\t\tGameManager.set_last_position(player.global_position.x)
\tTransitionManager.go_to(scene_path)
""")

# ── 4. Player.gd — spawn di last_x saat WorldMap dibuka ──────
write(os.path.join(BASE, "scripts", "player", "Player.gd"), """\
# =============================================================
#  scripts/player/Player.gd  —  Godot 4.7
# =============================================================
extends CharacterBody2D

const SPEED       : float = 200.0
const GRAVITY     : float = 800.0
const JUMP_FORCE  : float = -420.0
const WORLD_LEFT  : float = 40.0
const WORLD_RIGHT : float = 4760.0
const WORLD_TOP   : float = 50.0
const FLOOR_Y     : float = 554.0

@onready var _sprite : AnimatedSprite2D = $AnimatedSprite2D
var _anim_current : String = ""


func _ready() -> void:
\tassert(_sprite != null, "AnimatedSprite2D tidak ditemukan!")
\tadd_to_group("player")
\t_play_anim("idle")
\t# Spawn di posisi terakhir (depan lokasi yang baru dikunjungi)
\tglobal_position.x = GameManager.last_x
\tglobal_position.y = FLOOR_Y


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
\tif pos.x < WORLD_LEFT:
\t\tpos.x = WORLD_LEFT
\t\tvelocity.x = 0.0
\tif pos.x > WORLD_RIGHT:
\t\tpos.x = WORLD_RIGHT
\t\tvelocity.x = 0.0
\tif pos.y < WORLD_TOP:
\t\tpos.y = WORLD_TOP
\t\tvelocity.y = 0.0
\tif pos.y > FLOOR_Y + 20.0:
\t\tpos.y = FLOOR_Y
\t\tvelocity.y = 0.0
\tglobal_position = pos


func _update_animation() -> void:
\tvar next := "idle"
\tif not is_on_floor():
\t\tnext = "jump"
\telif abs(velocity.x) > 10.0:
\t\tnext = "walk"
\t_play_anim(next)


func _play_anim(anim_name: String) -> void:
\tif _anim_current == anim_name:
\t\treturn
\tif _sprite.sprite_frames and _sprite.sprite_frames.has_animation(anim_name):
\t\t_anim_current = anim_name
\t\t_sprite.play(anim_name)
""")

# ── 5. Git commit ─────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "feat: spawn player di depan lokasi setelah keluar scene"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

# ── 6. Auto-delete ────────────────────────────────────────────
try:
    os.remove(SCRIPT_PATH)
    print("  ✅  Script dihapus otomatis")
except:
    pass

print("\n" + "=" * 48)
print("  SELESAI!")
print("  Godot → Reload → F5")
print("  Masuk Masjid → selesai/balik")
print("  → Maryam muncul tepat di depan Masjid!")
print("=" * 48 + "\n")
