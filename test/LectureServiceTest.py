import unittest
import sys, os

testdir = os.path.dirname(__file__)
srcdir = '../summarizer'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from summarizer.LectureService import LectureService


class LectureServiceTest(unittest.TestCase):

    def test_lecture_creation(self):
        lecture_service = LectureService(memory_only=True)
        initial_result = lecture_service.create_lecture({
            "name": "random lecture",
            "course": "random course",
            "content": "This is random content."
        })

        self.assertEqual(initial_result, {'id': 1})

    def test_lecture_retrieval(self):
        lecture_service = LectureService(memory_only=True)
        initial = lecture_service.create_lecture({
            "name": "random lecture",
            "course": "random course",
            "content": "This is random content."
        })
        retrieved = lecture_service.get_lecture(initial['id'])
        self.assertEqual(retrieved['name'], 'random lecture')
        self.assertEqual(retrieved['course'], 'random course')

    def test_lecture_delete(self):
        lecture_service = LectureService(memory_only=True)
        initial_result = lecture_service.create_lecture({
            "name": "random lecture",
            "course": "random course",
            "content": "This is random content."
        })
        res = lecture_service.delete_lecture(initial_result['id'])
        self.assertEqual(res, {'id': 2})


if __name__ == '__main__':
    unittest.main()