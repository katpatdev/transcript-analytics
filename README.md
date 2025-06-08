# Financial Transcript Analytics Service

## 1. Project Overview

This service provides analytical insights into financial earnings call transcripts.It exposes a Flask-based REST API that fetches a specific transcript from the Benzinga API using a `call_id`, processes its content using various Hugging Face NLP models, and returns a structured JSON response with sentiment analysis and key phrase extraction. 

The project includes two primary endpoints:
* A **standard endpoint** (`/analytics`) for fast, general-purpose analysis.
* An **advanced endpoint** (`/analytics_advanced`) that uses more powerful, specialized models for deeper and more context-aware financial insights.

The entire application is containerized with Docker for easy setup, portability, and deployment. 

## 2. Features

* **Benzinga API Integration**: Fetches earnings call transcript data by `call_id`. 
* **Dual Analytics Endpoints**: Offers both standard and advanced analytics options.
* **Overall Sentiment Analysis**: Provides a top-level sentiment score (Positive/Negative/Neutral) for the transcript.
* **Granular Sentiment Analysis**: Breaks down the transcript into sentences or larger contextual chunks and analyzes the sentiment of each part. 
* **Key Phrase Extraction**: Uses Named Entity Recognition (NER) to identify important entities like companies, people, products, and dates. 
* **Containerized Environment**: Includes a `Dockerfile` for building a self-contained image, ensuring the environment is consistent and easy to run anywhere. 
* **Robust Testing**: Comes with a suite of unit tests using `pytest` to verify error handling and application logic.

## 3. Technologies Used

* **Language**: Python 
* **Framework**: Flask 
* **NLP**: Hugging Face Transformers, NLTK
* **API Interaction**: Requests
* **Containerization**: Docker 
* **Testing**: Pytest, Pytest-Mock

## 4. Final Project Structure

```
transcript-analytics/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   └── analytics_advanced.py
│   └── services/
│       ├── __init__.py
│       ├── benzinga_api.py
│       ├── nlp.py
│       └── nlp_advanced.py
├── tests/
│   ├── __init__.py
│   └── test_analytics.py
├── .env
├── .gitignore
├── config.py
├── Dockerfile
├── requirements.txt
├── README.md
├── pytest.ini
├── pyproject.toml
└── run.py
```

## 5. Setup and Execution

### Prerequisites

* Python 3.9+
* Docker
* Git

### Method 1: Local Development Setup

This method is recommended for developers who want to work with the source code directly.

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd transcript-analytics
    ```

2.  **Create an Environment File**
    Create a file named `.env` in the project root and add your Benzinga API key:
    ```
    BENZINGA_API_KEY=<your_benzinga API key>
    ```

3.  **Create and Activate a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Dependencies**
    Install all required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Install Project in Editable Mode**
    This crucial step makes your application code importable by the rest of the environment.
    ```bash
    pip install -e .
    ```

6.  **Run the Application**
    ```bash
    python run.py
    ```
    The service will now be running on `http://127.0.0.1:5000`.

### Method 2: Docker Setup

This method is recommended for quickly running the application in a stable, isolated environment without setting up Python or dependencies locally.

1.  **Build the Docker Image**
    From the project's root directory, run:
    ```bash
    docker build -t transcript-analytics .
    ```

2.  **Run the Docker Container**
    Run the image and pass the API key as an environment variable.
    ```bash
    docker run -p 5000:5000 -e BENZINGA_API_KEY="<your_benzinga API key>" --name analytics-service transcript-analytics
    ```
    The service will now be running on `http://localhost:5000`.

## 6. API Usage

The service provides two `GET` endpoints to perform analysis.

### Endpoint 1: Standard Analytics

This endpoint provides fast, general-purpose analysis using `DistilBERT`. It is ideal for quick sentiment checks.

* **URL**: `/analytics`
* **Method**: `GET`
* **Query Parameter**: `call_id={your_call_id}`
* **Example Request**:
    ```bash
    curl "http://localhost:5000/analytics?call_id=6784d5deaae66a00015735a6"
    ```

---

### Endpoint 2: Advanced Analytics

This endpoint uses larger, more specialized models (`FinBERT` for sentiment, `RoBERTa` for NER) to provide more accurate and detailed insights. It analyzes larger chunks of text for better contextual understanding.

* **URL**: `/analytics_advanced`
* **Method**: `GET`
* **Query Parameter**: `call_id={your_call_id}`
* **Example Request**:
    ```bash
    curl "http://localhost:5000/analytics_advanced?call_id=6784d5deaae66a00015735a6"
    ```

## 7. Testing

The project includes a suite of unit tests to verify error-handling logic in an isolated environment.

1.  **Ensure Development Dependencies are Installed**
    Make sure you have followed the local setup and that `pytest` and `pytest-mock` are installed.

2.  **Run the Tests**
    From the project root, simply run:
    ```bash
    pytest
    ```
    A successful run will show **`4 passed`**.
