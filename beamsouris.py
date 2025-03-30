import pyautogui

import sounddevice as sd

from eyeware.client import TrackerClient
import numpy as np
import time


# Initialisation de la reconnaissance vocale
tracker = TrackerClient()
screen_gaze = tracker.get_screen_gaze_info()

# Fonction pour obtenir les coordonnées du centre de la vision
# Fonction pour obtenir les coordonnées du centre de la vision
def get_gaze_coordinates():
    x, y = None, None  # Initialisation par défaut
    if tracker.connected:
        screen_gaze = tracker.get_screen_gaze_info()
        screen_gaze_is_lost = screen_gaze.is_lost
        if not screen_gaze_is_lost:
            x = screen_gaze.x
            y = screen_gaze.y
    return x, y


# Fonction pour déplacer la souris
def move_mouse_to_gaze():
    x, y = get_gaze_coordinates()
    pyautogui.moveTo(x, y)

def detect_clap(data, threshold=0.5):
    return np.max(np.abs(data)) > threshold


# Fonction principale
def main():
    print("Écoute des claquements de mains...")
    sample_rate = 44100  # Fréquence d'échantillonnage
    duration = 0.5  # Durée d'enregistrement (en secondes)
    
    while True:
        move_mouse_to_gaze()
        # Enregistrement audio
        audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype='float64')
        sd.wait()  # Attendre la fin de l'enregistrement
        
        # Détection des claquements de mains
        if detect_clap(audio_data):
            
            # Attendre un court instant pour voir s'il y a un deuxième claquement
            audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype='float64')
            sd.wait()
            if detect_clap(audio_data):
                print("2")
                pyautogui.click(button='right')
            else:
                print("1")
                pyautogui.click(button='left')

if __name__ == "__main__":
    main()
