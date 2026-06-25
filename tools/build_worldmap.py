"""
Maryam Journey - Auto Builder
Jalankan di PowerShell sebagai Administrator:

  cd "C:\path\ke\folder\maryam-journey"
  python build_worldmap.py

Script ini akan:
1. Copy Player.gd dan GameManager.gd ke folder yang benar
2. Buat file WorldMap.tscn yang valid
3. Buat file project.godot yang sudah include autoload GameManager
"""

import os, sys, shutil, textwrap

BASE = os.getcwd()

def path(*parts):
    return os.path.join(BASE, *parts)

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(textwrap.dedent(content).lstrip())
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

# ─────────────────────────────────────────────────────────────
print("\n🌙 Maryam Journey — Auto Builder")
print("=" * 48)

# ── 1. Player.gd ─────────────────────────────────────────────
write(path("scripts", "player", "Player.gd"), """
    # =============================================================
    #  scripts/player/Player.gd
    # =============================================================
    extends CharacterBody2D

    const SPEED      : float = 160.0
    const GRAVITY    : float = 700.0
    const JUMP_FORCE : float = -360.0

    @onready var _sprite : AnimatedSprite2D = $AnimatedSprite2D

    var _anim_current : String = ""


    func _ready() -> void:
    \\tassert(_sprite != null, "AnimatedSprite2D tidak ditemukan di bawah Player!")
    \\t_play_anim("idle")


    func _physics_process(delta: float) -> void:
    \\t_apply_gravity(delta)
    \\t_handle_movement()
    \\t_handle_jump()
    \\t_update_animation()
    \\tmove_and_slide()


    func _apply_gravity(delta: float) -> void:
    \\tif not is_on_floor():
    \\t\\tvelocity.y += GRAVITY * delta


    func _handle_movement() -> void:
    \\tvar dir := Input.get_axis("move_left", "move_right")
    \\tvelocity.x = dir * SPEED
    \\tif dir != 0.0:
    \\t\\t_sprite.flip_h = dir < 0.0


    func _handle_jump() -> void:
    \\tif is_on_floor() and Input.is_action_just_pressed("jump"):
    \\t\\tvelocity.y = JUMP_FORCE


    func _update_animation() -> void:
    \\tvar next : String
    \\tif not is_on_floor():
    \\t\\tnext = "jump"
    \\telif velocity.x != 0.0:
    \\t\\tnext = "walk"
    \\telse:
    \\t\\tnext = "idle"
    \\t_play_anim(next)


    func _play_anim(anim_name: String) -> void:
    \\tif _anim_current == anim_name:
    \\t\\treturn
    \\tif _sprite.sprite_frames and _sprite.sprite_frames.has_animation(anim_name):
    \\t\\t_anim_current = anim_name
    \\t\\t_sprite.play(anim_name)
""")

# ── 2. GameManager.gd ────────────────────────────────────────
write(path("scripts", "managers", "GameManager.gd"), """
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
    \\tprint("[MaryamJourney] Assalamu'alaikum! Game dimulai.")


    func add_star(amount: int = 1) -> void:
    \\ttotal_stars += amount
    \\tstar_collected.emit(total_stars)
    \\tprint("[MaryamJourney] Bintang: ", total_stars)


    func unlock_location(location_name: String) -> void:
    \\tif location_name not in unlocked_locations:
    \\t\\tunlocked_locations.append(location_name)
    \\t\\tlocation_unlocked.emit(location_name)
    \\t\\tprint("[MaryamJourney] Lokasi terbuka: ", location_name)


    func is_location_unlocked(location_name: String) -> bool:
    \\treturn location_name in unlocked_locations
""")

