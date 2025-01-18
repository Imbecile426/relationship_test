from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Database setup
def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name1 TEXT NOT NULL,
            dob1 TEXT NOT NULL,
            name2 TEXT NOT NULL,
            dob2 TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Static list of questions
question_list = [
    "What is your favorite color?",
    "What is your favorite hobby?",
    "What is your favorite cuisine?",
    "What is your dream travel destination?",
    "What is your favorite movie genre?",
    "What kind of music do you enjoy most?",
    "What is your favorite season?",
    "What is your favorite animal?",
    "What is your favorite type of sport?",
    "What is your favorite book or author?"
]

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/questions/<int:qid>', methods=['POST'])
def questions(qid):
    """Render each quiz question page."""
    if qid >= len(question_list):
        return redirect(url_for('result'))

    # Retain participant details and responses across requests
    if qid == 0:
        session['name1'] = request.form['name1']
        session['dob1'] = request.form['dob1']
        session['name2'] = request.form['name2']
        session['dob2'] = request.form['dob2']
        session['responses'] = []

        # Store participant details in the database
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO participants (name1, dob1, name2, dob2)
            VALUES (?, ?, ?, ?)
        ''', (session['name1'], session['dob1'], session['name2'], session['dob2']))
        conn.commit()
        conn.close()

    question = question_list[qid]

    return render_template('question.html', question=question, qid=qid)

@app.route('/result', methods=['POST', 'GET'])
def result():
    """Display the result of the quiz."""
    if request.method == 'POST':
        your_answer = request.form.get('your_answer', '')
        partner_answer = request.form.get('partner_answer', '')
        session['responses'].append((your_answer, partner_answer))

    name1 = session['name1']
    dob1 = session['dob1']
    name2 = session['name2']
    dob2 = session['dob2']

    # Generate a random result
    result = random.choice(["Not Compatible", "Extremely Incompatible"])

    return render_template('result.html', name1=name1, dob1=dob1, name2=name2, dob2=dob2, result=result)

@app.route('/db')
def show_db():
    """Display all entries in the database."""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM participants')
    entries = cursor.fetchall()
    conn.close()

    return render_template('db.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)