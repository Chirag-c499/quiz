from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import *
from auth import login_required, get_current_user
from operations import create_quiz
import os
import datetime

app = Flask(__name__)
app.secret_key = "secret-key"

db.connect()
db.create_tables([User, Quiz, Question, Result])

@app.route("/")
def home():
    user = get_current_user()
    return render_template("dashboard.html", user=user)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        is_admin = "admin" in request.form
        try:
            User.create(username=username, password=password, is_admin=is_admin)
            flash("Account created! You can now login.", "success")
            return redirect(url_for("login"))
        except:
            flash("Username already taken", "danger")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            user = User.get(User.username == username, User.password == password)
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        except:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

@app.route("/quizzes")
@login_required
def quiz_list():
    quizzes = Quiz.select()
    return render_template("quiz_list.html", quizzes=quizzes)

# Route to take a quiz
@app.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.get_by_id(quiz_id)
    questions = Question.select().where(Question.quiz == quiz)

    if request.method == "POST":
        score = 0
        for q in questions:
            selected = request.form.get(f"q{q.id}")
            print(f"Q{q.id}: selected={selected}, correct={q.correct_answer}")  # Debug line
            if selected and selected.upper() == q.correct_answer.upper():
                score += 1

        Result.create(user=get_current_user(), quiz=quiz, score=score)
        return redirect(url_for("quiz_result", quiz_id=quiz.id))

    return render_template("take_quiz.html", quiz=quiz, questions=questions)

@app.route("/quiz/<int:quiz_id>/result")
@login_required
def quiz_result(quiz_id):
    user = get_current_user()
    quiz = Quiz.get_by_id(quiz_id)
    result = Result.get_or_none(Result.user == user, Result.quiz == quiz)
    return render_template("quiz_result.html", quiz=quiz, result=result)

@app.route("/admin/add-quiz", methods=["GET", "POST"])
@login_required
def admin_add_quiz():
    user = get_current_user()
    if not user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("home"))
    if request.method == "POST":
        title = request.form["title"]
        questions = []
        for i in range(1, 6):
            questions.append({
                "text": request.form[f"q{i}"],
                "a": request.form[f"q{i}_a"],
                "b": request.form[f"q{i}_b"],
                "c": request.form[f"q{i}_c"],
                "d": request.form[f"q{i}_d"],
                "correct": request.form[f"q{i}_correct"]
            })
        create_quiz(title, questions)
        flash("Quiz created successfully!", "success")
        return redirect(url_for("quiz_list"))
    return render_template("admin_add_quiz.html")

if __name__ == "__main__":
    app.run(debug=True)
