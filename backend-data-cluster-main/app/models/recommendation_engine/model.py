import math, json

class RecommendationEngine():
  def __init__(self, db) -> None:
    # Initialize the engine with a database connection.
    self.db = db

  def load_course_data(self):
    # Retrieve all course data from the database
    courses = self.db.find_all('courses')
    return courses

  def find_closest_courses(self, preferences, n):
    courses = self.load_course_data()
    courses_data = {}
    # Normalize course attributes by the number of ratings
    for course in courses:
      courses_data[course["COURSE_CODE"] + "_" + course["COURSE_TITLE"]] = {
        "DIFFICULTY" : course["DIFFICULTY"] / course["RATING_COUNT"],
        "GRADING" : course["GRADING"] / course["RATING_COUNT"],
        "USEFULNESS" : course["USEFULNESS"] / course["RATING_COUNT"],
        "WORKLOAD" : course["WORKLOAD"] / course["RATING_COUNT"]
      }
    closest_courses = []
    # Compute Euclidean distance for each course based on preferences
    for course, scores in courses_data.items():
        distance = math.sqrt(sum((preferences[metric] - scores[metric]) ** 2 for metric in preferences))
        closest_courses.append((course, distance))
    # Sort courses by proximity to student preferences
    closest_courses.sort(key=lambda x: x[1])
    # Select top n courses closest to preferences
    selected_courses = [course[0] for course in closest_courses[:n]] if n <= len(closest_courses) - 1 else closest_courses
    selected_course_codes = [course.split("_")[0] for course in selected_courses]
    # Return the selected course details
    return_courses = [course for course in courses if course["COURSE_CODE"] in selected_course_codes]
    return return_courses

  def recommend_courses(self):
    # original_data = studyplan

    # Load student profile from a JSON file
    with open('studentProfile.json') as json_file:
        student_transcript = json.load(json_file)

    # Determine the current year and next year based on the transcript
    current_year = None
    if student_transcript.get("first_year") and not student_transcript.get("second_year"):
        current_year = "first_year"
        next_year = "second_year"
    elif student_transcript.get("second_year") and not student_transcript.get("third_year"):
        current_year = "second_year"
        next_year = "third_year"
    elif student_transcript.get("third_year") and not student_transcript.get("fourth_year"):
        current_year = "third_year"
        next_year = "fourth_year"
    else:
        return "Student has completed all years."

    # Retrieve courses available for the next academic year
    # next_year_courses = original_data.get(next_year)
    electives_to_be_taken = []

    # Filter out courses already completed by the student
    for courses in student_transcript.get(current_year, {}).values():
        for course in courses:
            if course in next_year_courses.values():
                next_year_courses = list(filter(lambda x: x != course, next_year_courses))

    # If elective courses are available, recommend them
    for elective_taken in student_transcript[current_year]["discipline_elective_courses"]:
        electives_to_be_taken.append(self.find_closest_courses(elective_taken))

    next_year_courses.popitem()

    return (next_year_courses, electives_to_be_taken)
