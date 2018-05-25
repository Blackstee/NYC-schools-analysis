import csv

import pandas
import numpy as np
import data.Schools as Schools
import data.Student as Student
import sys

import schools.services.data_service as svc
import random
import numpy as np
import mongoengine


import names


# ==================================== HELP GENERATORS ==============================


def generate_names(sex):

    if sex == "male":

        return names.get_full_name(gender='male')
    else:

        return names.get_full_name(gender='female')



def generate_sex():

    if random.randint(1, 10000)%2 == 0:

        return "male"
    else:

        return "female"



def generate_score():

    return random.randint(60, 100)


def generate_number_students():

    return random.randint(20, 35)


def generate_distr():
    return random.randint(1, 32)


# ========================================== MAIN GENERATORS ===========================

def generate_student(form_name):

    sex = generate_sex()
    full_name = generate_names(sex)

    student = svc.add_student(form_name, full_name, sex)

    print('Created {} with id {}'.format(student.full_name, student.id))



def generate_forms(school_dbn):


    for i in range(1, 12):

        number_students = generate_number_students()
        form = svc.add_form(school_dbn, str(i))

        for k in range(1, number_students):

            generate_student(form.id)


        print('Created {} with id {}'.format(form.name, form.id))


def make_schools_full():

    for each in Schools.objects.all():

        generate_forms(each.dbn)




