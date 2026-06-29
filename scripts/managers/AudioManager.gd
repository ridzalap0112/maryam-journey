# =============================================================
#  scripts/managers/AudioManager.gd
#  Autoload — musik latar procedural + SFX
#  Tidak butuh file audio eksternal!
# =============================================================
extends Node

# ── Volume settings ───────────────────────────────────────────
var bgm_volume   : float = 0.7
var sfx_volume   : float = 1.0
var bgm_enabled  : bool  = true
var sfx_enabled  : bool  = true

# ── Node audio ────────────────────────────────────────────────
var _bgm_player  : AudioStreamPlayer
var _sfx_player  : AudioStreamPlayer
var _gen_player  : AudioStreamPlayer
var _playback    : AudioStreamGeneratorPlayback

# ── State musik ───────────────────────────────────────────────
var _time        : float = 0.0
var _beat        : float = 0.0
var _bpm         : float = 80.0
var _playing_bgm : bool  = false
var _current_bgm : String = ""

# Nada-nada untuk melodi Islami yang tenang (frekuensi Hz)
# Tangga nada Hijaz: D E♭ F# G A B♭ C D
const SCALE_WORLD : Array[float] = [
	293.66, 311.13, 369.99, 392.00,
	440.00, 466.16, 523.25, 587.33
]
const SCALE_MENU : Array[float] = [
	261.63, 293.66, 329.63, 349.23,
	392.00, 440.00, 493.88, 523.25
]

var _melody_world : Array[int] = [0,2,4,5,4,2,0,1,2,4,6,5,4,2,3,1]
var _melody_menu  : Array[int] = [0,1,2,4,4,2,1,0,0,3,5,4,3,1,2,0]
var _melody_idx   : int        = 0
var _active_scale : Array[float] = []
var _active_melody: Array[int]   = []
var _note_timer   : float        = 0.0
var _note_dur     : float        = 0.75


func _ready() -> void:
	_setup_players()


func _setup_players() -> void:
	# BGM player via AudioStreamGenerator
	var gen            := AudioStreamGenerator.new()
	gen.mix_rate       = 44100.0
	gen.buffer_length  = 0.1
	_gen_player        = AudioStreamPlayer.new()
	_gen_player.stream = gen
	_gen_player.volume_db = linear_to_db(bgm_volume * 0.3)
	add_child(_gen_player)

	# SFX player
	_sfx_player = AudioStreamPlayer.new()
	_sfx_player.volume_db = linear_to_db(sfx_volume)
	add_child(_sfx_player)


func _process(delta: float) -> void:
	if not _playing_bgm or not bgm_enabled:
		return
	_time       += delta
	_note_timer += delta
	if _note_timer >= _note_dur:
		_note_timer = 0.0
		_play_next_note()
	_fill_buffer()


func _fill_buffer() -> void:
	if not _gen_player.playing:
		return
	if _playback == null:
		return
	var frames_avail : int = _playback.get_frames_available()
	if frames_avail <= 0:
		return
	var sample_rate  : float = 44100.0
	for _i in frames_avail:
		_time += 1.0 / sample_rate
		var sample : float = 0.0
		# Nada saat ini sudah di-handle oleh _current_freq
		sample = sin(_time * _current_freq * TAU) * _current_amp * _env
		_env   = max(0.0, _env - _env_decay)
		_playback.push_frame(Vector2(sample, sample))


var _current_freq : float = 440.0
var _current_amp  : float = 0.0
var _env          : float = 0.0
var _env_decay    : float = 0.002


func _play_next_note() -> void:
	if _active_melody.is_empty() or _active_scale.is_empty():
		return
	var idx    : int   = _active_melody[_melody_idx % _active_melody.size()]
	_current_freq      = _active_scale[idx % _active_scale.size()]
	_current_amp       = 0.18
	_env               = 1.0
	_env_decay         = 1.0 / (44100.0 * _note_dur * 0.85)
	_melody_idx        = (_melody_idx + 1) % _active_melody.size()


