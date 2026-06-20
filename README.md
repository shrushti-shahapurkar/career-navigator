# 🚀 Career Navigator

Career Navigator is a Flask-based web application designed for engineering students to manage and track their career development in one place.

The platform helps users organize their skills, internships, projects, certificates, and generate professional resumes while receiving career recommendations based on their skill set.

---

## ✨ Features

### 👤 User Management

* User Registration & Login
* Secure Session Management
* Profile Update
* Profile Picture Upload

### 📚 Skills Management

* Add Skills
* Update Skills
* Delete Skills
* Track Skill Progress

### 💼 Internship Management

* Add Internship Details
* Edit Internship Information
* Delete Internship Records

### 🛠 Project Management

* Add Projects
* Store GitHub Repository Links
* Edit Project Details
* Delete Projects

### 🏆 Certificate Management

* Add Certificates
* Store Certificate Links
* Edit Certificate Information
* Delete Certificates

### 🤖 AI Career Suggestions

* Analyze user skills
* Suggest suitable career paths

### 📄 Resume Generator

Generate a professional PDF resume containing:

* Personal Information
* Skills
* Internships
* Projects
* Certificates
* Career Goal

### 📊 Dashboard Analytics

* Total Skills
* Total Internships
* Total Projects
* Career Suggestions
* Skill Analysis Charts

---

## 🏗️ Technology Stack

### Backend

* Python
* Flask
* SQLite

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

### Libraries

* ReportLab (PDF Resume Generation)

---

## 📁 Project Structure

```text
career-navigator/
│
├── app.py
├── create_db.py
├── requirements.txt
├── .gitignore
│
├── static/
│   ├── uploads/
│   ├── styles/
│   └── generated_resumes/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── skills.html
│   ├── internships.html
│   ├── projects.html
│   ├── certificates.html
│   └── roadmap.html
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/shrushti-shahapurkar/career-navigator.git
```

### 2. Move into Project Folder

```bash
cd career-navigator
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Database

```bash
python create_db.py
```

### 5. Run Application

```bash
python app.py
```

### 6. Open Browser

```text
http://127.0.0.1:5000
```

---

## 🎯 Key Learning Outcomes

This project helped me learn:

* Flask Web Development
* Database Design with SQLite
* CRUD Operations
* Authentication & Sessions
* Template Rendering using Jinja2
* File Upload Handling
* PDF Generation with ReportLab
* Git & GitHub Workflow

---

## 🔮 Future Enhancements

* Dark Mode
* Activity Timeline
* Achievement Badges
* Advanced AI Career Recommendations
* Online Deployment
* Mobile Responsive Improvements

---

## 👩‍💻 Author

**Shrushti Shahapurkar**

Engineering Student | Python & Flask Developer

---

## 📜 License

This project is developed for learning and educational purposes.
