from transformers import pipeline
import nltk

# Download sentence tokenizer model (only needs to be done once)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.download('punkt')
    nltk.download('punkt_tab')
except nltk.downloader.DownloadError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

# Initialize pipelines once to avoid reloading models on every request
# Using a distilled model for better performance
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)


def analyze_sentiment(text: str):
    """Analyzes the overall sentiment of a given text."""
    return sentiment_analyzer(text)[0]

def analyze_sentiment_by_utterance(transcript_text: str):
    """Analyzes sentiment for each sentence (utterance) in the transcript."""
    sentences = nltk.sent_tokenize(transcript_text)
    # Analyze a subset for performance; analyzing thousands can be slow.
    # In a production system, you might process this offline.
    return [
        {
            "utterance": {"text": sentence},
            **sentiment_analyzer(sentence)[0]
        }
        for sentence in sentences[:50] # Limiting to first 50 utterances for speed
    ]

def extract_key_phrases(transcript_text: str):
    """Extracts key phrases (Named Entities) from the transcript."""
    # We use a Named Entity Recognition (NER) model to find organizations, people, etc.
    ner_results = ner_pipeline(transcript_text)
    
    # Filter for specific entities you consider "key phrases"
    key_phrases = [
        result['word'] for result in ner_results 
        if result['entity_group'] in ['ORG', 'PER', 'MISC']
    ]
    return list(set(key_phrases)) # Return unique phrases