# ── API Publik ────────────────────────────────────────────────
func play_bgm(track: String = "world") -> void:
	if _current_bgm == track and _playing_bgm:
		return
	_current_bgm   = track
	_playing_bgm   = true
	_melody_idx    = 0
	_note_timer    = 0.0
	_current_amp   = 0.0
	_env           = 0.0
	match track:
		"world":
			_active_scale  = SCALE_WORLD
			_active_melody = _melody_world
			_note_dur      = 0.75
		"menu":
			_active_scale  = SCALE_MENU
			_active_melody = _melody_menu
			_note_dur      = 0.90
		"masjid":
			_active_scale  = SCALE_WORLD
			_active_melody = [0,0,2,4,4,2,0,1,3,5,5,3,1,0,2,4]
			_note_dur      = 1.0
		_:
			_active_scale  = SCALE_MENU
			_active_melody = _melody_menu
			_note_dur      = 0.80
	if not _gen_player.playing:
		_gen_player.play()
		_playback = _gen_player.get_stream_playback()


func stop_bgm() -> void:
	_playing_bgm  = false
	_current_bgm  = ""
	_current_amp  = 0.0
	_env          = 0.0


func play_sfx(sfx_name: String) -> void:
	if not sfx_enabled:
		return
	# Generate SFX procedural
	var gen := AudioStreamGenerator.new()
	gen.mix_rate      = 44100.0
	gen.buffer_length = 0.3
	var player        := AudioStreamPlayer.new()
	player.stream     = gen
	player.volume_db  = linear_to_db(sfx_volume * 0.8)
	add_child(player)
	player.play()
	var pb : AudioStreamGeneratorPlayback = player.get_stream_playback()
	var sr : float = 44100.0
	var samples : int = int(sr * 0.25)
	match sfx_name:
		"click":
			# Suara klik: tone pendek naik
			for i in samples:
				var t   : float = float(i) / sr
				var env : float = 1.0 - (t / 0.25)
				var frq : float = 600.0 + t * 800.0
				var s   : float = sin(t * frq * TAU) * env * 0.4
				pb.push_frame(Vector2(s, s))
		"correct":
			# Suara benar: dua nada naik ceria
			for i in samples:
				var t   : float = float(i) / sr
				var env : float = 1.0 - (t / 0.25)
				var frq : float = 523.25 if t < 0.12 else 659.25
				var s   : float = sin(t * frq * TAU) * env * 0.45
				pb.push_frame(Vector2(s, s))
		"wrong":
			# Suara salah: nada turun pendek
			for i in samples:
				var t   : float = float(i) / sr
				var env : float = 1.0 - (t / 0.25)
				var frq : float = 300.0 - t * 100.0
				var s   : float = sin(t * frq * TAU) * env * 0.35
				pb.push_frame(Vector2(s, s))
		"star":
			# Suara bintang: arpeggio naik
			var notes : Array[float] = [523.25, 659.25, 783.99, 1046.5]
			var ns    : int          = int(sr * 0.06)
			for ni in notes.size():
				for i in ns:
					var t   : float = float(i) / sr
					var env : float = 1.0 - (t / 0.06)
					var s   : float = sin(t * notes[ni] * TAU) * env * 0.40
					pb.push_frame(Vector2(s, s))
		"enter":
			# Suara masuk lokasi: swoosh lembut
			for i in samples:
				var t   : float = float(i) / sr
				var env : float = sin(t / 0.25 * PI)
				var frq : float = 400.0 + sin(t * 8.0) * 80.0
				var s   : float = sin(t * frq * TAU) * env * 0.30
				pb.push_frame(Vector2(s, s))
		"jump":
			# Suara lompat: nada pendek naik
			for i in int(sr * 0.15):
				var t   : float = float(i) / sr
				var env : float = 1.0 - (t / 0.15)
				var frq : float = 350.0 + t * 600.0
				var s   : float = sin(t * frq * TAU) * env * 0.35
				pb.push_frame(Vector2(s, s))
	await get_tree().create_timer(0.35).timeout
	player.queue_free()


func set_bgm_volume(val: float) -> void:
	bgm_volume = clamp(val, 0.0, 1.0)
	_gen_player.volume_db = linear_to_db(bgm_volume * 0.3)


func set_sfx_volume(val: float) -> void:
	sfx_volume = clamp(val, 0.0, 1.0)


func toggle_bgm() -> void:
	bgm_enabled = not bgm_enabled
	if not bgm_enabled:
		_current_amp = 0.0
		_env         = 0.0


func toggle_sfx() -> void:
	sfx_enabled = not sfx_enabled
