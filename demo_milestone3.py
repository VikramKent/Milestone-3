from models import *

c = Course("CSE2000", 3, 1)
c.set_prerequisite("CSE1000", "C")

s1 = Student(1, "Alice")
s2 = Student(2, "Bob")

prereq = Course("CSE1000", 3, 10)
s1.enroll(prereq, "B")

c.request_enroll(s1, "2026-01-01")
try:
    c.request_enroll(s2, "2026-01-02")
except ValueError as e:
    print(e)
print(c.enrolled_roster)