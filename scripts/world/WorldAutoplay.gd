# =============================================================
#  scripts/world/WorldAutoplay.gd
#  Attach ke WorldMap node — play BGM otomatis
# =============================================================
extends Node2D


func _ready() -> void:
	AudioManager.play_bgm("world")
