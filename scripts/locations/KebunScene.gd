# =============================================================
#  scripts/locations/KebunScene.gd
#  Kebun Karakter — Cerita nilai Islam untuk anak
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

const CERITA : Array[Dictionary] = [
	{
		"judul"  : "🌸 Berbagi Itu Indah",
		"cerita" : "Maryam punya 2 apel.\nTemannya tidak punya apel.\nMaryam memberi 1 apel kepada temannya.\n\nTemannya sangat senang! 😊",
		"nilai"  : "Berbagi membuat hati bahagia! 💝",
		"emoji"  : "🍎"
	},
	{
		"judul"  : "🙏 Selalu Berdoa",
		"cerita" : "Sebelum makan, Maryam selalu berdoa.\n\n'Bismillahirrahmanirrahim'\n\nAllah senang dengan anak yang berdoa. ✨",
		"nilai"  : "Ingat Allah di setiap kegiatan! 🌟",
		"emoji"  : "🤲"
	},
	{
		"judul"  : "😊 Jujur Itu Berani",
		"cerita" : "Maryam tidak sengaja memecahkan gelas.\nMaryam berani berkata jujur kepada Ayah.\n\nAyah bangga karena Maryam jujur! 💪",
		"nilai"  : "Jujur adalah sifat orang berani! 🦁",
		"emoji"  : "💎"
	},
	{
		"judul"  : "🤝 Tolong Menolong",
		"cerita" : "Teman Maryam membawa tas yang berat.\nMaryam membantu mengangkat tasnya.\n\nMereka berjalan bersama dengan gembira! 🌈",
		"nilai"  : "Membantu sesama adalah kebaikan! 💛",
		"emoji"  : "👫"
	},
	{
		"judul"  : "😌 Sabar Itu Kuat",
		"cerita" : "Maryam mengantri dengan tertib.\nWalaupun lama, Maryam tetap sabar.\n\nAllah suka dengan orang yang sabar! ⭐",
		"nilai"  : "Sabar adalah kekuatan sejati! 🌺",
		"emoji"  : "⏳"
	},
]

var _idx      : int  = 0
var _selesai  : bool = false

@onready var _lbl_judul     : Label  = $UI/CardCerita/LblJudul
@onready var _lbl_emoji     : Label  = $UI/CardCerita/LblEmoji
@onready var _lbl_cerita    : Label  = $UI/CardCerita/LblCerita
@onready var _lbl_nilai     : Label  = $UI/CardCerita/LblNilai
@onready var _btn_next      : Button = $UI/CardCerita/BtnNext
@onready var _lbl_progress  : Label  = $UI/TopBar/LblProgress
@onready var _btn_back      : Button = $UI/TopBar/BtnBack
@onready var _panel_selesai : Panel  = $UI/PanelSelesai
@onready var _btn_keluar    : Button = $UI/PanelSelesai/VBox/BtnKeluar


func _ready() -> void:
	_panel_selesai.visible = false
	_btn_back.pressed.connect(_on_back)
	_btn_keluar.pressed.connect(_on_back)
	_btn_next.pressed.connect(_on_next)
	_tampil_cerita()


func _tampil_cerita() -> void:
	if _idx >= CERITA.size():
		_selesai_semua()
		return
	var c : Dictionary = CERITA[_idx]
	_lbl_judul.text   = c["judul"]
	_lbl_emoji.text   = c["emoji"]
	_lbl_cerita.text  = c["cerita"]
	_lbl_nilai.text   = c["nilai"]
	_lbl_progress.text = str(_idx + 1) + " / " + str(CERITA.size())
	if _idx == CERITA.size() - 1:
		_btn_next.text = "✅  Selesai!"
	else:
		_btn_next.text = "Cerita Berikutnya →"


func _on_next() -> void:
	if _selesai:
		return
	AudioManager.play_sfx("click")
	_idx += 1
	_tampil_cerita()


func _selesai_semua() -> void:
	if _selesai:
		return
	_selesai = true
	AudioManager.play_sfx("star")
	GameManager.add_star(3)
	_panel_selesai.visible = true


func _on_back() -> void:
	TransitionManager.go_to(WORLD_SCENE)
