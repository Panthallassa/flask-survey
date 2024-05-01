from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "BurbujaBruja"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    return render_template('start_survey.html', survey=satisfaction_survey)

@app.route('/answer', methods=['POST', 'GET'])
def handle_answer():
    answer_yes = request.form.get('answer-yes')
    answer_no = request.form.get('answer-no')

    if answer_yes:
        answer = answer_yes
    elif answer_no:
        answer = answer_no
    else:
        # Handle error if no answer submitted
        return redirect(url_for('home_page'))

    responses.append(answer)
    next_question = len(responses)
    if next_question == len(satisfaction_survey.questions) - 1 and answer:
        return redirect(url_for('survey_complete'))
    else:
        return redirect(url_for('questions', num=next_question))

@app.route('/start_survey')
def start_survey():
    return redirect(url_for('questions', num=0))

@app.route('/questions/<int:num>')
def questions(num):
    if len(responses) == len(satisfaction_survey.questions):
        return redirect(url_for('survey_complete'))
    elif num == len(responses):
        if num < len(satisfaction_survey.questions):
            return render_template(f'question_{num}.html', survey=satisfaction_survey, question=satisfaction_survey.questions[num])
        else:
            return redirect(url_for('survey_complete'))
    else:
        flash("Please answer the questions in order.")
        return redirect(url_for('questions', num=len(responses)))
    
@app.route('/complete')
def survey_complete():
    return render_template('survey_complete.html')