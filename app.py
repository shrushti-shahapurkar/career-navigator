from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "career_navigator_secret"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name,email,password) VALUES (?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]

            return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        name=session['user_name']
    )

@app.route('/skills', methods=['GET', 'POST'])
def skills():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        skill_name = request.form['skill_name']
        status = request.form['status']

        cursor.execute(
            '''
            INSERT INTO skills
            (user_id, skill_name, status)
            VALUES (?, ?, ?)
            ''',
            (
                session['user_id'],
                skill_name,
                status
            )
        )

        conn.commit()

    cursor.execute(
        '''
        SELECT * FROM skills
        WHERE user_id=?
        ''',
        (session['user_id'],)
    )

    skills = cursor.fetchall()

    conn.close()

    return render_template(
        'skills.html',
        skills=skills
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/delete_skill/<int:id>')
def delete_skill(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM skills WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/skills')

if __name__ == '__main__':
    app.run(debug=True)