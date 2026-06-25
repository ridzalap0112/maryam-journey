"""
Maryam Journey - Fix Player.gd (Parse Error)
Jalankan di PowerShell di folder maryam-journey:
  python fix_player.py
"""
import os

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Fix Player.gd")
print("=" * 48)

player_gd = open(os.path.join(BASE, "scripts", "player", "Player.gd"), "w", encoding="utf-8", newline="\n")
player_gd.write("""\
# =============================================================
#  scripts/player/Player.gd
#  Karakter Maryam — Godot 4.7
# =============================================================
extends CharacterBody2D

const SPEED      : float = 160.0
const GRAVITY    : float = 700.0
const JUMP_FORCE : float = -360.0

@onready var _sprite : AnimatedSprite2D = $AnimatedSprite2D

var _anim_current : String = ""


func _ready() -> void:
\tassert(_sprite != null, "AnimatedSprite2D tidak ditemukan!")
\t_play_anim("idle")


func _physics_process(delta: float) -> void:
\t_apply_gravity(delta)
\t_handle_movement()
\t_handle_jump()
\t_update_animation()
\tmove_and_slide()


func _apply_gravity(delta: float) -> void:
\tif not is_on_floor():
\t\tvelocity.y += GRAVITY * delta


func _handle_movement() -> void:
\tvar dir := Input.get_axis("move_left", "move_right")
\tvelocity.x = dir * SPEED
\tif dir != 0.0:
\t\t_sprite.flip_h = dir < 0.0


func _handle_jump() -> void:
\tif is_on_floor() and Input.is_action_just_pressed("jump"):
\t\tvelocity.y = JUMP_FORCE


func _update_animation() -> void:
\tvar next : String
\tif not is_on_floor():
\t\tnext = "jump"
\telif velocity.x != 0.0:
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
player_gd.close()
print("  ✅  scripts/player/Player.gd")

game_manager = open(os.path.join(BASE, "scripts", "managers", "GameManager.gd"), "w", encoding="utf-8", newline="\n")
game_manager.write("""\
# =============================================================
#  scripts/managers/GameManager.gd
#  Autoload — tersedia di seluruh scene
# =============================================================
extends Node

var player_name        : String = "Maryam"
var total_stars        : int    = 0
var unlocked_locations : Array  = ["masjid"]

signal star_collected(total: int)
signal location_unlocked(location_name: String)


func _ready() -> void:
\tprint("[MaryamJourney] Assalamu'alaikum! Game dimulai.")


func add_star(amount: int = 1) -> void:
\ttotal_stars += amount
\tstar_collected.emit(total_stars)
\tprint("[MaryamJourney] Bintang: ", total_stars)


func unlock_location(location_name: String) -> void:
\tif location_name not in unlocked_locations:
\t\tunlocked_locations.append(location_name)
\t\tlocation_unlocked.emit(location_name)
\t\tprint("[MaryamJourney] Lokasi terbuka: ", location_name)


func is_location_unlocked(location_name: String) -> bool:
\treturn location_name in unlocked_locations
""")
game_manager.close()
print("  ✅  scripts/managers/GameManager.gd")

print("\n" + "=" * 48)
print("  SELESAI! Sekarang:")
print("  1. Kembali ke Godot")
print("  2. Klik Project > Reload Current Project")
print("  3. Tekan F5")
print("=" * 48 + "\n")
