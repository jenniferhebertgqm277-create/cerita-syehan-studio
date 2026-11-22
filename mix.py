#!/usr/bin/env python3
"""
mix.py: Automated Audio Mixer for Cerita Syehan Episode 0
Combines AI Voiceover + Curated Viral Meme Sound Effects + Lo-fi Background Music
Output: out/mix.wav
"""
import subprocess
import os

def mix_audio():
    os.makedirs("out", exist_ok=True)
    
    # SFX cue timing (in milliseconds) based on word-level subtitle alignment:
    # 0.10s -> Vine Boom (Hook impact)
    # 12.0s -> Windows Error ("masalah absurd")
    # 14.2s -> Bruh sound ("rada gaje")
    # 17.5s -> Ding Idea ("inovasi gila")
    # 19.8s -> Huh Meme Cat ("tetangga curiga")
    # 23.5s -> Airhorn Drop ("follow sekarang")
    # 25.2s -> Metal Pipe Bonk (Punchline impact)
    
    cmd = [
        "ffmpeg", "-y",
        "-i", "assets/voice.mp3",
        "-i", "assets/bgm.wav",
        "-i", "assets/sfx/vine-boom.mp3",
        "-i", "assets/sfx/windows-error.mp3",
        "-i", "assets/sfx/bruh.mp3",
        "-i", "assets/sfx/ding.mp3",
        "-i", "assets/sfx/huh.mp3",
        "-i", "assets/sfx/airhorn.mp3",
        "-i", "assets/sfx/metal-pipe.mp3",
        "-filter_complex",
        "[1]volume=0.20[bgm]; "
        "[2]adelay=100|100,volume=0.85[s1]; "
        "[3]adelay=12000|12000,volume=0.65[s2]; "
        "[4]adelay=14200|14200,volume=0.85[s3]; "
        "[5]adelay=17500|17500,volume=0.75[s4]; "
        "[6]adelay=19800|19800,volume=0.75[s5]; "
        "[7]adelay=23500|23500,volume=0.70[s6]; "
        "[8]adelay=25200|25200,volume=0.65[s7]; "
        "[0][bgm][s1][s2][s3][s4][s5][s6][s7]amix=inputs=9:duration=first:dropout_transition=2[outa]",
        "-map", "[outa]",
        "-ar", "44100",
        "out/mix.wav"
    ]
    
    print("Menggabungkan Voiceover, Background Music, dan Meme Sound Effects...")
    subprocess.run(cmd, check=True)
    print("Audio mix berhasil dibuat di out/mix.wav!")

if __name__ == "__main__":
    mix_audio()
