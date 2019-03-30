import unittest
import sys, os

testdir = os.path.dirname(__file__)
srcdir = '../summarizer'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from summarizer.LectureService import LectureService
from summarizer.SummarizationService import SummarizationService


class LectureServiceTest(unittest.TestCase):

    def test_lecture_creation(self):
        lecture_service = LectureService(memory_only=True)
        initial_result = lecture_service.create_lecture({
            "name": "random lecture",
            "course": "random course",
            "content": "This is random content."
        })

        self.assertIsNotNone(initial_result)

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
        self.assertIsNotNone(res)


class SummarizationServiceTest(unittest.TestCase):

    summarization_service = SummarizationService(use_memory=True)

    PASSAGE = '''
    The Chrysler Building, the famous art deco New York skyscraper, will be sold for a small fraction of its previous sales price.
    The deal, first reported by The Real Deal, was for $150 million, according to a source familiar with the deal.
    Mubadala, an Abu Dhabi investment fund, purchased 90% of the building for $800 million in 2008.
    Real estate firm Tishman Speyer had owned the other 10%.
    The buyer is RFR Holding, a New York real estate company.
    Officials with Tishman and RFR did not immediately respond to a request for comments.
    It's unclear when the deal will close.
    The building sold fairly quickly after being publicly placed on the market only two months ago.
    The sale was handled by CBRE Group.
    The incentive to sell the building at such a huge loss was due to the soaring rent the owners pay to Cooper Union, a New York college, for the land under the building.
    The rent is rising from $7.75 million last year to $32.5 million this year to $41 million in 2028.
    Meantime, rents in the building itself are not rising nearly that fast.
    While the building is an iconic landmark in the New York skyline, it is competing against newer office towers with large floor-to-ceiling windows and all the modern amenities.
    Still the building is among the best known in the city, even to people who have never been to New York.
    It is famous for its triangle-shaped, vaulted windows worked into the stylized crown, along with its distinctive eagle gargoyles near the top.
    It has been featured prominently in many films, including Men in Black 3, Spider-Man, Armageddon, Two Weeks Notice and Independence Day.
    The previous sale took place just before the 2008 financial meltdown led to a plunge in real estate prices.
    Still there have been a number of high profile skyscrapers purchased for top dollar in recent years, including the Waldorf Astoria hotel, which Chinese firm Anbang Insurance purchased in 2016 for nearly $2 billion, and the Willis Tower in Chicago, which was formerly known as Sears Tower, once the world's tallest.
    Blackstone Group (BX) bought it for $1.3 billion 2015.
    The Chrysler Building was the headquarters of the American automaker until 1953, but it was named for and owned by Chrysler chief Walter Chrysler, not the company itself.
    Walter Chrysler had set out to build the tallest building in the world, a competition at that time with another Manhattan skyscraper under construction at 40 Wall Street at the south end of Manhattan. He kept secret the plans for the spire that would grace the top of the building, building it inside the structure and out of view of the public until 40 Wall Street was complete.
    Once the competitor could rise no higher, the spire of the Chrysler building was raised into view, giving it the title.
    '''

    def test_summary_creation(self):
        created_summary = self.__create_summary()
        self.assertEqual(created_summary['name'], 'cool summary')
        self.assertEqual(created_summary['ratio'], 0.2)
        self.assertEqual(len([x for x in created_summary['content'].split('.') if x != '']), 4)

    def test_get_summary(self):
        created_summary = self.__create_summary()
        result = self.summarization_service.get_summary(created_summary['lecture'], created_summary['id'])
        self.assertEqual(result['name'], 'cool summary')
        self.assertEqual(result['ratio'], 0.2)
        self.assertEqual(len([x for x in result['content'].split('.') if x != '']), 4)

    def test_delete_summary(self):
        created_summary = self.__create_summary()
        result = self.summarization_service.delete_summary(created_summary['id'])
        attempt = self.summarization_service.get_summary(created_summary['lecture'], result['id'])
        self.assertEqual(attempt, {})

    def __create_summary(self):
        item = self.summarization_service.lecture_service.create_lecture({
            "name": "random lecture",
            "course": "random_course",
            "content": self.PASSAGE
        })
        lid: int = item['id']

        summary_request = {
            'name': 'cool summary',
            'ratio': 0.2
        }
        created_summary = self.summarization_service.create_summary(lid, summary_request)
        return created_summary



if __name__ == '__main__':
    unittest.main()