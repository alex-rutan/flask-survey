from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def load_home():
    """Loads homepage and the button form that begins the survey"""

    return render_template(
        "survey_start.html",
        survey=survey
    )


@app.route('/begin', methods=["POST"])
def start_survey():
    """Redirects to the first question of the survey"""

    return redirect("/questions/0")



@app.route('/questions/<int:questionNum>', methods=["POST"])
def ask_questions(questionNum):
    """Loads pages for each question in the survey, and logs answer in responses list"""

    return render_template(
        "question.html",
        question=survey.questions[questionNum]
    )



