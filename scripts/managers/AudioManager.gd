# =============================================================
#  scripts/managers/AudioManager.gd
#  Autoload — kelola musik & SFX
#  Daftarkan di: Project > Autoload > AudioManager
#  Nanti tinggal isi file audio di assets/audio/
# =============================================================
extends Node

# Path audio (isi saat sudah ada file)
const BGM_WORLD  : String = "res://assets/audio/music/bgm_world.ogg"
const SFX_JUMP   : String = "res://assets/audio/sfx/jump.wav"
const SFX_STAR   : String = "res://assets/audio/sfx/star.wav"
const SFX_ENTER  : String = "res://assets/audio/sfx/enter_location.wav"

var _bgm  : AudioStreamPlayer
var _sfx  : AudioStreamPlayer


func _ready() -> void:
	_bgm = AudioStreamPlayer.new()
	_bgm.bus = "Music"
	_bgm.volume_db = -8.0
	add_child(_bgm)

	_sfx = AudioStreamPlayer.new()
	_sfx.bus = "SFX"
	add_child(_sfx)


func play_bgm(path: String) -> void:
	if not ResourceLoader.exists(path):
		return
	if _bgm.playing and _bgm.stream and _bgm.stream.resource_path == path:
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


func set_bgm_volume(db: float) -> void:
	_bgm.volume_db = db


func set_sfx_volume(db: float) -> void:
	_sfx.volume_db = db
