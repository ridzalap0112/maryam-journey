# =============================================================
#  scripts/world/WorldBackground.gd
#  Menggerakkan awan secara otomatis
# =============================================================
extends Node2D

const CLOUD_SPEED : float = 18.0
const WORLD_WIDTH : float = 1280.0

@onready var _clouds : Array = []


func _ready() -> void:
	for child in get_children():
		if child.name.begins_with("Cloud"):
			_clouds.append(child)


func _process(delta: float) -> void:
	for cloud in _clouds:
		cloud.position.x += CLOUD_SPEED * delta
		if cloud.position.x > WORLD_WIDTH + 200.0:
			cloud.position.x = -200.0
