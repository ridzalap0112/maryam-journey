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
	assert(_sprite != null, "AnimatedSprite2D tidak ditemukan!")
	add_to_group("player")
	_play_anim("idle")


func _physics_process(delta: float) -> void:
	_apply_gravity(delta)
	_handle_movement()
	_handle_jump()
	move_and_slide()
	_enforce_boundary()
	_update_animation()


func _apply_gravity(delta: float) -> void:
	if not is_on_floor():
		velocity.y += GRAVITY * delta
		velocity.y = min(velocity.y, 1400.0)


func _handle_movement() -> void:
	var dir := Input.get_axis("move_left", "move_right")
	velocity.x = dir * SPEED
	if dir != 0.0:
		_sprite.flip_h = dir < 0.0


func _handle_jump() -> void:
	if is_on_floor() and Input.is_action_just_pressed("jump"):
		velocity.y = JUMP_FORCE


func _enforce_boundary() -> void:
	var pos := global_position
	if pos.x < WORLD_LEFT:
		pos.x = WORLD_LEFT
		velocity.x = 0.0
	if pos.x > WORLD_RIGHT:
		pos.x = WORLD_RIGHT
		velocity.x = 0.0
	if pos.y < WORLD_TOP:
		pos.y = WORLD_TOP
		velocity.y = 0.0
	if pos.y > FLOOR_Y + 20.0:
		pos.y = FLOOR_Y
		velocity.y = 0.0
	global_position = pos


func _update_animation() -> void:
	var next := "idle"
	if not is_on_floor():
		next = "jump"
	elif abs(velocity.x) > 10.0:
		next = "walk"
	_play_anim(next)


func _play_anim(anim_name: String) -> void:
	if _anim_current == anim_name:
		return
	if _sprite.sprite_frames and _sprite.sprite_frames.has_animation(anim_name):
		_anim_current = anim_name
		_sprite.play(anim_name)
