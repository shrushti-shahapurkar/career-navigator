from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename
import os
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skill_name TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS internships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        company TEXT,
        role TEXT,
        duration TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        project_name TEXT,
        description TEXT,
        github_link TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        certificate_name TEXT,
        organization TEXT,
        issue_date TEXT
    )
    """)

    conn.commit()
    conn.close()



app = Flask(__name__)
app.secret_key = "career_navigator_secret"

app.config['UPLOAD_FOLDER'] = 'static/uploads'




# ---------------- AI CAREER ----------------
def get_career(skills):

    skill_list = [s[2].lower() for s in skills]

    score = {
        "frontend": 0,
        "backend": 0,
        "data": 0,
        "cyber": 0
    }

    # Frontend skills
    if "html" in skill_list: score["frontend"] += 2
    if "css" in skill_list: score["frontend"] += 2
    if "javascript" in skill_list: score["frontend"] += 3
    if "react" in skill_list: score["frontend"] += 4

    # Backend skills
    if "python" in skill_list: score["backend"] += 3
    if "flask" in skill_list: score["backend"] += 4
    if "django" in skill_list: score["backend"] += 4
    if "sql" in skill_list: score["backend"] += 3

    # Data skills
    if "python" in skill_list: score["data"] += 3
    if "sql" in skill_list: score["data"] += 4
    if "excel" in skill_list: score["data"] += 2

    # Cyber security
    if "networking" in skill_list: score["cyber"] += 3
    if "linux" in skill_list: score["cyber"] += 3
    if "security" in skill_list: score["cyber"] += 4

    best = max(score, key=score.get)

    if best == "frontend":
        return "Frontend Developer (React / UI Engineer)"
    elif best == "backend":
        return "Backend Developer (Python / Flask / Django)"
    elif best == "data":
        return "Data Analyst / Data Scientist"
    elif best == "cyber":
        return "Cyber Security Engineer"
    else:
        return "Full Stack Developer (Start with Web + Python)"


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

import time

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
@app.route('/download_resume')
def download_resume():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # User
    cursor.execute(
        "SELECT name, bio FROM users WHERE id=?",
        (session['user_id'],)
    )
    user = cursor.fetchone()

    # Skills
    cursor.execute(
        "SELECT skill_name FROM skills WHERE user_id=?",
        (session['user_id'],)
    )
    skills = cursor.fetchall()

    # Internships
    cursor.execute(
        "SELECT company, role, duration FROM internships WHERE user_id=?",
        (session['user_id'],)
    )
    internships = cursor.fetchall()

    # Projects
    cursor.execute(
        "SELECT project_name, github_link FROM projects WHERE user_id=?",
        (session['user_id'],)
    )
    projects = cursor.fetchall()

    # Certificates
    cursor.execute(
        """
        SELECT certificate_name, organization, issue_date
        FROM certificates
        WHERE user_id=?
        """,
        (session['user_id'],)
    )
    certificates = cursor.fetchall()

    conn.close()

    filename = f"static/resume_{session['user_id']}_{int(time.time())}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()
    content = []

    # Header
    content.append(Paragraph(user[0], styles['Title']))
    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            user[1] if user[1] else "Engineering Student",
            styles['Normal']
        )
    )

    content.append(Spacer(1, 20))

    # Skills
    content.append(Paragraph("SKILLS", styles['Heading2']))

    if skills:
        for skill in skills:
            content.append(
                Paragraph(f"• {skill[0]}", styles['Normal'])
            )
    else:
        content.append(
            Paragraph("No skills added yet.", styles['Normal'])
        )

    content.append(Spacer(1, 15))

    # Internships
    content.append(Paragraph("INTERNSHIPS", styles['Heading2']))

    if internships:
        for internship in internships:
            content.append(
                Paragraph(
                    f"• {internship[0]} - {internship[1]} ({internship[2]})",
                    styles['Normal']
                )
            )
    else:
        content.append(
            Paragraph("No internships added yet.", styles['Normal'])
        )

    content.append(Spacer(1, 15))

    # Projects
    content.append(Paragraph("PROJECTS", styles['Heading2']))

    if projects:
        for project in projects:

            content.append(
                Paragraph(
                    f"• {project[0]}",
                    styles['Normal']
                )
            )

            if project[1]:
                content.append(
                    Paragraph(
                        f"GitHub: {project[1]}",
                        styles['Normal']
                    )
                )

    else:
        content.append(
            Paragraph("No projects added yet.", styles['Normal'])
        )

    content.append(Spacer(1, 15))

    
    

    # Certificates
    content.append(Paragraph("CERTIFICATES", styles['Heading2']))

    if certificates:
        for certificate in certificates:
            content.append(
                Paragraph(
                    f"• {certificate[0]} - {certificate[1]} ({certificate[2]})",
                    styles['Normal']
                )
            )
    else:
        content.append(
            Paragraph("No certificates added yet.", styles['Normal'])
        )

    content.append(Spacer(1, 20))

    # Career Goal
    content.append(Paragraph("CAREER GOAL", styles['Heading2']))
    content.append(
        Paragraph(
            "Backend Developer / Software Engineer",
            styles['Normal']
        )
    )

    doc.build(content)

    return redirect('/' + filename)


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name,email,password) VALUES (?,?,?)",
                (name, email, password)
            )

            conn.commit()
            return redirect('/login')

        except sqlite3.IntegrityError:
            return "⚠️ Email already exists. Try another email."

        finally:
            conn.close()

    return render_template('register.html')


# ---------------- LOGIN ----------------
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

        return "Invalid Login"

    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # User Info
    cursor.execute("""
        SELECT name, bio, profile_pic
        FROM users
        WHERE id=?
    """, (session['user_id'],))

    user = cursor.fetchone()

    # Skills
    cursor.execute("""
        SELECT *
        FROM skills
        WHERE user_id=?
    """, (session['user_id'],))

    skills = cursor.fetchall()

    # AI Career Suggestion
    career = get_career(skills)

    # Skill Counts for Chart
    skill_names = [s[2].lower() for s in skills]

    python_count = skill_names.count("python")
    html_count = skill_names.count("html")
    css_count = skill_names.count("css")
    sql_count = skill_names.count("sql")
    flask_count = skill_names.count("flask")

    # Statistics
    total_skills = len(skills)

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM internships WHERE user_id=?",
            (session['user_id'],)
        )
        total_internships = cursor.fetchone()[0]
    except:
        total_internships = 0

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM projects WHERE user_id=?",
            (session['user_id'],)
        )
        total_projects = cursor.fetchone()[0]
    except:
        total_projects = 0

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM certificates WHERE user_id=?",
            (session['user_id'],)
        )
        total_certificates = cursor.fetchone()[0]
    except:
        total_certificates = 0

    conn.close()

    return render_template(
        'dashboard.html',

        name=user[0],
        bio=user[1],
        profile_pic=user[2],

        skills=skills,
        career=career,

        python_count=python_count,
        html_count=html_count,
        css_count=css_count,
        sql_count=sql_count,
        flask_count=flask_count,

        total_skills=total_skills,
        total_internships=total_internships,
        total_projects=total_projects,
        total_certificates=total_certificates
    )


# ---------------- SKILLS ----------------
@app.route('/skills', methods=['GET', 'POST'])
def skills():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        skill_name = request.form['skill_name']
        status = request.form['status']

        cursor.execute("""
            INSERT INTO skills (user_id, skill_name, status)
            VALUES (?, ?, ?)
        """, (session['user_id'], skill_name, status))

        conn.commit()

    cursor.execute("SELECT * FROM skills WHERE user_id=?", (session['user_id'],))
    skills = cursor.fetchall()

    conn.close()

    return render_template("skills.html", skills=skills)


# ---------------- DELETE ----------------
@app.route('/delete_skill/<int:id>')
def delete_skill(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM skills WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/skills')


# ---------------- EDIT ----------------
@app.route('/edit_skill/<int:id>', methods=['GET', 'POST'])
def edit_skill(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        skill_name = request.form['skill_name']
        status = request.form['status']

        cursor.execute("""
            UPDATE skills
            SET skill_name=?, status=?
            WHERE id=?
        """, (skill_name, status, id))

        conn.commit()
        conn.close()

        return redirect('/skills')

    cursor.execute("SELECT * FROM skills WHERE id=?", (id,))
    skill = cursor.fetchone()

    conn.close()

    return render_template("edit_skill.html", skill=skill)


# ---------------- PROFILE UPLOAD ----------------
@app.route('/upload_profile', methods=['POST'])
def upload_profile():

    if 'user_id' not in session:
        return redirect('/login')

    bio = request.form['bio']
    file = request.files['profile_pic']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT profile_pic FROM users WHERE id=?",
        (session['user_id'],)
    )

    result = cursor.fetchone()
    filename = result[0] if result else None

    if file and file.filename:

        filename = secure_filename(file.filename)

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        file.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

    cursor.execute("""
        UPDATE users
        SET bio=?, profile_pic=?
        WHERE id=?
    """, (
        bio,
        filename,
        session['user_id']
    ))

    conn.commit()
    conn.close()

    return redirect('/dashboard')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#-----------------internship--------------

@app.route('/internships', methods=['GET', 'POST'])
def internships():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        company = request.form['company']
        role = request.form['role']
        duration = request.form['duration']

        cursor.execute("""
            INSERT INTO internships
            (user_id, company, role, duration)
            VALUES (?, ?, ?, ?)
        """, (
            session['user_id'],
            company,
            role,
            duration
        ))

        conn.commit()

    cursor.execute("""
        SELECT * FROM internships
        WHERE user_id=?
    """, (session['user_id'],))

    internships = cursor.fetchall()

    conn.close()

    return render_template(
        'internships.html',
        internships=internships
    )
@app.route('/delete_internship/<int:id>')
def delete_internship(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM internships WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/internships')
@app.route('/edit_internship/<int:id>', methods=['GET', 'POST'])
def edit_internship(id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        company = request.form['company']
        role = request.form['role']
        duration = request.form['duration']

        cursor.execute("""
            UPDATE internships
            SET company=?,
                role=?,
                duration=?
            WHERE id=?
        """, (
            company,
            role,
            duration,
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/internships')

    cursor.execute(
        "SELECT * FROM internships WHERE id=?",
        (id,)
    )

    internship = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_internship.html',
        internship=internship
    )
#------------------project-----------
@app.route('/projects', methods=['GET', 'POST'])
def projects():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        project_name = request.form['project_name']
        description = request.form['description']
        github_link = request.form['github_link']

        cursor.execute("""
            INSERT INTO projects
            (user_id, project_name, description, github_link)
            VALUES (?, ?, ?, ?)
        """, (
            session['user_id'],
            project_name,
            description,
            github_link
        ))

        conn.commit()

    cursor.execute("""
        SELECT * FROM projects
        WHERE user_id=?
    """, (session['user_id'],))

    projects = cursor.fetchall()

    conn.close()

    return render_template(
        'projects.html',
        projects=projects
    )

@app.route('/delete_project/<int:id>')
def delete_project(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM projects WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/projects')

@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        project_name = request.form['project_name']
        description = request.form['description']
        github_link = request.form['github_link']

        cursor.execute("""
            UPDATE projects
            SET project_name=?,
                description=?,
                github_link=?
            WHERE id=?
        """, (
            project_name,
            description,
            github_link,
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/projects')

    cursor.execute(
        "SELECT * FROM projects WHERE id=?",
        (id,)
    )

    project = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_project.html',
        project=project
    )
#---------------roadmap-----------------
@app.route('/roadmap')
def roadmap():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT skill_name FROM skills WHERE user_id=?",
        (session['user_id'],)
    )

    skills = [row[0].lower() for row in cursor.fetchall()]

    conn.close()

    roadmap = []

    if "python" in skills:
        roadmap = [
            "Python",
            "Flask",
            "SQL",
            "API Development",
            "Backend Developer"
        ]

    elif "html" in skills:
        roadmap = [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Frontend Developer"
        ]

    return render_template(
        'roadmap.html',
        roadmap=roadmap
    )
#----------------certificate-----------
@app.route('/certificates', methods=['GET', 'POST'])
def certificates():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        certificate_name = request.form['certificate_name']
        organization = request.form['organization']
        issue_date = request.form['issue_date']
        certificate_link = request.form['certificate_link']

        cursor.execute("""
            INSERT INTO certificates
            (user_id, certificate_name, organization, issue_date, certificate_link)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session['user_id'],
            certificate_name,
            organization,
            issue_date,
            certificate_link
        ))

        conn.commit()

    cursor.execute("""
        SELECT *
        FROM certificates
        WHERE user_id=?
    """, (session['user_id'],))

    certificates = cursor.fetchall()

    conn.close()

    return render_template(
        'certificates.html',
        certificates=certificates
    )
@app.route('/delete_certificate/<int:id>')
def delete_certificate(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM certificates WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/certificates')
@app.route('/edit_certificate/<int:id>', methods=['GET', 'POST'])
def edit_certificate(id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        certificate_name = request.form['certificate_name']
        organization = request.form['organization']
        issue_date = request.form['issue_date']
        certificate_link = request.form['certificate_link']

        cursor.execute("""
            UPDATE certificates
            SET certificate_name=?,
                organization=?,
                issue_date=?,
                certificate_link=?
            WHERE id=?
        """, (
            certificate_name,
            organization,
            issue_date,
            certificate_link,
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/certificates')

    cursor.execute(
        "SELECT * FROM certificates WHERE id=?",
        (id,)
    )

    certificate = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_certificate.html',
        certificate=certificate
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True)