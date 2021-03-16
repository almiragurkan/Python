#Almira Gürkan

class Student(object):

    def __init__(self, name, last_name, student_id):
        self.name = name
        self.last_name = last_name
        self.__id = student_id
        self.university = None

    def get_id(self):
        return self.__id

class University(object):
    def __init__(self, uni_id, name, base_points, capacity):
        self.students = []
        self.id = uni_id
        self.name = name
        self.base_points = base_points
        self.capacity = capacity


class Answer(object):
    def __calc_mark(self, key):
        incorrect = 0
        for i in range(len(key)):
            if self.answers[i] == key[i]:
                self.total_correct += 1
                self.deducted_correct += 1
            elif self.answers[i] == '-':
                self.total_blank += 1
                continue
            else:
                incorrect += 1
                self.total_incorrect += 1
                if incorrect == 4:
                    incorrect = 0
                    self.deducted_correct -= 1
        self.__score = self.deducted_correct * 15

    def get_score(self, a_key=None, b_key=None):
        if self.__score == -1:
            if self.book_type == 'A':
                self.__calc_mark(a_key)
            else:
                self.__calc_mark(b_key)
        return self.__score

    def __init__(self, book_type, answers, university_choices):
        self.book_type = book_type
        self.answers = answers
        self.university_choices = university_choices
        self.__score = -1
        self.total_correct = 0
        self.deducted_correct = 0
        self.total_blank = 0
        self.total_incorrect = 0


def read_keys(file):

    key_file = open(file, 'r')
    key_lines = key_file.read().splitlines()

    key_file.close()

    a_keys = key_lines[0]
    b_keys = key_lines[1]
    return a_keys, b_keys


def read_universities(file):
    # array of universities
    universities = []
    universities_file = open(file, 'r')

    for line in universities_file:
        values = line.split(',')
        universities.append(University(values[0], values[1], int(values[2]), int(values[3])))

    return universities


def read_students(file):
    # array of students
    students = []
    students_file = open(file, 'r')

    for line in students_file:
        values = line.split()
        students.append(Student(values[1], values[2], values[0]))
    return students


def read_answers(file):
    answers = {}
    answers_file = open(file, 'r')

    for line in answers_file:
        values = line.split()
        answers[values[0]] = Answer(values[1], values[2], values[3:])
    return answers


def get_input():
    print('- ' * 30)
    print('(1) Search for a student with a given id and display his/her name and last name')
    print('(2) List the university/universities and departments with a maximum base points')
    print('(3) Create a file named \'results.txt\' for each student')
    print('(4) List the student information sorted by their score')
    print('(5) List the students placed in every university/department')
    print('(6) List the students who were not able to be placed anywhere')
    print('(7) List all the departments')
    print('- ' * 30)
    return input('Your choice: ')


def search_student_name(students):
    student_id = input('Enter the ID of the student: ')
    for student in students:
        if student.get_id() == student_id:
            print(student.name + ' ' + student.last_name)
            return
    print('Student not found')


def universitiies_with_max_base_points(universities):
    def key_for_sort(u):
        return u.base_points

    for university in sorted(universities, key=key_for_sort, reverse=True):
        print(university.name + ', ' + str(university.base_points))


def create_file(students, answers, fileName):
    file = open(fileName, 'w')
    file.write('ID, Name, Last Name, Book Type, Score, Correct Answers, Incorrect Answers, Blank Answers, Deducted Answers, School\n')

    for student in students:
        answer = answers[student.get_id()]
        if student.university is None:
            uni_name = "No University"
        else:
            uni_name = student.university.name
        file.write(student.get_id() + ', ' + student.name + ' ' + student.last_name + ', ' + answer.book_type + ', ' + str(answer.get_score())
                   + ', ' + str(answer.total_correct) + ', ' + str(answer.total_incorrect) + ', ' + str(answer.total_blank)
                   + ', ' + str(answer.deducted_correct) + ', ' + uni_name + "\n")
    print("File", fileName, "is created")


def list_students(students, answers):
    for student in students:
        answer = answers[student.get_id()]
        print(student.get_id() + ',', student.name + ' ' + student.last_name + ',', answer.get_score())


def list_universities_with_students(universities, answers):
    for univesity in universities:
        print(univesity.name + ':')
        print('- ' * 30)
        count=1
        for student in univesity.students:
            answer = answers[student.get_id()]
            print(count, ') ' + student.get_id() + ',', student.name + ' ' + student.last_name + ',', answer.get_score())
            count = count + 1
        print()


def list_unplaced_students(students, answers):
    for student in students:
        if student.university is not None:
            continue
        answer = answers[student.get_id()]
        print(student.get_id() + ',', student.name + ' ' + student.last_name + ',', answer.get_score())


def list_departments(universities):
    for university in universities:
        print(university.name)


def main():
    #reading keys from key.txt
    a_key, b_key = read_keys('key.txt')

    #reading universities
    universities = read_universities('university.txt')

    #reading students
    students = read_students('student.txt')

    #reading answers
    answers = read_answers('answers.txt')


    def get_score_for_sort(st):
        ans = answers[st.get_id()]
        return ans.get_score(a_key, b_key)

    students.sort(key=get_score_for_sort, reverse=True)

    # add students to universities, highest scores first
    for student in students:
        answer = answers[student.get_id()]
        for uni in universities:
            finished_choice_loop = False
            for university_choice in answer.university_choices:
                if uni.id == university_choice and uni.capacity > len(uni.students) and uni.base_points <= answer.get_score(a_key, b_key):
                    uni.students.append(student)
                    student.university = uni
                    finished_choice_loop=True
                    break
            if finished_choice_loop:
                break

    while True:
        q = get_input()
        if q == '1':
            search_student_name(students)
        elif q == '2':
            universitiies_with_max_base_points(universities)
        elif q == '3':
            create_file(students, answers, 'result.txt')
        elif q == '4':
            list_students(students, answers)
        elif q == '5':
            list_universities_with_students(universities, answers)
        elif q == '6':
            list_unplaced_students(students, answers)
        elif q == '7':
            list_departments(universities)
        else:
            print("Wrong input")

        cont = input('\nDo you want to continue (y)es or (n)o: ')
        if cont.lower() != 'y':
            break


main()
