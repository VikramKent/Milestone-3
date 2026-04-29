import unittest
from models import *
# This file contains unit tests for milestone 3. You can run this file to test your implementation of the HashMap, Course, Student, merge_sort, and quick_sort. - Vikram Kent
class TestMilestone3(unittest.TestCase):

    def test_hashmap(self):
        h = HashMap()
        h.put("a", 1)
        self.assertEqual(h.get("a"), 1)

    def test_rehash(self):
        h = HashMap(2)
        h.put("a", 1)
        h.put("b", 2)
        h.put("c", 3)
        self.assertEqual(len(h), 3)

    def test_collision(self):
        h = HashMap(1)
        h.put("a", 1)
        h.put("b", 2)
        self.assertEqual(h.get("a"), 1)
        self.assertEqual(h.get("b"), 2)

    def test_prereq_fail(self):
        c = Course("CSE2000", 3, 10)
        c.set_prerequisite("CSE1000", "C")

        s = Student(1, "Bob")

        with self.assertRaises(ValueError):
            c.request_enroll(s, "2026-01-01")

    def test_prereq_pass(self):
        c = Course("CSE2000", 3, 10)
        c.set_prerequisite("CSE1000", "C")

        s = Student(1, "Bob")
        prereq = Course("CSE1000", 3, 10)
        s.enroll(prereq, "B")

        c.request_enroll(s, "2026-01-01")
        self.assertEqual(len(c.enrolled_roster), 1)

    def test_sort(self):
        c = Course("CSE2000", 3, 10)

        s1 = Student(3, "Charlie")
        s2 = Student(1, "Alice")
        s3 = Student(2, "Bob")

        c.request_enroll(s1, "2026-01-03")
        c.request_enroll(s2, "2026-01-01")
        c.request_enroll(s3, "2026-01-02")

        sorted_merge = c.sort_roster_by_id_merge()
        self.assertEqual([r.student.student_id for r in sorted_merge], [1,2,3])
        
        sorted_quick = c.sort_roster_by_id_quick()
        self.assertEqual([r.student.student_id for r in sorted_quick], [1,2,3])


if __name__ == "__main__":
    unittest.main()