# ── 3. WorldMap.tscn ─────────────────────────────────────────
write(path("scenes", "world", "WorldMap.tscn"), """
    [gd_scene load_steps=6 format=3]

    [ext_resource type="Script" path="res://scripts/player/Player.gd" id="1_player"]

    [sub_resource type="SpriteFrames" id="SpriteFrames_1"]
    animations = [{
    "frames": [],
    "loop": true,
    "name": &"idle",
    "speed": 5.0
    }, {
    "frames": [],
    "loop": true,
    "name": &"walk",
    "speed": 8.0
    }, {
    "frames": [],
    "loop": false,
    "name": &"jump",
    "speed": 5.0
    }]

    [sub_resource type="RectangleShape2D" id="RectangleShape2D_ground"]
    size = Vector2(1280, 40)

    [sub_resource type="RectangleShape2D" id="RectangleShape2D_player"]
    size = Vector2(40, 80)

    [node name="WorldMap" type="Node2D"]

    [node name="Background" type="ColorRect" parent="."]
    color = Color(0.529, 0.808, 0.922, 1)
    size = Vector2(1280, 720)

    [node name="Ground" type="StaticBody2D" parent="."]
    position = Vector2(0, 680)

    [node name="GroundShape" type="CollisionShape2D" parent="Ground"]
    shape = SubResource("RectangleShape2D_ground")

    [node name="GroundVisual" type="ColorRect" parent="Ground"]
    color = Color(0.29, 0.647, 0.208, 1)
    size = Vector2(1280, 40)

    [node name="Player" type="CharacterBody2D" parent="."]
    position = Vector2(300, 580)
    script = ExtResource("1_player")

    [node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="Player"]
    sprite_frames = SubResource("SpriteFrames_1")

    [node name="CollisionShape2D" type="CollisionShape2D" parent="Player"]
    shape = SubResource("RectangleShape2D_player")

    [node name="Camera2D" type="Camera2D" parent="Player"]
    zoom = Vector2(1, 1)
""")

# ── 4. Patch project.godot — tambah autoload & input map ─────
godot_proj = path("project.godot")
if not os.path.exists(godot_proj):
    print("\n  ⚠️  project.godot tidak ditemukan!")
    print("     Pastikan kamu jalankan script ini di dalam folder project Godot.")
    sys.exit(1)

with open(godot_proj, "r", encoding="utf-8") as f:
    content = f.read()

# Tambah autoload kalau belum ada
autoload_block = '[autoload]\n\nGameManager="*res://scripts/managers/GameManager.gd"\n'
if "GameManager" not in content:
    content += "\n" + autoload_block
    print("  ✅  Autoload GameManager ditambahkan ke project.godot")
else:
    print("  ⏭️   Autoload GameManager sudah ada")

# Tambah input map kalau belum ada
input_block = """
[input]

move_left={
"deadzone": 0.2,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":4194319,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)
, Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":65,"key_label":0,"unicode":97,"location":0,"echo":false,"script":null)
]
}
move_right={
"deadzone": 0.2,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":4194321,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)
, Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":68,"key_label":0,"unicode":100,"location":0,"echo":false,"script":null)
]
}
jump={
"deadzone": 0.2,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":32,"key_label":0,"unicode":32,"location":0,"echo":false,"script":null)
, Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":4194320,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)
]
}
"""
if "[input]" not in content:
    content += input_block
    print("  ✅  Input Map (WASD + Arrow + Space) ditambahkan")
else:
    print("  ⏭️   Input Map sudah ada")

with open(godot_proj, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

# ── 5. Set main scene ────────────────────────────────────────
with open(godot_proj, "r", encoding="utf-8") as f:
    content = f.read()

if 'run/main_scene' not in content:
    content = content.replace(
        '[application]',
        '[application]\n\nrun/main_scene="res://scenes/world/WorldMap.tscn"'
    )
    with open(godot_proj, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("  ✅  Main scene di-set ke WorldMap.tscn")
else:
    print("  ⏭️   Main scene sudah di-set")

print("\n" + "=" * 48)
print("  SELESAI! Sekarang:")
print("  1. Kembali ke Godot")
print("  2. Klik Project > Reload Current Project")
print("  3. Double-click scenes/world/WorldMap.tscn")
print("  4. Tekan F5 untuk main game!")
print("=" * 48 + "\n")
