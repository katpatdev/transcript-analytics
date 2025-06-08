# import time
# from flask import Blueprint, request, jsonify
# from app.services import benzinga_api, nlp_advanced # Import the new advanced NLP service

# # Create a new Blueprint for the advanced analytics endpoint
# analytics_advanced_bp = Blueprint('analytics_advanced', __name__)

# @analytics_advanced_bp.route('/analytics_advanced', methods=['GET'])
# def get_advanced_analytics():
#     """
#     Endpoint to fetch and perform ADVANCED analysis on a transcript.
#     """
#     start_time = time.time()
#     call_id = request.args.get('call_id')

#     if not call_id:
#         return jsonify({"error": "call_id parameter is required"}), 400

#     transcript_data = benzinga_api.get_transcript_by_call_id(call_id)
    
#     if not transcript_data or transcript_data.get("error"):
#          return jsonify({"error": "Failed to fetch or invalid transcript data"}), 404

#     # Safely extract the transcript text from the nested structure
#     transcript_text = ""
#     transcripts_list = transcript_data.get('transcripts', [])
#     if transcripts_list and isinstance(transcripts_list, list) and len(transcripts_list) > 0:
#         transcript_text = transcripts_list[0].get('text', '')

#     if not transcript_text:
#         return jsonify({"error": "Could not find transcript text in the API response."}), 404

#     # --- Use the new advanced NLP functions ---
#     # We can get a better overall sentiment by chunking the text
#     # Here, we'll just use the first 512 tokens for a quick overall score with FinBERT
#     overall_sentiment = nlp_advanced.sentiment_analyzer(transcript_text[:512])[0]
#     sentiment_by_utterance = nlp_advanced.analyze_sentiment_by_utterance(transcript_text)
#     key_phrases = nlp_advanced.extract_detailed_key_phrases(transcript_text)
    
#     end_time = time.time()
#     processing_time_ms = int((end_time - start_time) * 1000)

#     # Return a new structured JSON response
#     response = {
#         "call_id": call_id,
#         "company": transcript_data.get("symbol", "N/A"),
#         "date": transcript_data.get("start_time", "N/A").split("T")[0],
#         "advanced_analytics": {
#             "overall_sentiment": {
#                 "score": round(overall_sentiment['score'], 4),
#                 "label": overall_sentiment['label']
#             },
#             "sentiment_by_utterance": sentiment_by_utterance,
#             "detailed_key_phrases": key_phrases[:50], # Limiting for readability
#             "word_count": len(transcript_text.split()),
#             "processing_time_ms": processing_time_ms
#         }
#     }

#     return jsonify(response)
import time
from flask import Blueprint, request, jsonify
from app.services import benzinga_api, nlp_advanced # Import the advanced NLP service

# Create a new Blueprint for the advanced analytics endpoint
analytics_advanced_bp = Blueprint('analytics_advanced', __name__)

@analytics_advanced_bp.route('/analytics_advanced', methods=['GET'])
def get_advanced_analytics():
    """
    Endpoint to fetch and perform ADVANCED analysis on a transcript.
    """
    start_time = time.time()
    call_id = request.args.get('call_id')

    if not call_id:
        return jsonify({"error": "call_id parameter is required"}), 400

    transcript_data = benzinga_api.get_transcript_by_call_id(call_id)
    
    if not transcript_data or transcript_data.get("error"):
         return jsonify({"error": "Failed to fetch or invalid transcript data"}), 404

    # Safely extract the transcript text from the nested structure
    transcript_text = ""
    transcripts_list = transcript_data.get('transcripts', [])
    if transcripts_list and isinstance(transcripts_list, list) and len(transcripts_list) > 0:
        transcript_text = transcripts_list[0].get('text', '')

    if not transcript_text:
        return jsonify({"error": "Could not find transcript text in the API response."}), 404

    # --- Use the new and updated advanced NLP functions ---
    
    # 1. Get a more accurate overall sentiment by analyzing a much larger initial part of the text.
    # We'll tokenize the text and take the first ~3000 tokens (approx 4000 chars)
    # Note: FinBERT's limit is still 512, but analyzing a larger coherent text provides a better sample.
    initial_long_chunk = transcript_text[:4000]
    overall_sentiment = nlp_advanced.sentiment_analyzer(initial_long_chunk[:512])[0]
    
    # 2. Analyze sentiment by large chunks (defaulting to 2500 tokens each)
    sentiment_by_chunk = nlp_advanced.analyze_sentiment_by_chunk(transcript_text)
    
    # 3. Extract and filter key phrases from the entire text
    key_phrases = nlp_advanced.extract_detailed_key_phrases(transcript_text)
    
    end_time = time.time()
    processing_time_ms = int((end_time - start_time) * 1000)

    # Return a new structured JSON response
    response = {
        "call_id": call_id,
        "company": transcript_data.get("symbol", "N/A"),
        "date": transcript_data.get("start_time", "N/A").split("T")[0],
        "advanced_analytics": {
            "overall_sentiment_on_intro": { # Renamed for clarity
                "score": round(overall_sentiment['score'], 4),
                "label": overall_sentiment['label']
            },
            "sentiment_by_chunk": sentiment_by_chunk,
            "filtered_key_phrases": key_phrases,
            "word_count": len(transcript_text.split()),
            "processing_time_ms": processing_time_ms
        }
    }

    return jsonify(response)