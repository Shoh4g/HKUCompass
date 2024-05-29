import PyPDF2
import re, io
from typing import BinaryIO


def extract_text_from_pdf(pdf_file: BinaryIO):
    # Create a PDF reader object from the binary file
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    # Loop through each page in the PDF document
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        # Extract text from the current page and accumulate it
        text += page.extract_text()
    return text


def extract_transcript_info(pdf_file: BinaryIO):
    # Create an in-memory binary stream for the PDF file to facilitate extraction
    pdf_data = io.BytesIO(pdf_file)
    # Extract all text from the PDF using the previously defined function
    pdf_text = extract_text_from_pdf(pdf_data)
    student_info = {}
    courses = []

    # Define a regex pattern to find the student's name and ID in the text
    name_id_pattern = r"Official Name: (.+)\s(\d+)"
    match = re.search(name_id_pattern, pdf_text)
    if match:
        student_info["Name"] = match.group(1)
        student_info["Student ID"] = match.group(2)

    program_level_pattern = (
        r"Academic Career: (.+)\nAcademic Program: (.+)\nLevel: (.+)"
    )
    match = re.search(program_level_pattern, pdf_text)
    if match:
        student_info["Academic Career"] = match.group(1)
        student_info["Academic Program"] = match.group(2)
        student_info["Year of Study"] = match.group(3)

    # Define a regex pattern to extract detailed course information
    course_pattern = r"([A-Z]{4}\s+\d{4})\s+(.+?)\s+(\d{4}-\d{2}\s+.+?)\s+(\S+)\s+(\S+)"
    matches = re.findall(course_pattern, pdf_text)
    for match in matches:
        course = {
            "Course Code": match[0],
            "Course Title": match[1],
            "Term": match[2],
            "Grade": match[3],
            "Units": match[4],
        }
        courses.append(course)

    # Aggregate all extracted course data into the student info dictionary
    student_info["Courses"] = courses

    return student_info