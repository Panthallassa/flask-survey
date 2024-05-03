from flask import Flask, render_template, redirect, url_for, request, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "BurbujaBruja"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/', methods=['POST', 'GET'])
def home_page():
    if request.cookies.get('survey_completed'):
        return render_template('survey_complete.html')

    session['responses'] = []
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
    
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    
    next_question = len(session['responses'])
    if next_question == len(satisfaction_survey.questions) and answer:
        response = make_response(redirect(url_for('survey_complete')))
        response.set_cookie('survey_completed', 'true')
        return response
    else:
        return redirect(url_for('questions', num=next_question))

@app.route('/start_survey', methods=['POST', 'GET'])
def start_survey():
    session['responses'] = []
    return redirect(url_for('questions', num=0))

@app.route('/questions/<int:num>')
def questions(num):
    if request.cookies.get('survey_completed'):
        return redirect(url_for('survey_complete'))
    
    elif num < len(session['responses']):
        return redirect(url_for('questions', num=num + 1))
    
    elif num == len(session['responses']):
        if num < len(satisfaction_survey.questions):
            return render_template(f'question_{num}.html', survey=satisfaction_survey, question=satisfaction_survey.questions[num])
        else:
            return redirect(url_for('survey_complete'))
    else:
        flash("Please answer the questions in order.")
        print(session['responses'])
        return redirect(url_for('questions', num=len(session['responses'])))
    
@app.route('/complete')
def survey_complete():
    return render_template('survey_complete.html')