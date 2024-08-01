import numpy as np
import soundfile as sf

# Fonction pour générer un son d'applaudissements
def generate_applause(duration, sample_rate):
    applause = np.random.uniform(-1, 1, int(sample_rate * duration))
    envelope = np.linspace(0, 1, int(sample_rate * 0.2))
    envelope = np.concatenate((envelope, np.ones(len(applause) - 2 * len(envelope)), envelope[::-1]))
    applause *= envelope
    applause *= np.random.rand(len(applause))  # variation d'amplitude pour rendre plus naturel
    return applause

# Fonction pour générer un son d'acclamation
def generate_acclamation(phrases, sample_rate, duration_per_phrase):
    acclamation = np.zeros(int(sample_rate * duration_per_phrase * len(phrases)))
    for i, phrase in enumerate(phrases):
        t = np.linspace(0, duration_per_phrase, int(sample_rate * duration_per_phrase), endpoint=False)
        if phrase == "Yeah":
            freq = 200 + np.sin(2 * np.pi * t) * 20
            acclamation[int(i * len(t)):int((i + 1) * len(t))] = np.sin(2 * np.pi * freq * t)
        elif phrase == "Bravo":
            freq = 300 + np.sin(2 * np.pi * t) * 30
            acclamation[int(i * len(t)):int((i + 1) * len(t))] = np.sin(2 * np.pi * freq * t)
    return acclamation

# Paramètres pour le son de réaction du public
sample_rate = 44100  # Taux d'échantillonnage
duration_applause = 2.5  # Durée des applaudissements en secondes
duration_per_phrase = 0.5  # Durée pour chaque phrase d'acclamation
phrases = ["Yeah", "Bravo"]

# Génération des sons
applause = generate_applause(duration_applause, sample_rate)
acclamation = generate_acclamation(phrases, sample_rate, duration_per_phrase)

# Combinaison des sons d'applaudissements et d'acclamations
combined_length = max(len(applause), len(acclamation))
combined_sound = np.zeros(combined_length)
combined_sound[:len(applause)] += applause
combined_sound[:len(acclamation)] += acclamation

# Sauvegarde du son dans un fichier
file_path_reaction = './public_reaction_point_v2.wav'
sf.write(file_path_reaction, combined_sound, sample_rate)

file_path_reaction
