import numpy as np
import pandas as pd
import time
import mongoengine
from data.Student import Student
from data.Att_by_Distr import Att_by_Distr
import services.data_service as svc

from schools.infrastructure.switchlang import switch
from schools.program_hosts import get_action, unknown_command, exit_app


def analysis_districts() -> Att_by_Distr:
    print('\n ****************** START ANALYSIS OF DISTRICTS  **************** \n')
    dist = []
    attendance = []
    enrollment = []
    for distr in Att_by_Distr.objects:
        dist.append(distr.district)
        attendance.append(distr.attendance)
        enrollment.append(distr.enrol)

    dist_stat = pd.DataFrame(np.column_stack([dist, attendance, enrollment]),
                             columns=['District', 'Attendance', 'Enrollment'])

    for col in dist_stat:
        dist_stat[col] = pd.to_numeric(pd.Series(dist_stat[col]), errors='ignore')

    print(' ****************** Top 10 districts with biggest enrollment  **************** \n')
    print(dist_stat[['District', 'Enrollment']].groupby(['District'], as_index=False).mean().sort_values(by = 'Enrollment', ascending= False).head(10))


def get_dataframe():
    sex = []
    district = []
    avg_score = []
    for student in Student.objects:
        sex.append(student.sex)
        district.append(student.district)
        avg_score.append(student.avg_score)

    stud_stat = pd.DataFrame(np.column_stack([sex, district, avg_score]),
                             columns=['Sex', 'District', 'Avg_score'])
    return stud_stat


def analysis_students() -> Student:
    print('\n ****************** START ANALYSIS OF STUDENTS  **************** \n')

    print('\n ****************** UPDATING ALL SCORES  **************** \n')
    time.sleep(5)
    print('\n ****************** ALL SCORES UPDATED  **************** \n')
    #svc.update_av_score_all_students()
    stud_stat = get_dataframe()

    for col in stud_stat:
        stud_stat[col] = pd.to_numeric(pd.Series(stud_stat[col]), errors='ignore')


    print(' ****************** Dependence of average score on male or female  **************** \n')
    print(stud_stat[['Sex', 'Avg_score']].groupby(['Sex'], as_index=False).mean())

    print('\n ****************** Dependence of average score on district **************** \n')
    print(stud_stat[['District', 'Avg_score']].groupby(['District'], as_index=False).mean())

    print('\n ****************** Top 5 districts with students which average of average scores are the highest **************** \n')
    print(stud_stat[['District', 'Avg_score']].groupby(['District'], as_index=False).mean().sort_values(by = 'Avg_score', ascending= False).head(5))

    show_commands3()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('1', save_to_file)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands3)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return

def show_commands3():
    print('Which dataframe save to file?:')
    print('Yes = > 1')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()

def save_to_file():
    stud_stat = get_dataframe()
    stud_stat.to_csv('saved.csv')
    return print ("successfully saved")