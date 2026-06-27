# =============================================================
#  scripts/world/ParallaxSky.gd
#  Tempelkan ke node Sky (ColorRect) di WorldMap
#  Sky bergerak 20% dari kecepatan kamera — memberi kesan depth
# =============================================================
extends Node2D

const PARALLAX_FACTOR : float = 0.15

var _start_x   : float = 0.0
var _camera    : Camera2D


func _ready() -> void:
	_start_x = position.x
	await get_tree().process_frame
	# Cari Camera2D di dalam Player
	var player = get_tree().get_first_node_in_group("player")
	if player:
		_camera = player.get_node_or_null("Camera2D")


func _process(_delta: float) -> void:
	if not _camera:
		return
	position.x = _start_x + _camera.get_screen_center_position().x * PARALLAX_FACTOR
