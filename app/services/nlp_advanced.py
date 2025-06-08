# from transformers import pipeline
# import nltk

# # Ensure the 'punkt' sentence tokenizer is available
# try:
#     nltk.data.find('tokenizers/punkt')
# except nltk.downloader.DownloadError:
#     nltk.download('punkt')

# # 1. Initialize the advanced, finance-specific sentiment analysis model
# # This model can handle longer inputs, but we'll still feed it sentences for granular analysis
# sentiment_analyzer = pipeline(
#     "sentiment-analysis", 
#     model="ProsusAI/finbert"
# )

# # 2. Initialize the advanced, larger NER model for more detailed key phrases
# ner_pipeline = pipeline(
#     "ner", 
#     model="Jean-Baptiste/roberta-large-ner-english", 
#     grouped_entities=True
# )

# def analyze_sentiment_by_utterance(transcript_text: str):
#     """Analyzes sentiment for each sentence using FinBERT."""
#     sentences = nltk.sent_tokenize(transcript_text)
#     # Analyze a subset for performance; analyzing thousands can be slow.
#     return [
#         {
#             "utterance": {"text": sentence},
#             **sentiment_analyzer(sentence)[0]
#         }
#         for sentence in sentences[:50] # Still limiting to 50 for speed
#     ]

# def extract_detailed_key_phrases(transcript_text: str):
#     """Extracts detailed key phrases (18 entity types) using a large RoBERTa model."""
#     ner_results = ner_pipeline(transcript_text)
    
#     key_phrases = [
#         {"text": result['word'], "type": result['entity_group']} 
#         for result in ner_results
#     ]
#     return key_phrases
from transformers import pipeline, AutoTokenizer
import nltk
import math

# Ensure the 'punkt' sentence tokenizer is available
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')

# --- MODEL INITIALIZATION (REMAINS THE SAME) ---
# 1. Initialize the advanced, finance-specific sentiment analysis model
sentiment_analyzer = pipeline(
    "sentiment-analysis", 
    model="ProsusAI/finbert"
)

# 2. Initialize the advanced, larger NER model for more detailed key phrases
ner_pipeline = pipeline(
    "ner", 
    model="Jean-Baptiste/roberta-large-ner-english", 
    grouped_entities=True
)

# We need the tokenizer for the NER model to accurately count tokens for chunking
ner_tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-ner-english")


# --- NEW FUNCTION: CHUNK TEXT BY TOKEN LIMIT ---
def chunk_text_by_tokens(text: str, model_tokenizer, chunk_size: int):
    """Splits text into chunks of a specified token size."""
    sentences = nltk.sent_tokenize(text)
    
    chunks = []
    current_chunk_sentences = []
    current_chunk_tokens = 0

    for sentence in sentences:
        sentence_token_count = len(model_tokenizer.tokenize(sentence))
        
        if current_chunk_tokens + sentence_token_count <= chunk_size:
            current_chunk_sentences.append(sentence)
            current_chunk_tokens += sentence_token_count
        else:
            # Add the current chunk to the list if it's not empty
            if current_chunk_sentences:
                chunks.append(" ".join(current_chunk_sentences))
            
            # Start a new chunk with the current sentence
            current_chunk_sentences = [sentence]
            current_chunk_tokens = sentence_token_count
            
    # Add the last remaining chunk
    if current_chunk_sentences:
        chunks.append(" ".join(current_chunk_sentences))
        
    return chunks


# --- UPDATED FUNCTION: analyze_sentiment_by_utterance ---
# It will now analyze by larger chunks instead of single sentences
def analyze_sentiment_by_chunk(transcript_text: str, chunk_token_size: int = 300):
    """Analyzes sentiment for each chunk of text up to a token limit."""
    
    # Use the NER tokenizer as a reference for chunking
    text_chunks = chunk_text_by_tokens(transcript_text, ner_tokenizer, chunk_token_size)
    
    analysis_results = []
    for i, chunk in enumerate(text_chunks):
        # The sentiment model has a smaller limit, so we truncate the chunk for it.
        # This gives a sentiment for a larger conceptual block.
        sentiment_result = sentiment_analyzer(chunk[:512])[0] 
        analysis_results.append({
            "chunk_number": i + 1,
            "text": chunk,
            "sentiment": sentiment_result
        })
    return analysis_results


# --- UPDATED FUNCTION: extract_detailed_key_phrases ---
# Added filtering to remove unwanted tokens
def extract_detailed_key_phrases(transcript_text: str):
    """Extracts and filters detailed key phrases using a large RoBERTa model."""
    ner_results = ner_pipeline(transcript_text)
    
    filtered_phrases = []
    # Define keywords/characters to ignore
    ignore_list = [".", ",", "-", ":"]
    
    for result in ner_results:
        # Check if the extracted word is in the ignore list or is a single non-alphanumeric character
        if result['word'].strip() not in ignore_list and result['word'].strip().isalnum():
            filtered_phrases.append(
                {"text": result['word'].strip(), "type": result['entity_group']}
            )
            
    return filtered_phrases