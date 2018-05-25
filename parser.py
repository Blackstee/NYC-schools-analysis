import csv

import pandas
import numpy as np
import schools.data.Schools as Schools
import sys

import schools.services.data_service as svc


#getting data about NYC schools

def get_data():

    with open('./tables/ap_col.csv', encoding='utf-8') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:
            if svc.find_School_by_dbn(row['DBN']):
                print(row['DBN'], row['SchoolName'])
            else:
                svc.add_school(row['DBN'], row['SchoolName'], '0', '0', '0', '0', row['AP Test Takers '],
                               row['Total Exams Taken'], row['Number of Exams with scores 3 4 or 5'])
                print(row['DBN'], row['SchoolName'])





    with open('./tables/test_res.csv', encoding='utf-8') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            svc.add_exams(row['DBN'], row['Num of SAT Test Takers'], row["SAT Critical Reading Avg. Score"], row["SAT Math Avg. Score"], row["SAT Writing Avg. Score"])
            print(row['DBN'], row['SCHOOL NAME'])



#getting data about districts and attendance + enrollment of students

def get_data_distr():

    with open('./tables/attend.csv', encoding='utf-8') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            svc.add_district_at(row['District'], row['YTD % Attendance (Avg)'], row['YTD Enrollment(Avg)'])
