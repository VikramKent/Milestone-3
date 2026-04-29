import datetime
class HashMap:
    def __init__(self, size = 8):
        """ Initializes the HashMap - Jack Barbuto """
        self._size = size
        self._length = 0
        self._buckets = [[] for _ in range(self._size)]
    
    def _hash(self, key):
        """Using Hash function - Jacn Barbuto"""
        return hash(key) % self._size
    
    def load_factor(self):
        return self._length / self._size
    
    def _rehash(self):
        """ Doubles the capacity and rehashes all entries  - Jack Barbuto."""
        old_buckets = self._buckets
        self._size *= 2
        self._buckets = [[] for _ in range(self._size)]
        self._length = 0
        
       
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def put(self, key, value):
        """Insert or update a key-value pair in the HashMap - Jack Barbuto"""
        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        
        bucket.append((key, value))
        self._length += 1
        
        
        if self.load_factor() >= 0.8:
            self._rehash()
    
    def get(self, key, default = None):
        """Retrieve a value by key - Jack Barbuto"""
        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return default
    
    def items(self):
        for bucket in self._buckets:
            for key, value in bucket:
                yield key, value

    def is_empty(self):
        """ Check if the HashMap is empty - Jack Barbuto"""
        return self._length == 0
    
    def __len__(self):
        """Return the Length - Jack Barbuto"""
        return self._length
    
    def __contains__(self, key):
        """Checks if key exists in the map - Jack Barbuto"""

        bucket = self._buckets[self._hash(key)]
        for k, _ in bucket:
            if k == key:
                return True
        return False

class Course:
    def __init__(self, course_code, credits, capacity):
        """Initializes the Course Class - Jack Barbuto"""
        self.course_code = course_code
        self.credits = credits
        self.students = []
        self.capacity = capacity
        self.enrolled_roster = []
        self.waitlist = LinkedQueue()
        self.prerequisites = HashMap()


    def __repr__(self):
        """Allows Course_Code to be Printable - Jack Barbuto"""
        return f"{self.course_code}"

    def add_student(self, student):
        """Adds Student to list of Students - Jack Barbuto"""
        self.students.append(student)
    
    def get_student_count(self):
        """Gets the Total count of Students - Jack Barbuto"""
        return len(self.students)
    
    def set_prerequisite(self, prerequisite_course_code, required_grade):
        """Sets a prerequisite and required grade for a course- Jack Barbuto"""
        self.prerequisites.put(prerequisite_course_code, required_grade)
    

    def _check_prerequisites(self, student):
        """Checks a prerequisite and required grade for a course- Jack Barbuto"""
        
        if self.prerequisites.is_empty():
            return True, None
        
        completed_courses = {course.course_code: grade for course, grade in student.courses.items()}
        
        
        for prereq_course, required_grade in self.prerequisites.items():
            if prereq_course not in completed_courses:
                return False, f"Student has not completed prerequisite: {prereq_course}"
            
            student_grade = completed_courses[prereq_course]
            
            # Define grade hierarchy for comparison
            GRADE_POINTS = {'A' : 4.0, 'A-' : 3.7,'B+': 3.3, 'B' : 3.0, 'B-' : 2.7,'C+': 2.3, 'C' : 2.0, 'C-' : 1.7,'D' : 1.0,'F' : 0.0}
            
            if student_grade not in GRADE_POINTS or required_grade not in GRADE_POINTS:
                return False, f"Invalid grade in prerequisite check for {prereq_course}"
            
            if GRADE_POINTS[student_grade] < GRADE_POINTS[required_grade]:
                return False, f"Student's grade ({student_grade}) in {prereq_course} is below required ({required_grade})"
        
        return True, None




    def request_enroll(self, student, enroll_date):
        """Checks if you can enroll in a class, enrolls or waitlists a student - Jack Barbuto"""
        for record in self.enrolled_roster:
            if record.student.student_id == student.student_id:
                return
            
        prereq_met, error_msg = self._check_prerequisites(student)
        if not prereq_met:
            raise ValueError(f"Cannot enroll student {student} in {self.course_code}: {error_msg}")    
            
        if len(self.enrolled_roster) < self.capacity:
            record = EnrollmentRecord(student, enroll_date)
            self.enrolled_roster.append(record)
            self.add_student(student)

        else:
            self.waitlist.enqueue(student)

    def drop(self, student_id, enroll_date_for_replacement=None):
        """Drops a student from a class adds a student from waitlist to take his spot - Jack Barbuto"""
        target_record = None
        for record in self.enrolled_roster:
            if record.student.student_id == student_id:
                target_record = record
                break
 
        if target_record is None:
            raise ValueError(f"Student with ID {student_id} is not enrolled in {self.course_code}")
 
        self.enrolled_roster.remove(target_record)
        self.students.remove(target_record.student)
 
       
        if not self.waitlist.is_empty():
            next_student = self.waitlist.dequeue()
            replacement_date = enroll_date_for_replacement or datetime.date.today()
            self.request_enroll(next_student, replacement_date)

    def sort_roster_by_id_merge(self):
        self.enrolled_roster = merge_sort(self.enrolled_roster, lambda record: record.student.student_id)
        return self.enrolled_roster

    def sort_roster_by_name_merge(self):
        self.enrolled_roster = merge_sort(self.enrolled_roster, lambda record: record.student.name)
        return self.enrolled_roster

    def sort_roster_by_date_merge(self):
        self.enrolled_roster = merge_sort(self.enrolled_roster, lambda record: record.enroll_date)
        return self.enrolled_roster

    def sort_roster_by_id_quick(self):
        self.enrolled_roster = quick_sort(self.enrolled_roster, lambda record: record.student.student_id)
        return self.enrolled_roster

    def sort_roster_by_name_quick(self):
        self.enrolled_roster = quick_sort(self.enrolled_roster, lambda record: record.student.name)
        return self.enrolled_roster

    def sort_roster_by_date_quick(self):
        self.enrolled_roster = quick_sort(self.enrolled_roster, lambda record: record.enroll_date)
        return self.enrolled_roster

