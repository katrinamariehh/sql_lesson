import sqlite3

DB = None
CONN = None

def get_student_by_git(git):
    query = """SELECT first_name, last_name, git FROM Students WHERE git = ?"""
    DB.execute(query, (git,))
    row = DB.fetchone()
    return row

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, git):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, git))
    CONN.commit()
    return (first_name, last_name, git)
    # print "Successfully added student: %s %s" % (first_name, last_name)

def find_project(project):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchone()
    return row

def make_new_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()


def get_grade_by_student_for_project(student_git, project_title):
    query = """SELECT grade FROM Grades WHERE student_git = ? AND project_title = ?"""
    DB.execute(query, (student_git, project_title))
    row = DB.fetchone()
    print """\
%s's grade for the %s project is %s""" % (student_git, project_title, row[0])

def add_new_grade(student_git, project_title, grade):
    query = """INSERT INTO Grades (student_git, project_title, grade) VALUES (?,?,?)"""
    DB.execute(query, (student_git, project_title, grade))
    CONN.commit()

def get_grades_by_student(student_git):
    query = """SELECT project_title, grade, Projects.max_grade FROM Grades JOIN Projects ON (project_title = title) WHERE student_git = ?"""
    DB.execute(query, (student_git,))
    rows = DB.fetchall()
    return rows

def all_grades_for_project(project_title):
    query = """SELECT project_title, grades.student_git, grades.grade FROM Projects JOIN Grades ON (title = Grades.project_title) WHERE project_title = ?"""
    DB.execute(query, (project_title,))
    rows = DB.fetchall()
    return rows

def main():
    connect_to_db()
    command = None
    print "Please input arguments separated by commas"
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(None, 1)
        command = tokens[0]
        argstring = tokens[1]
        args = [ arg.strip() for arg in argstring.split(',') ]


        if command == "student":
            get_student_by_git(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            if len(args) == 1:
                find_project(*args)
            else:
                print "Please give exactly one argument"
        elif command == "new_project":
            if len(args) == 3:
                make_new_project(*args)
            else:
                print "Please give exactly 3 arguments"
        elif command == "student_grade_for":
            if len(args) == 2:
                get_grade_by_student_for_project(*args)
            else:
                print "Please give exactly 2 arguments"
        elif command == "new_grade":
            if len(args) == 3:
                add_new_grade(*args)
            else:
                print "Please give exactly 3 arguments"
        elif command == "student_grades":
            if len(args) == 1:
                get_grades_by_student(*args)
            else:
                print "Please give exactly 1 argument"
        elif command == "all_grades":
            if len(args) == 1:
                all_grades_for_project(*args)
            else:
                print "Please give exactly 1 argument"

    CONN.close()


if __name__ == "__main__":
    main()
