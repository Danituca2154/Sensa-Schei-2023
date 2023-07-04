import RPi.GPIO as GPIO
import time

# Imposta il pin GPIO a cui è collegato il buzzer
buzzer_pin = 6

# Inizializza il GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Funzione per suonare una nota
def play_tone(frequency, duration):
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

# Frequenze delle note
E4 = 329.63
C4 = 261.63
G3 = 196.00
E3 = 164.81
G4 = 392.00
A4 = 440.00
F4 = 349.23
D4 = 293.66
B3 = 246.94

# Suoni per riprodurre il suono "Game Over" di Super Mario
notes = [E4, C4, G3, E3, G3, C4, E4, G4, A4, F4, G4, E4, C4, D4, B3]
durations = [0.15, 0.15, 0.3, 0.3, 0.3, 0.3, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.3]

# Riproduci il suono "Game Over" di Super Mario nota per nota
for i in range(len(notes)):
    frequency = notes[i]
    duration = durations[i]
    play_tone(frequency, duration)

# Pulisci il GPIO alla fine
GPIO.cleanup()
