import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- TESTS FOR THE ORIGINAL /analytics ENDPOINT ---

def test_missing_call_id(client):
    """Test response when call_id is missing."""
    response = client.get('/analytics')
    assert response.status_code == 400
    assert b"call_id parameter is required" in response.data

def test_invalid_call_id(client, mocker):
    """Test response for an invalid call_id by mocking the API call."""
    # Mock the function that calls the external API
    mocker.patch(
        'app.services.benzinga_api.get_transcript_by_call_id', 
        return_value={"error": "Invalid call_id provided.", "status": 404}
    )
    
    response = client.get('/analytics?call_id=invalid123')
    assert response.status_code == 404
    assert b"Invalid call_id provided" in response.data

# --- NEW TESTS FOR THE /analytics_advanced ENDPOINT ---

def test_advanced_missing_call_id(client):
    """Test advanced endpoint when call_id is missing."""
    response = client.get('/analytics_advanced') # Target the new URL
    assert response.status_code == 400
    assert b"call_id parameter is required" in response.data

def test_advanced_invalid_call_id(client, mocker):
    """Test advanced endpoint for an invalid call_id."""
    # The mocked function is the same, as both endpoints share it
    mocker.patch(
        'app.services.benzinga_api.get_transcript_by_call_id', 
        return_value=None # Simulate a failure to fetch data
    )
    
    response = client.get('/analytics_advanced?call_id=invalid123') # Target the new URL
    assert response.status_code == 404
    assert b"Failed to fetch or invalid transcript data" in response.data