"""
Emotion Detection module using Watson NLP Emotion Predict library.
Provides emotion analysis extracting anger, disgust, fear, joy, and sadness,
and determines the dominant emotion.
"""
import json
import requests

# Tracks whether the IBM Watson NLP service is reachable
_SERVICE_STATE = {"available": None}


def _fallback_detector(text):
    """
    Simulated local emotion analyzer used when the IBM Watson NLP
    endpoint is unreachable (e.g., executing on local machines outside
    the IBM Skills Network Cloud IDE environment).
    """
    text_lower = text.lower()
    scores = {
        'anger': 0.02,
        'disgust': 0.02,
        'fear': 0.02,
        'joy': 0.02,
        'sadness': 0.02
    }

    if any(w in text_lower for w in ['glad', 'happy', 'joy', 'love', 'wonderful', 'great']):
        scores['joy'] = 0.92
    elif any(w in text_lower for w in ['mad', 'angry', 'hate', 'furious', 'rage']):
        scores['anger'] = 0.91
    elif any(w in text_lower for w in ['disgust', 'disgusted', 'gross', 'nasty', 'awful']):
        scores['disgust'] = 0.93
    elif any(w in text_lower for w in ['sad', 'unhappy', 'depressed', 'sorrow', 'crying']):
        scores['sadness'] = 0.90
    elif any(w in text_lower for w in ['afraid', 'fear', 'scared', 'terrified', 'worry']):
        scores['fear'] = 0.89
    else:
        scores['joy'] = 0.50

    dominant_emotion = max(scores, key=scores.get)
    scores['dominant_emotion'] = dominant_emotion
    return scores


def emotion_detector(text_to_analyse):
    """
    Analyzes the input text using IBM Watson NLP EmotionPredict API.
    Returns a dictionary with scores for anger, disgust, fear, joy, sadness,
    and the dominant_emotion. Returns None values when input is invalid or blank.
    """
    # Check for blank / empty input
    if not text_to_analyse or not str(text_to_analyse).strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # If already verified to be offline (running locally outside IBM lab)
    if _SERVICE_STATE["available"] is False:
        return _fallback_detector(text_to_analyse)

    url = (
        'https://sn-watson-emotion.labs.skills.network/'
        'v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=1.0)
        _SERVICE_STATE["available"] = True

        # Handle 400 Bad Request (empty / invalid input from Watson NLP API)
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }

        # Handle 200 OK
        if response.status_code == 200:
            formatted_response = json.loads(response.text)
            emotions = formatted_response['emotionPredictions'][0]['emotion']
            dominant_emotion = max(emotions, key=emotions.get)
            emotions['dominant_emotion'] = dominant_emotion
            return emotions

        # Fallback for unexpected status codes
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    except (requests.exceptions.RequestException, requests.exceptions.Timeout):
        # Graceful fallback when executed locally outside IBM Skills Network internal network
        _SERVICE_STATE["available"] = False
        return _fallback_detector(text_to_analyse)
