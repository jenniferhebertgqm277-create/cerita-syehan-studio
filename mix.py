#!/usr/bin/env python3
"""
mix.py: Automated High-Precision Audio Mixer for Cerita Syehan Episode 0 (ElevenLabs Edition)
Duration: 72.36 seconds
Mixes ElevenLabs voiceover + 8 viral meme sound effects + 73s Lo-fi BGM track
"""
import subprocess
import os

def mix_audio():
    os.makedirs("out", exist_ok=True)
    
    # Copy uploaded ElevenLabs voiceover to assets/voice.mp3 if needed
    if os.path.exists("voice/voice.mp3"):
        import shutil
        shutil.copy("voice/voice.mp3", "assets/voice.mp3")
    
    # SFX cue timing (in milliseconds) based on Whisper transcription:
    # 1.8s   -> Vine Boom ("STOP!")
    # 6.0s   -> Ding ("Animasi 3D 100% kode")
    # 17.2s  -> Soft Ding ("Kenalin gue Syehan")
    # 28.3s  -> Bruh ("Agak gak normal")
    # 34.0s  -> Ding Idea ("Robot nyiram tanaman")
    # 40.0s  -> Huh Cat ("Jam 2 pagi")
    # 45.0s  -> Windows Error ("Nge-debug kode")
    # 57.5s  -> Metal Pipe Bonk ("Kadang meledak!")
    # 67.8s  -> Airhorn Drop ("Follow sekarang!")
    # 70.8s  -> Oof / Impact ("Gas kita mulai!")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", "assets/voice.mp3",
        "-i", "assets/bgm.wav",
        "-i", "assets/sfx/vine-boom.mp3",
        "-i", "assets/sfx/ding.mp3",
        "-i", "assets/sfx/bruh.mp3",
        "-i", "assets/sfx/huh.mp3",
        "-i", "assets/sfx/windows-error.mp3",
        "-i", "assets/sfx/metal-pipe.mp3",
        "-i", "assets/sfx/airhorn.mp3",
        "-i", "assets/sfx/oof.mp3",
        "-filter_complex",
        "[1]volume=0.18[bgm]; "
        "[2]adelay=1800|1800,volume=0.85[s1]; "
        "[3]adelay=6000|6000,volume=0.60[s2]; "
        "[4]adelay=28300|28300,volume=0.90[s3]; "
        "[5]adelay=40000|40000,volume=0.75[s4]; "
        "[6]adelay=45000|45000,volume=0.70[s5]; "
        "[7]adelay=57500|57500,volume=0.80[s6]; "
        "[8]adelay=67800|67800,volume=0.75[s7]; "
        "[9]adelay=70800|70800,volume=0.75[s8]; "
        "[0][bgm][s1][s2][s3][s4][s5][s6][s7][s8]amix=inputs=10:duration=first:dropout_transition=2[outa]",
        "-map", "[outa]",
        "-ar", "44100",
        "out/mix.wav"
    ]
    
    print("Mixing ElevenLabs voiceover, background music, and meme SFX...")
    subprocess.run(cmd, check=True)
    print("Audio mix created successfully at out/mix.wav!")

if __name__ == "__main__":
    mix_audio()
