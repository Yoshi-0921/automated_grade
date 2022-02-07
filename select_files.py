import glob
import os
from students_list import STUDENTS
import shutil

def select_files(root):
    all_students = glob.glob(f'{root}/*')
    submission = []

    for student in all_students:
        if ".csv" in student:
            continue

        if student[len(root)+1:len(root)+9] in STUDENTS:
            os.rename(student, student[:len(root)+9])
            submission.append(student[len(root)+1:len(root)+9])
        else:
            shutil.rmtree(student)

    no_submission = set(STUDENTS) - set(submission)
    for student in no_submission:
        os.mkdir(root + "/" + student)
    print(f"Students who may not submit the assignment: {no_submission}")
