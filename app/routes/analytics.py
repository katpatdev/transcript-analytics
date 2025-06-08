import time
from flask import Blueprint, request, jsonify, current_app
from app.services import benzinga_api, nlp

# Create a Blueprint. This is a way to organize a group of related views and other code.
analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """
    Endpoint to fetch and analyze an earnings call transcript.
    Expects a 'call_id' query parameter.
    """
    start_time = time.time()
    call_id = request.args.get('call_id')

    # 1. Validate input
    if not call_id:
        return jsonify({"error": "call_id parameter is required"}), 400

    # 2. Fetch transcript from Benzinga
    transcript_data = benzinga_api.get_transcript_by_call_id(call_id)
    
    if not transcript_data:
        return jsonify({"error": "Failed to fetch transcript from Benzinga API."}), 502 # Bad Gateway
    
    if transcript_data.get("error"):
         return jsonify({"error": transcript_data.get("error")}), transcript_data.get("status")
    '''
    transcript_text = transcript_data.get('body', '')
    if not transcript_text:
        return jsonify({"error": "Transcript body is empty."}), 404
    '''
    transcript_text = ""
    transcripts_list = transcript_data.get('transcripts', [])
    if transcripts_list and isinstance(transcripts_list, list) and len(transcripts_list) > 0:
        transcript_text = transcripts_list[0].get('text', '')

    if not transcript_text:
        # This error message is now more accurate.
        return jsonify({"error": "Could not find transcript text in the API response."}), 404

    # 3. Process with Hugging Face models
    overall_sentiment = nlp.analyze_sentiment(transcript_text[:512]) # Analyze first 512 tokens for speed
    sentiment_by_utterance = nlp.analyze_sentiment_by_utterance(transcript_text)
    key_phrases = nlp.extract_key_phrases(transcript_text)
    word_count = len(transcript_text.split())

    end_time = time.time()
    processing_time_ms = int((end_time - start_time) * 1000)

    # 4. Return structured JSON response 
    response = {
        "call_id": call_id,
        "company": transcript_data.get("symbol", "N/A"),
        "date": transcript_data.get("start_time", "N/A").split("T")[0],
        "analytics": {
            "overall_sentiment": {
                "score": round(overall_sentiment['score'], 2),
                "label": overall_sentiment['label']
            },
            "sentiment_by_utterance": sentiment_by_utterance,
            "key_phrases": key_phrases[:10], 
            # Limit to top 10 phrases
            "word_count": word_count,
            "processing_time_ms": processing_time_ms
        }
    }

    return jsonify(response)