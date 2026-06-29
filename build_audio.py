"""
Maryam Journey - Build Audio System
Musik latar procedural + SFX via AudioStreamGenerator
Tidak butuh file audio eksternal — suara langsung dari kode!
python build_audio.py
"""
import os, subprocess

BASE = os.getcwd()
SCRIPT_PATH = os.path.abspath(__file__)

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🔊 Maryam Journey — Build Audio System")
print("=" * 52)

# ── 1. AudioManager.gd — sistem audio lengkap ────────────────
# Menggunakan AudioStreamGenerator untuk suara procedural
# + siap menerima file .ogg/.wav kalau sudah ada
write(os.path.join(BASE, "scripts", "managers", "AudioManager.gd"), """\
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
\t293.66, 311.13, 369.99, 392.00,
\t440.00, 466.16, 523.25, 587.33
]
const SCALE_MENU : Array[float] = [
\t261.63, 293.66, 329.63, 349.23,
\t392.00, 440.00, 493.88, 523.25
]

var _melody_world : Array[int] = [0,2,4,5,4,2,0,1,2,4,6,5,4,2,3,1]
var _melody_menu  : Array[int] = [0,1,2,4,4,2,1,0,0,3,5,4,3,1,2,0]
var _melody_idx   : int        = 0
var _active_scale : Array[float] = []
var _active_melody: Array[int]   = []
var _note_timer   : float        = 0.0
var _note_dur     : float        = 0.75


func _ready() -> void:
\t_setup_players()


func _setup_players() -> void:
\t# BGM player via AudioStreamGenerator
\tvar gen            := AudioStreamGenerator.new()
\tgen.mix_rate       = 44100.0
\tgen.buffer_length  = 0.1
\t_gen_player        = AudioStreamPlayer.new()
\t_gen_player.stream = gen
\t_gen_player.volume_db = linear_to_db(bgm_volume * 0.3)
\tadd_child(_gen_player)

\t# SFX player
\t_sfx_player = AudioStreamPlayer.new()
\t_sfx_player.volume_db = linear_to_db(sfx_volume)
\tadd_child(_sfx_player)


func _process(delta: float) -> void:
\tif not _playing_bgm or not bgm_enabled:
\t\treturn
\t_time       += delta
\t_note_timer += delta
\tif _note_timer >= _note_dur:
\t\t_note_timer = 0.0
\t\t_play_next_note()
\t_fill_buffer()


func _fill_buffer() -> void:
\tif not _gen_player.playing:
\t\treturn
\tif _playback == null:
\t\treturn
\tvar frames_avail : int = _playback.get_frames_available()
\tif frames_avail <= 0:
\t\treturn
\tvar sample_rate  : float = 44100.0
\tfor _i in frames_avail:
\t\t_time += 1.0 / sample_rate
\t\tvar sample : float = 0.0
\t\t# Nada saat ini sudah di-handle oleh _current_freq
\t\tsample = sin(_time * _current_freq * TAU) * _current_amp * _env
\t\t_env   = max(0.0, _env - _env_decay)
\t\t_playback.push_frame(Vector2(sample, sample))


var _current_freq : float = 440.0
var _current_amp  : float = 0.0
var _env          : float = 0.0
var _env_decay    : float = 0.002


func _play_next_note() -> void:
\tif _active_melody.is_empty() or _active_scale.is_empty():
\t\treturn
\tvar idx    : int   = _active_melody[_melody_idx % _active_melody.size()]
\t_current_freq      = _active_scale[idx % _active_scale.size()]
\t_current_amp       = 0.18
\t_env               = 1.0
\t_env_decay         = 1.0 / (44100.0 * _note_dur * 0.85)
\t_melody_idx        = (_melody_idx + 1) % _active_melody.size()


# ── API Publik ────────────────────────────────────────────────
func play_bgm(track: String = "world") -> void:
\tif _current_bgm == track and _playing_bgm:
\t\treturn
\t_current_bgm   = track
\t_playing_bgm   = true
\t_melody_idx    = 0
\t_note_timer    = 0.0
\t_current_amp   = 0.0
\t_env           = 0.0
\tmatch track:
\t\t"world":
\t\t\t_active_scale  = SCALE_WORLD
\t\t\t_active_melody = _melody_world
\t\t\t_note_dur      = 0.75
\t\t"menu":
\t\t\t_active_scale  = SCALE_MENU
\t\t\t_active_melody = _melody_menu
\t\t\t_note_dur      = 0.90
\t\t"masjid":
\t\t\t_active_scale  = SCALE_WORLD
\t\t\t_active_melody = [0,0,2,4,4,2,0,1,3,5,5,3,1,0,2,4]
\t\t\t_note_dur      = 1.0
\t\t_:
\t\t\t_active_scale  = SCALE_MENU
\t\t\t_active_melody = _melody_menu
\t\t\t_note_dur      = 0.80
\tif not _gen_player.playing:
\t\t_gen_player.play()
\t\t_playback = _gen_player.get_stream_playback()


func stop_bgm() -> void:
\t_playing_bgm  = false
\t_current_bgm  = ""
\t_current_amp  = 0.0
\t_env          = 0.0


func play_sfx(sfx_name: String) -> void:
\tif not sfx_enabled:
\t\treturn
\t# Generate SFX procedural
\tvar gen := AudioStreamGenerator.new()
\tgen.mix_rate      = 44100.0
\tgen.buffer_length = 0.3
\tvar player        := AudioStreamPlayer.new()
\tplayer.stream     = gen
\tplayer.volume_db  = linear_to_db(sfx_volume * 0.8)
\tadd_child(player)
\tplayer.play()
\tvar pb : AudioStreamGeneratorPlayback = player.get_stream_playback()
\tvar sr : float = 44100.0
\tvar samples : int = int(sr * 0.25)
\tmatch sfx_name:
\t\t"click":
\t\t\t# Suara klik: tone pendek naik
\t\t\tfor i in samples:
\t\t\t\tvar t   : float = float(i) / sr
\t\t\t\tvar env : float = 1.0 - (t / 0.25)
\t\t\t\tvar frq : float = 600.0 + t * 800.0
\t\t\t\tvar s   : float = sin(t * frq * TAU) * env * 0.4
\t\t\t\tpb.push_frame(Vector2(s, s))
\t\t"correct":
\t\t\t# Suara benar: dua nada naik ceria
\t\t\tfor i in samples:
\t\t\t\tvar t   : float = float(i) / sr
\t\t\t\tvar env : float = 1.0 - (t / 0.25)
\t\t\t\tvar frq : float = 523.25 if t < 0.12 else 659.25
\t\t\t\tvar s   : float = sin(t * frq * TAU) * env * 0.45
\t\t\t\tpb.push_frame(Vector2(s, s))
\t\t"wrong":
\t\t\t# Suara salah: nada turun pendek
\t\t\tfor i in samples:
\t\t\t\tvar t   : float = float(i) / sr
\t\t\t\tvar env : float = 1.0 - (t / 0.25)
\t\t\t\tvar frq : float = 300.0 - t * 100.0
\t\t\t\tvar s   : float = sin(t * frq * TAU) * env * 0.35
\t\t\t\tpb.push_frame(Vector2(s, s))
\t\t"star":
\t\t\t# Suara bintang: arpeggio naik
\t\t\tvar notes : Array[float] = [523.25, 659.25, 783.99, 1046.5]
\t\t\tvar ns    : int          = int(sr * 0.06)
\t\t\tfor ni in notes.size():
\t\t\t\tfor i in ns:
\t\t\t\t\tvar t   : float = float(i) / sr
\t\t\t\t\tvar env : float = 1.0 - (t / 0.06)
\t\t\t\t\tvar s   : float = sin(t * notes[ni] * TAU) * env * 0.40
\t\t\t\t\tpb.push_frame(Vector2(s, s))
\t\t"enter":
\t\t\t# Suara masuk lokasi: swoosh lembut
\t\t\tfor i in samples:
\t\t\t\tvar t   : float = float(i) / sr
\t\t\t\tvar env : float = sin(t / 0.25 * PI)
\t\t\t\tvar frq : float = 400.0 + sin(t * 8.0) * 80.0
\t\t\t\tvar s   : float = sin(t * frq * TAU) * env * 0.30
\t\t\t\tpb.push_frame(Vector2(s, s))
\t\t"jump":
\t\t\t# Suara lompat: nada pendek naik
\t\t\tfor i in int(sr * 0.15):
\t\t\t\tvar t   : float = float(i) / sr
\t\t\t\tvar env : float = 1.0 - (t / 0.15)
\t\t\t\tvar frq : float = 350.0 + t * 600.0
\t\t\t\tvar s   : float = sin(t * frq * TAU) * env * 0.35
\t\t\t\tpb.push_frame(Vector2(s, s))
\tawait get_tree().create_timer(0.35).timeout
\tplayer.queue_free()


func set_bgm_volume(val: float) -> void:
\tbgm_volume = clamp(val, 0.0, 1.0)
\t_gen_player.volume_db = linear_to_db(bgm_volume * 0.3)


func set_sfx_volume(val: float) -> void:
\tsfx_volume = clamp(val, 0.0, 1.0)


func toggle_bgm() -> void:
\tbgm_enabled = not bgm_enabled
\tif not bgm_enabled:
\t\t_current_amp = 0.0
\t\t_env         = 0.0


func toggle_sfx() -> void:
\tsfx_enabled = not sfx_enabled
""")