class Student:
    def __init__(self, student_id, name):
        """Initializes the Student Class - Jack Barbuto"""
        self.student_id = student_id
        self.name = name
        self.courses = {}

    def __repr__(self):
        """Allows User to print a Students Name and ID - Jack Barbuto"""
        return f"{self.name} ({self.student_id})"

    def enroll(self, course, grade):
        """Takes a grade and a course for a student and stores it in a dictionary - Jack Barbuto"""
        self.courses[course] = grade
        course.add_student(self)

    def update_grade(self, course, grade):
        """Updates a grade for an exsiting course - Jack Barbuto"""
        self.courses[course] = grade

    def calculate_gpa(self):
        """Calculates GPA for a student goes through ever corse they took - Jack Barbuto""" 
        GRADE_POINTS = {'A' : 4.0, 'A-' : 3.7,'B+': 3.3, 'B' : 3.0, 'B-' : 2.7,'C+': 2.3, 'C' : 2.0, 'C-' : 1.7,'D' : 1.0,'F' : 0.0}
        total_points = 0
        total_credits = 0
        for course, grade in self.courses.items():
            for key in GRADE_POINTS:
                if key == grade:
                    total_points += GRADE_POINTS[grade] * course.credits
                    total_credits += course.credits
        if total_credits <= 0:
            return 0.0 
        elif total_points <= 0:
            return 0.0 
        else:
            return total_points / total_credits
                

    def get_courses(self):
        """allows user to view all courses a student took - Jack Barbuto"""     
        return list(self.courses.keys())


    def get_course_info(self):
        """allows user to view all courses, grades, and credits a student has taken - Jack Barbuto"""
        info = []
        for course, grade in self.courses.items():
            info.append({
                "course": course.course_code,
                "grade": grade,
                "credits": course.credits
            })
        return info
    
class EnrollmentRecord:

    def __init__(self, student: Student, enroll_date):
        """Initializes the Enrollment Record - Jack Barbuto"""
        
        """Makes Enroll_date Unified - Jack Barbuto"""
        if isinstance(enroll_date, datetime.date):
            self.enroll_date = enroll_date
        elif isinstance(enroll_date, str):
            self.enroll_date = datetime.date.fromisoformat(enroll_date)   
        else:
            raise TypeError("enroll_date must be a datetime.date or a YYYY-MM-DD string")
 
        self.student = student

class Node:
    def __init__(self, data):
        """Creates Node - Jack Barbuto"""
        self.data = data
        self.next = None
class LinkedQueue:
    def __init__(self):
        """Creates a Linked Queue - Jack Barbuto"""
        self._head = None   
        self._tail = None   
        self._length = 0
 
    def enqueue(self, item):
        """Adds an item to the queue - Jack Barbuto"""
        
        node = Node(item)
        if self._tail is None:         
            self._head = node
            self._tail = node
        
        else:
            self._tail.next = node
            self._tail = node
        
        self._length += 1
 
    
    def dequeue(self):
        """Remove and returns the front item of the queue - Jack Barbuto"""
        if self.is_empty():
            raise ValueError("LinkedQueue is empty")
        
        data = self._head.data
        self._head = self._head.next
        
        if self._head is None:          
            self._tail = None
        
        self._length -= 1
        return data
 
    def is_empty(self):
        """Checks if Linked Queue is empty - Jack Barbuto"""
        return self._length == 0
 
    
    def __len__(self):
        """Finds Lenght of the Linked Queue - Jack Barbuto"""
        return self._length
 
    
    def __repr__(self):
        items, node = [], self._head
        while node:
            items.append(repr(node.data))
            node = node.next
        return f"LinkedQueue([{', '.join(items)}])"

def merge_sort(items, key):
    if len(items) <= 1:
        return items

    middle = len(items) // 2
    left = merge_sort(items[:middle], key)
    right = merge_sort(items[middle:], key)

    sorted_items = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            sorted_items.append(left[i])
            i += 1
        else:
            sorted_items.append(right[j])
            j += 1

    sorted_items += left[i:]
    sorted_items += right[j:]

    return sorted_items


def quick_sort(items, key):
    if len(items) <= 1:
        return items

    pivot = items[0]
    small = []
    big = []

    for item in items[1:]:
        if key(item) <= key(pivot):
            small.append(item)
        else:
            big.append(item)

    return quick_sort(small, key) + [pivot] + quick_sort(big, key)

