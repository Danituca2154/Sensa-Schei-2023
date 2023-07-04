import RPi.GPIO as GPIO
import time

# Imposta il pin GPIO a cui è collegato il buzzer
buzzer_pin = 6

# Definisci le note e le relative durate per la melodia di Super Mario
notes = ['E7', 'E7', '0', 'E7', '0', 'C7', 'E7', '0', 'G7', '0', '0', '0', 'G6', '0', '0', '0', 'C7', '0', '0', 'G6', '0', '0', 'E6', '0', '0', 'A6', '0', 'B6', '0', 'AS6', 'A6', '0', 'G6', 'E7', 'G7', 'A7', '0', 'F7', 'G7', '0', 'E7', '0', 'C7', 'D7', 'B6', '0', '0', 'C7', '0', '0', 'G6', '0', '0', 'E6', '0', '0', 'A6', '0', 'B6', '0', 'AS6', 'A6', '0', 'G6', 'E7', 'G7', 'A7', '0', 'F7', 'G7', '0', 'E7', '0', 'C7', 'D7', 'B6', '0', '0']
durations = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.24, 0.12, 0.12, 0.12, 0.24, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.24, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12]

# Inizializza il GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Funzione per suonare una nota
def play_tone(note, duration):
    if note == '0':
        # Pausa se la nota è '0'
        time.sleep(duration)
    else:
        # Calcola la frequenza corrispondente alla nota
        tones = {
            'C7': 2093,
            'B6': 1976,
            'AS6': 1865,
            'A6': 1760,
            'G7': 3136,
            'G6': 1568,
            'F7': 2794,
            'E7': 2637,
            'D7': 2349,
            'C6': 1047,
            'E6': 1319,
            'A7': 3520
        }
        frequency = tones[note]
        
        # Calcola il periodo corrispondente alla durata
        period = 1.0 / frequency
        
        # Calcola il numero di cicli per la durata specificata
        cycles = int(duration / (period * 2))
        
        # Suona la nota
        for _ in range(cycles):
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(period)
            GPIO.output(buzzer_pin, GPIO.LOW)
            time.sleep(period)

# Riproduci la melodia di Super Mario nota per nota
for i in range(len(notes)):
    note = notes[i]
    duration = durations[i]
    play_tone(note, duration)

# Pulisci il GPIO alla fine
GPIO.cleanup()
