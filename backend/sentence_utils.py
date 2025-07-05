import pandas as pd
import os
import json

SENTENCE_FILE = 'backend/sentences.xlsx'

def get_next_sentence(participant_id):
    df = pd.read_excel(SENTENCE_FILE)
    sentences = df['Sentence'].tolist()

    log_path = f'backend/logs/{participant_id}.json'
    os.makedirs('backend/logs', exist_ok=True)
    recorded = []
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            recorded = json.load(f)

    for idx, sentence in enumerate(sentences):
        if idx not in recorded:
            return sentence, idx

    return None, None

def log_sentence(participant_id, sentence_idx):
    log_path = f'backend/logs/{participant_id}.json'
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            recorded = json.load(f)
    else:
        recorded = []

    recorded.append(sentence_idx)
    with open(log_path, 'w') as f:
        json.dump(recorded, f)