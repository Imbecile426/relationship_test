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
    return '''
    <h1>Relationship Test Quiz</h1>
    <form action="/questions/0" method="post">
        <label for="name1">Your Name:</label>
        <input type="text" id="name1" name="name1" required><br>
        <label for="dob1">Your Date of Birth:</label>
        <input type="date" id="dob1" name="dob1" required><br>

        <label for="name2">Partner's Name:</label>
        <input type="text" id="name2" name="name2" required><br>
        <label for="dob2">Partner's Date of Birth:</label>
        <input type="date" id="dob2" name="dob2" required><br>

        <button type="submit">Start Quiz</button>
    </form>
    '''

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

    return f'''
    <h1>Question {qid + 1}</h1>
    <form action="/questions/{qid + 1}" method="post">
        <p>{question}</p>
        <label for="your_answer">Your Answer:</label>
        <input type="text" id="your_answer" name="your_answer" required><br>

        <label for="partner_answer">Partner's Answer:</label>
        <input type="text" id="partner_answer" name="partner_answer" required><br>

        <button type="submit">Next Question</button>
    </form>
    '''

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

    return f'''
    <h1>Relationship Test Result</h1>
    <p>Your Name: {name1}</p>
    <p>Your Date of Birth: {dob1}</p>
    <p>Partner's Name: {name2}</p>
    <p>Partner's Date of Birth: {dob2}</p>
    <h2>Result: {result}</h2>
    <a href="/">Try Again</a>
    '''

@app.route('/db')
def show_db():
    """Display all entries in the database."""
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM participants')
    entries = cursor.fetchall()
    conn.close()

    entries_html = '<br>'.join([
        f"ID: {entry[0]}, Name1: {entry[1]}, DOB1: {entry[2]}, Name2: {entry[3]}, DOB2: {entry[4]}"
        for entry in entries
    ])

    return f'''
    <h1>Database Entries</h1>
    {entries_html if entries else '<p>No entries found.</p>'}
    <a href="/">Back to Home</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)