# ── 2. Update WorldMap — play BGM saat masuk ─────────────────
world_autoplay_script = """\
# =============================================================
#  scripts/world/WorldAutoplay.gd
#  Attach ke WorldMap node — play BGM otomatis
# =============================================================
extends Node2D


func _ready() -> void:
\tAudioManager.play_bgm("world")
"""
write(os.path.join(BASE, "scripts", "world", "WorldAutoplay.gd"), world_autoplay_script)

# ── 3. Patch WorldMap.tscn — attach WorldAutoplay.gd ─────────
wmap_path = os.path.join(BASE, "scenes", "world", "WorldMap.tscn")
with open(wmap_path, "r", encoding="utf-8") as f:
    wmap = f.read()

if "WorldAutoplay.gd" not in wmap:
    # Tambah ext_resource
    wmap = wmap.replace(
        "[ext_resource type=\"Script\" path=\"res://scripts/player/Player.gd\" id=\"1_player\"]",
        "[ext_resource type=\"Script\" path=\"res://scripts/player/Player.gd\" id=\"1_player\"]\n[ext_resource type=\"Script\" path=\"res://scripts/world/WorldAutoplay.gd\" id=\"99_autoplay\"]"
    )
    # Attach ke WorldMap node
    wmap = wmap.replace(
        "[node name=\"WorldMap\" type=\"Node2D\"]",
        "[node name=\"WorldMap\" type=\"Node2D\"]\nscript = ExtResource(\"99_autoplay\")"
    )
    with open(wmap_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(wmap)
    print("  ✅  WorldMap.tscn — BGM autoplay ditambahkan")

# ── 4. Update MainMenu — play BGM menu ───────────────────────
menu_gd_path = os.path.join(BASE, "scripts", "ui", "MainMenu.gd")
with open(menu_gd_path, "r", encoding="utf-8") as f:
    menu_gd = f.read()

if "AudioManager.play_bgm" not in menu_gd:
    menu_gd = menu_gd.replace(
        "\t_btn_start.pressed.connect(_on_start)",
        "\tAudioManager.play_bgm(\"menu\")\n\t_btn_start.pressed.connect(_on_start)"
    )
    with open(menu_gd_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(menu_gd)
    print("  ✅  MainMenu.gd — BGM menu ditambahkan")

# ── 5. Update LocationZone — SFX enter ───────────────────────
zone_path = os.path.join(BASE, "scripts", "locations", "LocationZone.gd")
with open(zone_path, "r", encoding="utf-8") as f:
    zone = f.read()

if "AudioManager.play_sfx" not in zone:
    zone = zone.replace(
        "\tTransitionManager.go_to(scene_path)",
        "\tAudioManager.play_sfx(\"enter\")\n\tTransitionManager.go_to(scene_path)"
    )
    with open(zone_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(zone)
    print("  ✅  LocationZone.gd — SFX enter ditambahkan")

# ── 6. Update Player — SFX jump ──────────────────────────────
player_path = os.path.join(BASE, "scripts", "player", "Player.gd")
with open(player_path, "r", encoding="utf-8") as f:
    player = f.read()

if "AudioManager.play_sfx" not in player:
    player = player.replace(
        "\tif is_on_floor() and Input.is_action_just_pressed(\"jump\"):\n\t\tvelocity.y = JUMP_FORCE",
        "\tif is_on_floor() and Input.is_action_just_pressed(\"jump\"):\n\t\tvelocity.y = JUMP_FORCE\n\t\tAudioManager.play_sfx(\"jump\")"
    )
    with open(player_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(player)
    print("  ✅  Player.gd — SFX jump ditambahkan")

# ── 7. Update MasjidScene — SFX klik & star ──────────────────
masjid_path = os.path.join(BASE, "scripts", "locations", "MasjidScene.gd")
with open(masjid_path, "r", encoding="utf-8") as f:
    masjid = f.read()

if "AudioManager" not in masjid:
    masjid = masjid.replace(
        "func _ready() -> void:\n\tassert(_sprite_frames",
        "func _ready() -> void:\n\tAudioManager.play_bgm(\"masjid\")\n\tassert(_sprite_frames"
    )
    # Tambah SFX klik kartu
    masjid = masjid.replace(
        "\t_lbl_nama.text = data[\"arab\"] + \"  —  \" + data[\"nama\"]",
        "\tAudioManager.play_sfx(\"click\")\n\t_lbl_nama.text = data[\"arab\"] + \"  —  \" + data[\"nama\"]"
    )
    # Tambah SFX bintang
    masjid = masjid.replace(
        "func _show_selesai() -> void:\n\tGameManager.add_star(3)",
        "func _show_selesai() -> void:\n\tAudioManager.play_sfx(\"star\")\n\tGameManager.add_star(3)"
    )
    with open(masjid_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(masjid)
    print("  ✅  MasjidScene.gd — SFX ditambahkan")

# ── 8. Update TamanScene — SFX benar/salah ───────────────────
taman_path = os.path.join(BASE, "scripts", "locations", "TamanScene.gd")
with open(taman_path, "r", encoding="utf-8") as f:
    taman = f.read()

if "AudioManager" not in taman:
    taman = taman.replace(
        "\tif is_benar:\n\t\t_benar_warna += 1\n\t\t_lbl_feedback_w.text = \"✅  Betul! Hebat Maryam!\"",
        "\tif is_benar:\n\t\tAudioManager.play_sfx(\"correct\")\n\t\t_benar_warna += 1\n\t\t_lbl_feedback_w.text = \"✅  Betul! Hebat Maryam!\""
    )
    taman = taman.replace(
        "\telse:\n\t\t_lbl_feedback_w.text = \"❌  Coba lagi ya!\"",
        "\telse:\n\t\tAudioManager.play_sfx(\"wrong\")\n\t\t_lbl_feedback_w.text = \"❌  Coba lagi ya!\""
    )
    taman = taman.replace(
        "func _selesai(mode: String) -> void:\n\tGameManager.add_star(3)",
        "func _selesai(mode: String) -> void:\n\tAudioManager.play_sfx(\"star\")\n\tGameManager.add_star(3)"
    )
    with open(taman_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(taman)
    print("  ✅  TamanScene.gd — SFX ditambahkan")

# ── 9. Update PondokScene — SFX klik & star ──────────────────
pondok_path = os.path.join(BASE, "scripts", "locations", "PondokScene.gd")
with open(pondok_path, "r", encoding="utf-8") as f:
    pondok = f.read()

if "AudioManager" not in pondok:
    pondok = pondok.replace(
        "\t_lbl_info.text = data[\"huruf\"] + \"  —  \" + data[\"emoji\"] + \"  \" + data[\"kata\"]",
        "\tAudioManager.play_sfx(\"click\")\n\t_lbl_info.text = data[\"huruf\"] + \"  —  \" + data[\"emoji\"] + \"  \" + data[\"kata\"]"
    )
    pondok = pondok.replace(
        "func _show_selesai() -> void:\n\tGameManager.add_star(3)",
        "func _show_selesai() -> void:\n\tAudioManager.play_sfx(\"star\")\n\tGameManager.add_star(3)"
    )
    with open(pondok_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(pondok)
    print("  ✅  PondokScene.gd — SFX ditambahkan")

# ── 10. Update KebunScene — SFX klik & star ──────────────────
kebun_path = os.path.join(BASE, "scripts", "locations", "KebunScene.gd")
with open(kebun_path, "r", encoding="utf-8") as f:
    kebun = f.read()

if "AudioManager" not in kebun:
    kebun = kebun.replace(
        "func _on_next() -> void:\n\tif _selesai:\n\t\treturn\n\t_idx += 1",
        "func _on_next() -> void:\n\tif _selesai:\n\t\treturn\n\tAudioManager.play_sfx(\"click\")\n\t_idx += 1"
    )
    kebun = kebun.replace(
        "func _selesai_semua() -> void:\n\tif _selesai:\n\t\treturn\n\t_selesai = true\n\tGameManager.add_star(3)",
        "func _selesai_semua() -> void:\n\tif _selesai:\n\t\treturn\n\t_selesai = true\n\tAudioManager.play_sfx(\"star\")\n\tGameManager.add_star(3)"
    )
    with open(kebun_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(kebun)
    print("  ✅  KebunScene.gd — SFX ditambahkan")

# ── 11. Git commit ────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "feat: audio system — musik latar procedural + SFX klik/benar/salah/bintang/lompat"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

# ── 12. Auto-delete ───────────────────────────────────────────
try:
    os.remove(SCRIPT_PATH)
    print("  ✅  Script dihapus otomatis")
except:
    pass

print("\n" + "=" * 52)
print("  SELESAI!")
print("  Godot → Reload → F5")
print("  🎵 Main Menu   → melodi tenang")
print("  🎵 World Map   → melodi petualangan")
print("  🎵 Masjid      → melodi Islami")
print("  🔊 Klik kartu  → suara klik")
print("  🔊 Jawaban ✅  → suara benar")
print("  🔊 Jawaban ❌  → suara salah")
print("  🔊 Bintang     → arpeggio naik")
print("  🔊 Lompat      → swoosh pendek")
print("=" * 52 + "\n")
