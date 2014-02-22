import sqlite3

DB = None
CONN = None

def get_student_by_git(git):
    query = """SELECT first_name, last_name, git FROM Students WHERE git = ?"""
    DB.execute(query, (git,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, git):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, git))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def find_project(project):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchone()
    print """\
Project: %s
Description: %s
Max Grade: %s""" % (row[1], row[2], row[3])

def make_new_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print """\
Successfully added project: %s
Description: %s
Max Grade: %s""" % (title, description, max_grade)

def join_args(args, exp_len):
    if exp_len == 1:
        if len(args) > 1:
            args = [' '.join(args)]
    elif exp_len == 2:
        if len(args) > 2:
            args = [args[0], ' '.join(args[1:])]
    elif exp_len == 3:
        if len(args) > 3:
            args = ' '.join(args)
            args = args.split("\"")
    elif exp_len == "newgrade":
        if len(args) > 3:
            args = [args[0], ' '.join(args[1:-1]), args[-1]]
    return args 

def check_for_quotes(args):
    wrong_quotes = False
    double_quotes = 0
    for arg in args:
        if arg[0] == "'":
            wrong_quotes = True
        if len(args) > 3:
            if '"' in arg:
                double_quotes += 1
    if len(args) > 3 and (double_quotes != 2 or double_quotes != 4):
        wrong_quotes = True
    return wrong_quotes

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
    print """\
Successfully added grade %s
for %s for project %s""" % (grade, student_git, project_title)

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_git(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            args = join_args(args, 1)
            find_project(*args)
        elif command == "new_project":
            formatting_error = False
            if len(args) < 3:
                formatting_error = True
            if not check_for_quotes(args) and formatting_error == False:
                if len(args) == 3:
                    make_new_project(*args)
                else:
                    args = join_args(args, 3)
                    make_new_project(*args)
            else:
                print "Please put project name and description in double quotes"
        elif command == "student_grade_for":
            args = join_args(args, 2)
            get_grade_by_student_for_project(*args)
        elif command == "new_grade":
            args = join_args(args, "newgrade")
            add_new_grade(*args)
        elif command == "student_grades":
            get_grades_by_student(*args)

    CONN.close()


if __name__ == "__main__":
    main()
