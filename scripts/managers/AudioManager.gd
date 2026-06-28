extends Node

var _bgm : AudioStreamPlayer
var _sfx : AudioStreamPlayer


func _ready() -> void:
	_bgm            = AudioStreamPlayer.new()
	_bgm.volume_db  = -8.0
	add_child(_bgm)
	_sfx            = AudioStreamPlayer.new()
	add_child(_sfx)


func play_bgm(path: String) -> void:
	if not ResourceLoader.exists(path):
		return
	_bgm.stream = load(path)
	_bgm.play()


func stop_bgm() -> void:
	_bgm.stop()


func play_sfx(path: String) -> void:
	if not ResourceLoader.exists(path):
		return
	_sfx.stream = load(path)
	_sfx.play()
