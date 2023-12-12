from flask import Flask, render_template, request, jsonify
import os
import openai
import random
import json

app = Flask(__name__)

# Retrieve and set the API key for OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

def grade_paper(text):
    # Assess the quality of writing
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Grade the following text based on creativity:\n{text}",
        max_tokens=50
    )
    grade = response.choices[0].text.strip()

    # Assign a random grade if the grade is not clear
    if grade not in ["A", "B", "C", "D", "F"]:
        grade = random.choice(["A", "B", "C", "D", "F"])

    # Generate feedback based on the grade
    if grade in ["A", "B"]:
        style = "Snoop Dogg"
        feedback_prompt = f"Write a positive feedback in the style of {style} for a grade {grade} text."
    elif grade in ["C", "D"]:
        style = "Arnold Schwarzenegger"
        feedback_prompt = f"Write a motivational feedback in the style of {style} for a grade {grade} text."
    elif grade == "F":
        style = "Stewie Griffin"
        feedback_prompt = f"Write a condescending feedback in the style of {style} for a grade {grade} text."

    feedback_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=feedback_prompt,
        max_tokens=60
    )
    feedback = feedback_response.choices[0].text.strip()

    return grade, feedback

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_work = request.form['student_work']
        grade, feedback = grade_paper(student_work)
        return render_template('index.html', grade=grade, feedback=feedback)
    return render_template('index.html')

@app.route('/grade', methods=['POST'])
def grade():
    student_work = request.get_json()['studentWork']
    grade, feedback = grade_paper(student_work)
    return jsonify({'grade': grade, 'feedback': feedback})

if __name__ == '__main__':
    app.run(debug=True)
