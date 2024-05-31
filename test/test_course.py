import io
import unittest

from aggregator import course


class TestObject(unittest.TestCase):
    def setUp(self):
        self.object = course.Object()

    def test_is_superball_placed(self):
        self.object.set_id(34)

        flag = b"00000110000000000000000000000100"
        self.object.set_flags(int(flag))

        self.assertTrue(self.object.is_superball())

    def test_is_superball_contained(self):
        self.object.set_child_id(34)

        flag = b"00000110000000000000000000000100"
        self.object.set_child_flags(int(flag))

        for container_id in self.object.SUPERBALL_CONTAINER_IDS:
            self.object.set_id(container_id)
            self.assertTrue(self.object.is_superball())

    def test_unknown_superball_container(self):
        self.object.set_id(-1)

        flag = b"00000110000000000000000000000100"
        self.object.set_child_flags(int(flag))

        self.assertFalse(self.object.is_superball())


# Course module end to end testing
class TestCourse(unittest.TestCase):
    decrypted_level_fixtures = [
        "./test/fixtures/decrypted-B4170JNDG",
        "./test/fixtures/decrypted-RJ7C12HNF",
    ]

    # TODO: reduce nesting without copy pasting?
    def test_course_init(self):
        difficulty = "e"
        course_id = "FOOBARBAZ"

        for fixture in self.decrypted_level_fixtures:
            with self.subTest(fixture=fixture):
                with open(fixture, "rb") as course_data:
                    test_course = course.Course(course_data, difficulty, course_id)

                    course_data = test_course.get_course_data()

                    self.assertIs(course_data.pop("played"), 0)

                    for course_value in course_data.values():
                        self.assertTrue(
                            course_value
                        )  # Truthy to check if value is defined

                    objects = [
                        *test_course.area_main.objects,
                        *test_course.area_sub.objects,
                    ]

                    for obj in objects:
                        object_data = obj.get_object_summary()
                        for obj_value in object_data:
                            self.assertIsNot(obj_value, None)


class TestHelpers(unittest.TestCase):
    def test_seek_get(self):
        data = io.BytesIO(b"foo")

        bit1 = course.seek_get(data, 0, 1)
        bit2 = course.seek_get(data, 2, 1)
        bits = course.seek_get(data, 1, 2)

        self.assertEqual(bit1, b"f")
        self.assertEqual(bit2, b"o")
        self.assertEqual(bits, b"oo")
