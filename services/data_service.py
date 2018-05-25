from typing import List

import datetime

import bson
import mongoengine

from data.owners import Owner
from data.Schools import Schools
from data.Student import Student
from data.Form import Form
from data.Att_by_Distr import Att_by_Distr
from data.Score import Score

import generator


# ================================== ACCOUNT STUFF ==========================

def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects(email=email).first()
    return owner


def find_School_by_dbn(dbn: str) -> Schools:
    school = Schools.objects(dbn=dbn).first()
    return school

# =================================== WORK WITH DATA ==============================


# =================================== STUDENTS ====================================

def add_student(form_id, full_name, sex) -> Student:

    student = Student()
    student.full_name  = full_name
    student.sex = sex

    student.save()

    form = Form.objects(id=form_id).first()
    form.Student_ids.append(student.id)
    form.save()


    return student




def add_score (stud_id, score, subject) -> Score:
    student = Student.objects(id=stud_id).first()
    mscore = Score()
    mscore.name = subject
    mscore.score = score
    mscore.save()
    student.scores_ids.append(mscore.id)
    student.save()


def add_districts_all() -> Student:

    for each in Student.objects.all():
        add_district(each.id)

def add_district(stud_id) ->Student:
    Student.objects(id=stud_id).update(district= generator.generate_distr())

def update_aver_score_student(stud_id) -> Student:

    Student.objects(id=stud_id).update(avg_score=get_average_score_for_student(stud_id))


def update_aver_score_form(form_id) -> Form:

    Form.objects(id=form_id).update(avg_score=get_average_score_for_form(form_id))


def update_aver_score_school(school_dbn) -> Schools:

    Schools.objects(dbn=school_dbn).update(avg_score=get_average_score_for_school(school_dbn))


def update_av_score_all_students() -> Student:
    for s in Student.objects:
        update_aver_score_student(s.id)


def generate_scores_all():

    for each in Student.objects.all():
        add_score(each.id, generator.generate_score(), "math")
        add_score(each.id, generator.generate_score(), "read")
        add_score(each.id, generator.generate_score(), "write")
        print('Generated scores for  {} with id {}'.format(each.full_name, each.id))

def get_students_for_class(class_id: bson.ObjectId) -> List[Student]:
    my_class = Form.objects(id=class_id).first()
    students = Student.objects(id__in=my_class.Student_ids).all()

    return list(students)


def get_scores_for_student(student_id: bson.ObjectId) -> List[Score]:
    my_student = Student.objects(id = student_id).first()
    scores = Score.objects(id__in = my_student.scores_ids).all()

    return list(scores)

def get_average_score_for_student(student_id: bson.ObjectId):
    my_student = Student.objects(id=student_id).first()
    avg= Score.objects(id__in=my_student.scores_ids).average('score')
    return avg

def get_average_score_for_form(form_id: bson.ObjectId):
    my_form = Form.objects(id=form_id).first()
    avg= Student.objects(id__in=my_form.Student_ids).average('avg_score')
    return avg

def get_average_score_for_school(school_dbn: bson.ObjectId):
    my_school = Schools.objects(dbn=school_dbn).first()
    avg= Form.objects(id__in=my_school.Form_ids).average('avg_score')
    return avg


def get_rated_students_for_class(form_id: bson.ObjectId, count) -> List[Student]:
    my_class = Form.objects(id=form_id).first()
    students = Student.objects(id__in=my_class.Student_ids).all().order_by("-" + "avg_score").limit(count)
    return list(students)

def get_rated_forms_for_school(school_dbn, count) -> List[Form]:
    my_school = Schools.objects(dbn=school_dbn).first()
    print (my_school)
    forms = Form.objects(id__in=my_school.Form_ids).all().order_by("-" + "avg_score").limit(count)
    return list(forms)

# ==================================== FORMS ======================================


def add_form(school_dbn, name) -> Form:

    form  = Form()
    form.name  = name

    form.save()

    school = Schools.objects(dbn=school_dbn).first()
    school.Form_ids.append(form.id)
    school.save()


    return form

def get_forms_for_school(school_dbn: bson.ObjectId) -> List[Form]:
    my_school = Schools.objects(dbn=school_dbn).first()
    forms = Form.objects(id__in=my_school.Form_ids).all()

    return forms




# =================================== SCHOOLS =====================================
def add_school_custom (account, dbn, name, num_takers, reading_score, math_score, writing_score, num_takers2, exam_taken2, exam_good2) -> Schools:
    school = Schools()
    school.dbn = dbn
    school.name = name
    school.num_takers = num_takers
    school.reading_score = reading_score
    school.math_score = math_score
    school.writing_score = writing_score
    school.num_takers2 = num_takers2
    school.exam_taken2 = exam_taken2
    school.exam_good2 = exam_good2

    school.save()

    owner = find_account_by_email(account.email)
    owner.School_ids.append(school.id)
    owner.save()

    return school


def add_school (dbn, name, num_takers, reading_score, math_score, writing_score, num_takers2, exam_taken2, exam_good2) -> Schools:
    school = Schools()
    school.dbn = dbn
    school.name = name
    school.num_takers = num_takers
    school.reading_score = reading_score
    school.math_score = math_score
    school.writing_score = writing_score
    school.num_takers2 = num_takers2
    school.exam_taken2 = exam_taken2
    school.exam_good2 = exam_good2

    school.save()



def add_exams(dbn, num_takers, reading_score, math_score, writing_score ) -> Schools:

    Schools.objects(dbn = dbn).update(num_takers = num_takers, reading_score = reading_score, math_score = math_score, writing_score = writing_score)


def get_schools_for_user(user_id: bson.ObjectId) -> List[Schools]:
    owner = Owner.objects(id=user_id).first()
    schools = Schools.objects(id__in=owner.School_ids).all()

    return list(schools)




def get_schools() -> List[Schools]:
    schools = Schools.objects().all()

    return list(schools)

def get_schools_sorted(my_type: str) -> List[Schools]:

    schools = Schools.objects.order_by( "+" + my_type ).limit(30)
    return list(schools)



# ======================================= District =============================================

def add_district_at (district, attendance, enrol) -> Att_by_Distr:
    at_d = Att_by_Distr()
    at_d.district = district
    at_d.attendance = attendance
    at_d.enrol = enrol

    at_d.save()


def get_districts() -> List[Att_by_Distr]:

    districts = Att_by_Distr.objects().all()

    return list(districts)


def get_districts_sorted(my_type: str) -> List[Att_by_Distr]:

    districts = Att_by_Distr.objects.order_by( "-" + my_type )
    return list(districts)

