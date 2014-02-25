from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

# code will go here?
@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_git = request.args.get("github")
    rows = hackbright_app.get_grades_by_student(student_git)
    html = render_template("student_info.html", github = student_git, rows = rows)
    return html

@app.route("/project/<project_name>")
def all_grades(project_name):
    hackbright_app.connect_to_db()
    rows = hackbright_app.all_grades_for_project(project_name)
    html = render_template("all_grades.html", rows = rows)
    return html

@app.route("/new_student")
def make_new_student():
    return render_template("new_student.html")

@app.route("/new_student/created")
def made_new_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    git = request.args.get("git")
    hackbright_app.make_new_student(first_name, last_name, git)
    html = render_template("new_student_created.html", first_name = first_name,
                                                       last_name = last_name,
                                                       git = git)
    return html

@app.route("/new_project")
def make_new_project():
    return render_template("new_project.html")

@app.route("/new_project/created")
def made_new_project():
    hackbright_app.connect_to_db()
    project_name = request.args.get("project_name")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    hackbright_app.make_new_project(project_name, description, max_grade)
    html = render_template("new_project_created.html", project_name = project_name,
                                                       description = description,
                                                       max_grade = max_grade)
    return html

@app.route("/new_grade")
def add_new_grade():
    return render_template("new_grade.html")

@app.route("/new_grade/added")
def added_new_grade():
    hackbright_app.connect_to_db()
    student_git = request.args.get("student_git")
    project_name = request.args.get("project_name")
    grade = request.args.get("grade")
    hackbright_app.add_new_grade(student_git, project_name, grade)
    rows = hackbright_app.get_grades_by_student(student_git)
    html = render_template("student_info.html", rows=rows)
    return html


if __name__ == "__main__":
    app.run(debug=True)