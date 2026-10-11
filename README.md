# Emotion Detection Application

A web-based AI application that analyzes user feedback using the Watson NLP Emotion Predict library and Flask to detect emotions (anger, disgust, fear, joy, and sadness) and identify the dominant emotion.

## Project Details
- **Project Name**: Emotion Detection System
- **Course**: Developing AI Applications with Python and Flask
- **Frameworks & Libraries**: Python 3, Flask, Watson NLP Embeddable AI Library, Requests
- **Repository**: oaqjp-final-project-emb-ai

## Application Structure
- `EmotionDetection/`: Package containing the emotion detection logic.
  - `emotion_detection.py`: Core function interacting with the Watson NLP Emotion Predict API.
  - `__init__.py`: Package initialization exposing `emotion_detector`.
- `server.py`: Flask web server routing requests and rendering the web application.
- `static/mywebscript.js`: Client-side JavaScript handling user interactions and API calls.
- `templates/index.html`: Web interface for emotion analysis.
- `test_emotion_detection.py`: Unit test suite testing statements across all target emotions.

## Author
OminduD
