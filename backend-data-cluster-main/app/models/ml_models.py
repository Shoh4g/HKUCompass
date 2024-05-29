import nltk
from .uba.model import UBA
from .sentiment_analysis.model import SentimentAnalysis
from .relevance_analysis.model import RelevanceAnalysis
from .spam_detection.model import SpamDetection
from .transcript_parser.parser import extract_transcript_info
from .recommendation_engine.model import RecommendationEngine 


class MLModels():
  def __init__(self, db) -> None:
    self.db = db
    self.setup()
    self.uba = UBA(db)
    self.spam = SpamDetection()
    self.sentiment = SentimentAnalysis()
    self.relevance = RelevanceAnalysis(self.sentiment)
    self.transcript_parser = extract_transcript_info
    self.recommendation_engine = RecommendationEngine(db)

  def setup(self):
    nltk.download('all')