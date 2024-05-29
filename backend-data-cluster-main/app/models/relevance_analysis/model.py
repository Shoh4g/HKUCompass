from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import spacy, json
from ..sentiment_analysis.model import SentimentAnalysis

class RelevanceAnalysis():
  def __init__(self, sentiment : SentimentAnalysis) -> None:
    # Initialization with a sentiment analysis model and loading BERT and spaCy models
    self.sentiment = sentiment
    self.model_name = "bert-base-uncased"
    self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
    self.model = BertModel.from_pretrained(self.model_name)
    self.nlp = spacy.load("en_core_web_sm")

  def polarity_scores_roberta(self, text):
    # Get sentiment scores using the sentiment analysis model
    scores_dict = self.sentiment.get_sentiment_scores(text)
    total = scores_dict['roberta_neg'] + scores_dict['roberta_pos']
    return total
  
  def calculate_similarity(self, text1 : str, text2 : str):
      # Calculate the cosine similarity between two texts using BERT embeddings
      maxlength = max(len(text1.split()), len(text2.split()))
      input_ids1 = self.tokenizer.encode(text1, add_special_tokens=True, max_length=maxlength, truncation=True,
                                    padding='max_length')
      input_ids2 = self.tokenizer.encode(text2, add_special_tokens=True, max_length=maxlength, truncation=True,
                                    padding='max_length')
      input_ids1 = torch.tensor(input_ids1).unsqueeze(0)
      input_ids2 = torch.tensor(input_ids2).unsqueeze(0)
      with torch.no_grad():
          outputs1 = self.model(input_ids1)
          embeddings1 = outputs1.last_hidden_state
          outputs2 = self.model(input_ids2)
          embeddings2 = outputs2.last_hidden_state
      embeddings1 = embeddings1[0].numpy()
      embeddings2 = embeddings2[0].numpy()
      similarity = cosine_similarity(embeddings1, embeddings2)
      return similarity[0][0]

  def count_action_verbs(self, text):
    action_verbs = ["Prepare", "Plan", "Organize", "Attend", "Engage", "Review", "Practice", "Seek", "Network", "Adapt",
                    "Balance", "Stay Motivated", "Reflect", "Utilize", "Manage", "Take Notes", "Stay Informed",
                    "Achieve", "Learn", "Understand",
                    "Analyze", "Discuss", "Participate", "Collaborate", "Research", "Experiment", "Adapt", "Focus",
                    "Prioritize",
                    "Problem-solve", "Communicate", "Listen", "Support", "Guide", "Clarify", "Simplify",
                    "Demonstrate", "Encourage", "Coach",
                    "Motivate", "Inspire", "Challenge", "Evaluate", "Monitor", "Assess", "Evaluate", "Revise",
                    "Improve", "Master", "Apply",
                    "Share", "Exchange", "Connect", "Relate", "Collaborate", "Integrate", "Assist", "Serve",
                    "Offer", "Recommend", "Suggest",
                    "Advise", "Mentor", "Guide", "Help", "Empower", "Assist", "Familiarize", "Inform", "Direct",
                    "Influence", "Lead", "Inspire",
                    "Encourage", "Promote", "Facilitate", "Foster", "Advocate", "Support", "Nurture", "Empathize",
                    "Inspire", "Motivate",
                    "Resolve", "Tackle", "Overcome", "Face", "Conquer", "Manage", "Maintain", "Handle", "Address",
                    "Cope", "Adapt", "Flourish",
                    "Thrive", "Excel", "Achieve", "Succeed", "Triumph"]
    doc = self.nlp(text)
    verbs_in_text = [token.text for token in doc if token.text in action_verbs]
    return len(verbs_in_text)

  def calculate_text_ratio(self, text1, text2):
    return len(text2) / len(text1)

  def calculate_relevance_score(self, description, text):
    # Compute a relevance score combining similarity, action verb count, text ratio, and sentiment
    return self.calculate_similarity(description, text) + self.count_action_verbs(text) + self.calculate_text_ratio(description, text) + self.polarity_scores_roberta(text)
  
  def sort_texts_on_relevance(self, description, texts):
    # Sort a list of texts by their relevance score in descending order
    relevance_scores = {}
    for t in texts:
      text = t['COMMENT']
      score = self.calculate_relevance_score(description, text)
      relevance_scores[json.dumps(t)] = score
    relevance_scores = dict(sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True))
    sorted_list = []
    for key, value in relevance_scores.items():
      sorted_list.append(json.loads(key))
    sorted_list = sorted_list[::-1]
    return sorted_list