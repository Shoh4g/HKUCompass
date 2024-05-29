from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.special import softmax
import ssl

class SentimentAnalysis():
    def __init__(self) -> None:
        # Initialize the SentimentAnalysis class and load the model and tokenizer
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        self.load_model_and_tokenizer()

    def load_model_and_tokenizer(self):
        # Setup SSL context to avoid certificate verification issues during model loading
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            # If the environment doesn't support _create_unverified_context, do nothing
            pass
        else:
            # Apply the unverified context for HTTPS requests globally
            ssl._create_default_https_context = _create_unverified_https_context

        # Load the tokenizer and model from the Hugging Face Hub
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

    def get_sentiment_scores(self, text):
        # Tokenize the input text and perform sentiment analysis using the loaded model
        encoded_text = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_text)
        # Extract and detach the logits from the model's output
        scores = output[0][0].detach().numpy()
        # Apply softmax to the logits to get probabilities
        scores = softmax(scores)
        # Map the probabilities to sentiment labels
        scores_dict = {
            'roberta_neg': scores[0],
            'roberta_neu': scores[1],
            'roberta_pos': scores[2]
        }
        return scores_dict