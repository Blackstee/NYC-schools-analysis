import datetime

from infrastructure.switchlang import switch
import program_hosts as hosts
import services.data_service as svc
from program_hosts import success_msg, error_msg
import infrastructure.state as state


def run():
    print(' ****************** Welcome guest **************** ')
    print()

    show_commands()

    while True:
        action = hosts.get_action()

        with switch(action) as s:
            s.case('c', hosts.create_account)
            s.case('l', hosts.log_into_account)

            s.case('a', add_a_school)
            s.case('y', view_his_schools)
            s.case('v', view_districts)

            s.case('m', lambda: 'change_mode')

            s.case('?', show_commands)
            s.case('', lambda: None)
            s.case(['x', 'bye', 'exit', 'exit()'], hosts.exit_app)

            s.default(hosts.unknown_command)

        state.reload_account()

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('[L]ogin to your account')
    print('[A]dd a school')
    print('View [y]our top-10_schools')
    print('[V]iew districts')
    print('[M]ain menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


# ====================================== Work with data ================================


def add_a_school():
    print(' ****************** Add a school **************** ')
    print ("%s", state.active_account)
    if not state.active_account:
        error_msg("You must log in first to add a school")
        return

    name = input("What is your school's name? ")
    if not name:
        error_msg('cancelled')
        return

    dbn = input("What is your school's dbn? ")
    if not dbn:
        error_msg('cancelled')
        return

    num_takers = input('How many people are taking exam 1? ')

    reading_score = input('Reading score? ')

    math_score = input('Math score? ')

    writing_score = input('Writing score? ')

    num_takers2 = input('How many people are taking exam 2? ')

    exam_taken2 = input('How many people have taken exam 2? ')

    exam_good2 = input('ow many people have taken exam 2 good? ')

    school = svc.add_school_custom(state.active_account, dbn, name, num_takers, reading_score, math_score, writing_score, num_takers2, exam_taken2, exam_good2)

    state.reload_account()
    success_msg('Created {} with id {}'.format(school.name, school.id))


def view_his_schools():
    print(' ****************** Your saved schools **************** ')
    if not state.active_account:
        error_msg("You must log in first to view your schools")
        return

    schools = svc.get_schools_for_user(state.active_account.id)
    print("You have {} schools.".format(len(schools)))
    for s in schools:
        print(" * {} has a DBN {}, average math score {}, average reading score {}, average writing score {}.".format(
            s.name,
            s.dbn,
            s.math_score,
            s.reading_score,
            s.writing_score
        ))

def view_districts():
    print(' ****************** Districts **************** ')
    if not state.active_account:
        error_msg("You must log in first to get districts")
        return

    districts = svc.get_districts()
    print("There are {} districts.".format(len(districts)))
    for s in districts:
        print(" * District {} has attendance {} and enrollment {}.".format(
            s.district,
            s.attendance,
            s.enrol
        ))