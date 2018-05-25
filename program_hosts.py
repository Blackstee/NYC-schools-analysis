import datetime

from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc

import analysis as an

from schools.services.data_service import get_schools_sorted


def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('l', log_into_account)
            s.case('s', list_schools)
            s.case('a', attendance_an)
            s.case('n', scores_an)
            s.case('e', enrol_an)
            s.case('f', rate_forms_in_school)
            s.case('b', rate_students_all_forms_by_school)
            s.case('an_s', an.analysis_students)
            s.case('an_d', an.analysis_districts)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an [a]ccount')
    print('[L]ogin to your account')
    print('List all[S]chools')
    print('[A]nalyze attendance by district')
    print('Analyze [E]nrollment by district')
    print('A[N]alyze scores')
    print ('Rate all [F]orms in school')
    print('Rate all students in all forms [B]y school')
    print('[AN_S] Analysis of students')
    print('[AN_D] Analysis of districts')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


# =================================== Account stuff =====================================


def create_account():
    print(' ****************** REGISTER **************** ')

    name = input('What is your name? ')
    email = input('What is your email? ').strip().lower()

    old_account = svc.find_account_by_email(email)
    if old_account:
        error_msg(f"ERROR: Account with email {email} already exists.")
        return

    state.active_account = svc.create_account(name, email)
    success_msg(f"Created new account with id {state.active_account.id}.")


def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input('What is your email? ').strip().lower()
    account = svc.find_account_by_email(email)

    if not account:
        error_msg(f'Could not find account with email {email}.')
        return

    state.active_account = account
    success_msg('Logged in successfully.')



# ====================================== Work with data ================================


# list of all schools in NYC

def list_schools():
    print(' ****************** All schools in NYC **************** ')
    if not state.active_account:
        error_msg("You must log in first to view schools")
        return

    schools = svc.get_schools()
    print("There are {} schools.".format(len(schools)))
    for s in schools:
        print(" * {} has a DBN {}, average math score {}, average reading score {}, average writing score {}.".format(
            s.name,
            s.dbn,
            s.math_score,
            s.reading_score,
            s.writing_score
        ))



# list of districts of NYC sorted by attendance

def attendance_an():

    print(' ****************** Districts of NYC sorted by attendance **************** ')
    if not state.active_account:
        error_msg("You must log in first to view attendance by district anallysis")
        return

    districts = svc.get_districts_sorted("attendance")
    print("There are {} districts.".format(len(districts)))
    for s in districts:
        print(" * District {} has attendance {}.".format(
            s.district,
            s.attendance
        ))




# Districts of NYC sorted by enrollment

def enrol_an():

    print(' ****************** Districts of NYC sorted by enrollment **************** ')
    if not state.active_account:
        error_msg("You must log in first to view enrollment by district anallysis")
        return

    districts = svc.get_districts_sorted("enrol")
    print("There are {} districts.".format(len(districts)))
    for s in districts:
        print(" * District {} has enrollment {}.".format(
            s.district,
            s.enrol
        ))



#Schools of NYC sorted by any score

def scores_an():
    print(' ****************** Schools of NYC sorted by any score **************** ')
    if not state.active_account:
        error_msg("You must log in first to view scools by score analysis")
        return

    show_commands2()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('1', get_schools_sorted_m)
            s.case('2', get_schools_sorted_r)
            s.case('3', get_schools_sorted_w)
            s.case('4', get_schools_sorted_ex)
            s.case('5', get_schools_sorted_av)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


# sort schools by math

def get_schools_sorted_m ():
    schools = svc.get_schools_sorted("math_score")
    print("There are {} schools.".format(len(schools)))
    for s in schools:
        print(" * {} has a DBN {}, average math score {}, average reading score {}, average writing score {}.".format(
            s.name,
            s.dbn,
            s.math_score,
            s.reading_score,
            s.writing_score
        ))


# sort schools by reading

