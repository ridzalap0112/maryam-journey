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
	assert(_sprite != null, "AnimatedSprite2D tidak ditemukan!")
	_play_anim("idle")


func _physics_process(delta: float) -> void:
	_apply_gravity(delta)
	_handle_movement()
	_handle_jump()
	_update_animation()
	move_and_slide()


func _apply_gravity(delta: float) -> void:
	if not is_on_floor():
		velocity.y += GRAVITY * delta


func _handle_movement() -> void:
	var dir := Input.get_axis("move_left", "move_right")
	velocity.x = dir * SPEED
	if dir != 0.0:
		_sprite.flip_h = dir < 0.0


func _handle_jump() -> void:
	if is_on_floor() and Input.is_action_just_pressed("jump"):
		velocity.y = JUMP_FORCE


func _update_animation() -> void:
	var next : String
	if not is_on_floor():
		next = "jump"
	elif velocity.x != 0.0:
		next = "walk"
	else:
		next = "idle"
	_play_anim(next)


func _play_anim(anim_name: String) -> void:
	if _anim_current == anim_name:
		return
	if _sprite.sprite_frames and _sprite.sprite_frames.has_animation(anim_name):
		_anim_current = anim_name
		_sprite.play(anim_name)
