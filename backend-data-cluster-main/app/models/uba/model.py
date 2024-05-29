import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

class UBA():
  def __init__(self, db) -> None:
    # Initialize with a database connection to access other courses data
    self.db = db

  def give_recommendations(self, course_code, number):
    # Retrieve the specific course using its code from the database
    course = self.db.find_one('courses', {"COURSE_CODE" : course_code})
    # Create a unique title for the course combining its code and title
    title = course["COURSE_CODE"] + "_" + course['COURSE_TITLE']
    # Retrieve all courses from the database
    courses = self.db.find_all('courses')
    courses = [course for course in courses if "COMP" in course["COURSE_CODE"]]
    overviews = [course['COURSE_DESCRIPTION'] for course in courses]

    # Initialize a TF-IDF Vectorizer
    tfv = TfidfVectorizer(min_df=3, max_features=None,
                          strip_accents='unicode', analyzer='word',
                          token_pattern=r'\w{1,}',
                          ngram_range=(1, 3),
                          stop_words='english')
    # Transform the course descriptions into a TF-IDF matrix
    tfv_matrix = tfv.fit_transform(overviews)
    # Compute the sigmoid kernel to measure similarity between courses
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
    # Create a map of course titles to their indices in the TF-IDF matrix
    indices = {course["COURSE_CODE"] + "_" + course['COURSE_TITLE'] : idx for idx, course in enumerate(courses)}
    idx = indices[title]
    # Get the list of similarity scores for the specific course with all other courses
    sig_scores = list(enumerate(sig[idx]))
    # Sort the courses based on similarity scores in descending order
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    # Exclude the first score since it's the course itself, and get the number of requested recommendations
    sig_scores = sig_scores[1:number + 1] if number < len(sig_scores) else sig_scores  # Exclude the input course itself
    # Get indices of the recommended courses
    course_indices = [i[0] for i in sig_scores]
    # Retrieve the recommended courses based on the indices
    recommended_courses = [courses[i] for i in course_indices]
    return recommended_courses


