from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY_NAME = "responses"


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

    session[RESPONSES_KEY_NAME] = []

    return redirect("/questions/0")



@app.route('/questions/<int:question_num>')
def ask_questions(question_num):
    """Loads pages for each question in the survey, and logs answer in responses list"""

    responses_length = len(session[RESPONSES_KEY_NAME])

    # If the user has completed all questions and tries to return to a survey question,
    # they will be redirected to the thanks endpoint
    if responses_length == len(survey.questions):
        flash('You have already completed the survey.')
        return redirect('/thanks')

    # If the user tries to skip ahead or go back to another question to a further question,
    # they will be redirected to the correct question
    if question_num != responses_length:
        flash('You tried to access an invalid question. Bad you.')
        return redirect(f'/questions/{responses_length}')

    return render_template(
        "question.html",
        question=survey.questions[question_num]
    )


@app.route('/answer', methods=['POST'])
def handle_answer():
    """Appends the user's answer to the session and redirects the user to the next question,
     or thanks page if they've completed all questions"""
    answer = request.form['answer']

    # TODO KEEP THESE LINES INTACT - Will implement database later
    responses = session[RESPONSES_KEY_NAME] 
    responses.append(answer)
    session[RESPONSES_KEY_NAME] = responses

    if len(responses) == len(survey.questions):
        return redirect('/thanks')

    new_question_index = len(responses)




    return redirect(f'/questions/{new_question_index}')


@app.route('/thanks')
def thank_user():
    """Thanks user for participating in the survey"""

    return render_template('completion.html')    


