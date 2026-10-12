"""Coordinates the Student Marks application."""
from validation import validate_mark, INVALID_MARK_MESSAGE
from calculations import calculate_total, calculate_average, calculate_grade
from display import display_result

SUBJECT_COUNT = 3


def read_mark(subject_number):
    return float(input(f"Enter marks for subject {subject_number}: "))


def read_marks():
    marks = []
    for i in range(SUBJECT_COUNT):
        mark = read_mark(i + 1)
        while not validate_mark(mark):
            print(INVALID_MARK_MESSAGE)
            mark = read_mark(i + 1)
        marks.append(mark)
    return marks


def main():
    name = input("Enter student name: ")
    marks = read_marks()

    total = calculate_total(marks)
    average = calculate_average(marks)
    grade = calculate_grade(average)

    display_result(name, total, average, grade)


if __name__ == "__main__":
    main()
