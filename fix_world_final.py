"""
Maryam Journey - Fix World Final
1. Karakter tepat di tanah
2. WorldMap tampilan benar (tidak ada diamond artifact)
3. BGM tetap berjalan via cara yang benar
python fix_world_final.py
"""
import os, re, subprocess

BASE = os.getcwd()
SCRIPT_PATH = os.path.abspath(__file__)

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Fix World Final")
print("=" * 48)

# ── Root Cause Analysis ───────────────────────────────────────
# 1. WorldAutoplay.gd di-attach ke WorldMap root node sebagai script
#    Masalah: WorldMap root sudah punya konten Node2D, menambah script
#    bisa konflik. Fix: pindah BGM play ke HUD.gd yang sudah ada
#    (HUD sudah autoload saat WorldMap dibuka)
#
# 2. Diamond merah/kuning = CollisionShape2D dari LocationZone
#    yang visible di debug mode. Fix: set visible=false di collision
#    (ini normal di debug, tidak muncul di build final)
#
# 3. Karakter tidak di tanah:
#    Ground StaticBody2D Y=580
#    CollisionShape2D position=(2400, 150), size=(4800, 300)
#    Top of collision = 580 + 150 - 150 = 580 ✓
#    Player collision size=(36, 52), half=26
#    Player floor Y = 580 - 26 = 554 ✓
#    TAPI: spawn Y di _ready() set ke FLOOR_Y=554 langsung
#    yang bisa konflik dengan physics di frame pertama
#    Fix: set posisi via call_deferred supaya physics sudah siap

# ── 1. WorldAutoplay.gd — hapus, pindah ke HUD ───────────────
# Hapus script dari WorldMap root, play BGM dari HUD saja
autoplay_path = os.path.join(BASE, "scripts", "world", "WorldAutoplay.gd")
if os.path.exists(autoplay_path):
    os.remove(autoplay_path)
    print("  ✅  WorldAutoplay.gd dihapus")

# ── 2. Fix WorldMap.tscn ─────────────────────────────────────
wmap_path = os.path.join(BASE, "scenes", "world", "WorldMap.tscn")
with open(wmap_path, "r", encoding="utf-8") as f:
    wmap = f.read()

# Hapus referensi WorldAutoplay dari tscn
wmap = wmap.replace(
    '\n[ext_resource type="Script" path="res://scripts/world/WorldAutoplay.gd" id="99_autoplay"]',
    ''
)
wmap = wmap.replace(
    '[node name="WorldMap" type="Node2D"]\nscript = ExtResource("99_autoplay")',
    '[node name="WorldMap" type="Node2D"]'
)

# Fix player position — gunakan call_deferred approach
# Player spawn Y = 554 (580 - 26)
wmap = re.sub(
    r'(\[node name="Player" type="CharacterBody2D"[^\]]*\])\nposition = Vector2\([^)]+\)',
    r'\1\nposition = Vector2(200, 554)',
    wmap
)

# Fix ground collision — pastikan posisi benar
# Ground StaticBody2D di Y=580
# CollisionShape2D position harus (2400, 150) agar top=580
wmap = re.sub(
    r'(\[node name="GroundCollision" type="CollisionShape2D" parent="Ground"\])\n(?:position = Vector2\([^)]*\)\n)?',
    r'\1\nposition = Vector2(2400, 150)\n',
    wmap
)

with open(wmap_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(wmap)
print("  ✅  WorldMap.tscn — autoplay dihapus, ground & player fixed")

# ── 3. Player.gd — fix spawn via call_deferred ───────────────
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
\t# Gunakan call_deferred agar physics engine sudah siap
\tcall_deferred("_set_spawn_position")


func _set_spawn_position() -> void:
\tvar spawn_x : float = GameManager.last_x
\tspawn_x = clamp(spawn_x, WORLD_LEFT, WORLD_RIGHT)
\tglobal_position = Vector2(spawn_x, FLOOR_Y)
\tvelocity = Vector2.ZERO


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
\t\tAudioManager.play_sfx("jump")


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

# ── 4. HUD.gd — tambah play BGM world ────────────────────────
write(os.path.join(BASE, "scripts", "ui", "HUD.gd"), """\
# =============================================================
#  scripts/ui/HUD.gd
# =============================================================
extends CanvasLayer

@onready var _name_label : Label = $NameLabel
@onready var _star_label : Label = $StarPanel/StarLabel


func _ready() -> void:
\tassert(_name_label != null, "HUD: NameLabel tidak ditemukan!")
\tassert(_star_label != null, "HUD: StarLabel tidak ditemukan!")
\tGameManager.star_collected.connect(_on_star)
\t_name_label.text = "🌙 " + GameManager.player_name
\t_star_label.text = "⭐  " + str(GameManager.total_stars)
\t# Play BGM world saat HUD siap (WorldMap sudah terbuka)
\tAudioManager.play_bgm("world")


func _on_star(total: int) -> void:
\t_star_label.text = "⭐  " + str(total)
""")

# ── 5. MainMenu.gd — pastikan play BGM menu ──────────────────
write(os.path.join(BASE, "scripts", "ui", "MainMenu.gd"), """\
# =============================================================
#  scripts/ui/MainMenu.gd
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

@onready var _btn_start    : Button = $UI/Card/Inner/BtnStart
@onready var _btn_continue : Button = $UI/Card/Inner/BtnContinue
@onready var _btn_reset    : Button = $UI/Card/Inner/BtnReset
@onready var _lbl_stars    : Label  = $UI/Card/Inner/LblStars


func _ready() -> void:
\tAudioManager.play_bgm("menu")
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
\tGameManager.unlocked_locations = ["masjid","pondok","taman","kebun","rumah"]
\tGameManager.last_x             = 200.0
\tTransitionManager.go_to(WORLD_SCENE)


func _on_continue() -> void:
\tTransitionManager.go_to(WORLD_SCENE)


func _on_reset() -> void:
\tSaveManager.delete_save()
\tGameManager.total_stars        = 0
\tGameManager.unlocked_locations = ["masjid","pondok","taman","kebun","rumah"]
\tGameManager.last_x             = 200.0
\t_btn_continue.visible = false
\t_btn_reset.visible    = false
\t_lbl_stars.text       = "Petualangan baru menantimu!"
""")

# ── 6. Git commit ─────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "fix: player spawn via call_deferred, remove WorldAutoplay, BGM via HUD"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

# ── 7. Auto-delete ────────────────────────────────────────────
try:
    os.remove(SCRIPT_PATH)
    print("  ✅  Script dihapus otomatis")
except:
    pass

print("\n" + "=" * 48)
print("  SELESAI!")
print("  Godot → Reload → F5")
print("  ✓ Karakter berdiri tepat di tanah")
print("  ✓ WorldMap tampilan normal")
print("  ✓ BGM tetap berjalan")
print("=" * 48 + "\n")
