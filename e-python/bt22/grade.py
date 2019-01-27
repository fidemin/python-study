from collections import namedtuple

Grade = namedtuple('Grade', ('score', 'weight'))

class SimpleGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)


class BySubjectGradeBook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, score):
        grades = self._grades[name]
        grades_by_subject = grades.setdefault(subject, [])
        grades_by_subject.append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        total_count = 0
        total_score = 0

        for scores_by_subject in grades.values():
            total_count += len(scores_by_subject)
            total_score += sum(scores_by_subject)

        return total_score / total_count


class WeightedGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, score, weight):
        grades = self._grades[name]
        grades_by_subject = grades.setdefault(subject, [])
        grades_by_subject.append((score, weight))

    def average_grade(self, name):
        grades = self._grades[name]
        total_count = 0
        total_avgs = 0

        for scores_by_subject in grades.values():
            sbj_sum = 0
            sbj_weight = 0
            for score, weight in scores_by_subject:
                sbj_sum += score * weight
                sbj_weight += weight

            total_avgs += sbj_sum / sbj_weight
            total_count += 1 

        return total_avgs / total_count


class Gradebook(object):
    def __init__(self):
        self._students = {}


    def student(self, name):
        return self._students.setdefault(name, Student(name))


class Student(object):
    def __init__(self, name):
        self._name = name
        self._subjects = {}

    def subject(self, subject_name):
        return self._subjects.setdefault(subject_name, Subject(subject_name))


    def average_grade(self):
        total_avgs = 0
        total_count = 0
        for subject in self._subjects.values():
            total_avgs += subject.average_grade()
            total_count += 1

        return total_avgs / total_count


class Subject(object):
    def __init__(self, subject):
        self._subject = subject
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total_sum = 0
        total_weight = 0
        for grade in self._grades:
            total_sum += grade.score * grade.weight
            total_weight += grade.weight

        return total_sum / total_weight


if __name__ == "__main__":
    book = SimpleGradebook()
    book.add_student('Yunhong')
    book.report_grade('Yunhong', 10)

    print(book.average_grade('Yunhong'))

    book = BySubjectGradeBook()
    book.add_student('Yun')
    book.report_grade('Yun', 'Math', 75)
    book.report_grade('Yun', 'Math', 65)
    book.report_grade('Yun', 'Gym', 90)
    book.report_grade('Yun', 'Gym', 95)


    print(book.average_grade('Yun'))


    book = WeightedGradebook()
    book.add_student('Yun')
    book.report_grade('Yun', 'Math', 75, 0.1)
    book.report_grade('Yun', 'Math', 65, 0.9)
    book.report_grade('Yun', 'Gym', 90, 0.5)
    book.report_grade('Yun', 'Gym', 95, 0.5)

    
    print(book.average_grade('Yun'))

    book = Gradebook()
    student1 = book.student('Yunhong')
    math = student1.subject('Math')
    math.report_grade(75, 0.1)
    math.report_grade(65, 0.9)
    gym = student1.subject('Gym')
    gym.report_grade(90, 0.5)
    gym.report_grade(95, 0.5)

    print(student1.average_grade())

