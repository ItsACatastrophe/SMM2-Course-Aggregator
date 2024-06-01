import io
import unittest

from aggregator import course


class TestObject(unittest.TestCase):
    def setUp(self):
        self.object = course.Object()
        self.id = 34
        self.bit_str = "00000110000000000000000000000100"
        self.flag = b"00000110000000000000000000000100"
        course.set_wanted_object(self.id, self.bit_str)

    def test_is_wanted_placed(self):
        self.object.set_id(self.id)

        self.object.set_flags(int(self.flag))

        self.assertTrue(self.object.is_wanted())

    def test_is_wanted_contained(self):
        self.object.set_child_id(self.id)

        self.object.set_child_flags(int(self.flag))

        for container_id in course.wanted_flag_bit_positions:
            with self.subTest(container_id=container_id):
                self.object.set_id(container_id)
                self.assertTrue(self.object.is_wanted())

    def test_unknown_wanted_container(self):
        self.object.set_id(-1)  # An unexpected container holds our object

        self.object.set_child_flags(int(self.flag))

        self.assertFalse(self.object.is_wanted())


# Course module end to end/integration testing
class TestCourse(unittest.TestCase):
    decrypted_course_fixtures = [
        "./test/fixtures/decrypted-B4170JNDG",
        "./test/fixtures/decrypted-RJ7C12HNF",
    ]
    object_id = 34
    flag_bits = "00000110000000000000000000000100"

    # TODO: reduce nesting without copy pasting?
    def test_course_init(self):
        difficulty = "e"
        course_id = "FOOBARBAZ"

        for fixture in self.decrypted_course_fixtures:
            with self.subTest(fixture=fixture):
                with open(fixture, "rb") as course_data:
                    test_course = course.Course(
                        course_data,
                        difficulty,
                        course_id,
                        self.object_id,
                        self.flag_bits,
                    )

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

        self.assertEqual(course.seek_get(data, 0, 1), b"f")
        self.assertEqual(course.seek_get(data, 2, 1), b"o")
        self.assertEqual(course.seek_get(data, 1, 2), b"oo")
