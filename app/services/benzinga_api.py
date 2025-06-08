import requests
from flask import current_app

def get_transcript_by_call_id(call_id: str):
    """
    Fetches a specific transcript from the Benzinga API using a call_id.
    
    Args:
        call_id: The unique identifier for the earnings call.
        
    Returns:
        A dictionary containing the transcript data or None if an error occurs.
    """
    api_key = current_app.config['BENZINGA_API_KEY']
    url = f"{current_app.config['BENZINGA_API_URL']}/{call_id}?token={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors, e.g., 404 Not Found for invalid call_id
        if response.status_code == 404:
            return {"error": "Invalid call_id provided.", "status": 404}
        current_app.logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        current_app.logger.error(f"Request error occurred: {req_err}")
        
    return None # Return None for other errors