def get_schools_sorted_r ():
    schools = svc.get_schools_sorted("reading_score")
    print("There are {} schools.".format(len(schools)))
    for s in schools:
        print(" * {} has a DBN {}, average math score {}, average reading score {}, average writing score {}.\n Average score {}".format(
            s.name,
            s.dbn,
            s.math_score,
            s.reading_score,
            s.writing_score,
            s.avg_score
        ))



# sort schools by writing

def get_schools_sorted_w ():
    schools = svc.get_schools_sorted("writing_score")
    print("There are {} schools.".format(len(schools)))
    for s in schools:
        print(
            " * {} has a DBN {}, average math score {}, average reading score {}, average writing score {}.\n Average score {}".format(
                s.name,
                s.dbn,
                s.math_score,
                s.reading_score,
                s.writing_score,
                s.avg_score
            ))


# sort schools by exam 2

def get_schools_sorted_ex ():
    schools = svc.get_schools_sorted("exam_good2")
    print("There are {} schools.".format(len(schools)))
    for s in schools:
        print(
            " * {} has a DBN {}, average math score {}, average reading score {}, average writing score {}.\n Average score {}".format(
                s.name,
                s.dbn,
                s.math_score,
                s.reading_score,
                s.writing_score,
                s.avg_score
            ))

# sort schools by average score by average score of forms by average score of students

def get_schools_sorted_av():
    schools = svc.get_schools_sorted("avg_score")
    print("There are {} schools.".format(len(schools)))
    for s in schools:
        print(
            " * {} has a DBN {}, average math score {}, average reading score {}, average writing score {}.\n Average score {}".format(
                s.name,
                s.dbn,
                s.math_score,
                s.reading_score,
                s.writing_score,
                s.avg_score
            ))


# helper for sorting schools

def show_commands2():
    print('What score for sorting would you like to choose?:')
    print('Math average = > 1')
    print('Reading average = > 2')
    print('Writing average = > 3')
    print('Exam 2 with 3, 4, 5 = > 4')
    print('Average score = > 5')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


# ======================================= Rates ==================================================


# list of rated students in class

def rate_students_in_class (form_id):
    print(' ****************** Rating of top 10 students from chosen form  **************** ')
    if not state.active_account:
        error_msg("You must log in first to view students")
        return

    students_rated = svc.get_rated_students_for_class(form_id, 10)

    for s in students_rated:
        print(" * Student {} has average score {}.".format(
            s.full_name,
            s.avg_score
        ))

# list of rated forms in school

def rate_forms_in_school ():
    print(' ****************** Rating of top 10 forms from chosen school  **************** ')
    if not state.active_account:
        error_msg("You must log in first to view forms")
        return

    forms_rated = svc.get_rated_forms_for_school("01M448", 10)

    for s in forms_rated:
        print(" * Form {} has average score {}.".format(
            s.name,
            s.avg_score
        ))


# list of rated students in each class of school

def rate_students_all_forms_by_school():

    print(' ****************** Rating of top 10 students of all forms from chosen school  **************** ')
    if not state.active_account:
        error_msg("You must log in first to view rating")
        return

    forms = svc.get_forms_for_school("01M448")
    for f in forms:
        rate_students_in_class(f.id)




# ========================================= UPDATE AVERAGE SCORES =====================

# update average score of students in form

def update_average_scores_student_by_form(form_id):

    students = svc.get_students_for_class(form_id)
    for s in students:
        svc.update_aver_score_student(s.id)
    svc.update_aver_score_form(form_id)



# update average score of form in school

def update_average_scores_student_by_school(school_dbn):

    forms = svc.get_forms_for_school(school_dbn)
    for f in forms:
        update_average_scores_student_by_form(f.id)
    svc.update_aver_score_school(school_dbn)


# update average score of school everywhere

def update_average_scores_everywhere ():

    schools = svc.get_schools()
    for f in schools:
        update_average_scores_student_by_school(f.dbn)




# ================================ Helpers ================================

def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input( text)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print( text )


def error_msg(text):
    print(text)
