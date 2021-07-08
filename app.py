from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


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

    session["responses"] = []

    return redirect("/questions/0")



@app.route('/questions/<int:question_num>')
def ask_questions(question_num):
    """Loads pages for each question in the survey, and logs answer in responses list"""

    return render_template(
        "question.html",
        question=survey.questions[question_num]
    )


@app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form['answer']

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    if len(responses) == len(survey.questions):
        return redirect('/thanks')

    new_question_index = len(responses)




    return redirect(f'/questions/{new_question_index}')


@app.route('/thanks')
def thank_user():

    return render_template('completion.html')    


