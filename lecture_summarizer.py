import requests
import argparse
from typing import Dict, List
from abc import abstractmethod
import json


class RequestProcessor(object):

    def __init__(self, args):
        self.args = args
        self.base_url = 'http://%s' % args.base_path

    def validate_args_all_of(self, required_items: List[str]):
        missing_args = [item for item in required_items if getattr(self.args, item) is None]
        if len(missing_args) > 0:
            raise RuntimeError('There were missing arguments for this command: ', ' '.join(missing_args))

    def validate_args_any_of(self, item_list: List[str]):
        if not any(getattr(self.args, x) is not None for x in item_list):
            raise RuntimeError("Need at least one item in list: %s" % ','.join(item_list))

    def run_post(self, url, body):
        req = requests.post(url, json.dumps(body), headers = {
            'Content-Type': 'application/json'
        })
        if req.status_code > 200:
            raise RuntimeError(req.json())
        print(req.json())

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        self.run()


class CreateLecture(RequestProcessor):

    def __init__(self, args):
        super(CreateLecture, self).__init__(args)

    def __get_lecture_content(self):
        with open(self.args.path) as d:
            all_data = d.read()
        url = self.base_url + '/udacity'

        req = requests.post(url, all_data)
        if req.status_code > 200:
            raise RuntimeError("Invalid request to service with file given")
        return req.json()['paragraph']

    def __create_body(self, to_upload):
        return {
            'course': self.args.course,
            'name': self.args.name,
            'content': to_upload
        }

    def run(self):
        self.validate_args_all_of(['path', 'course', 'name'])
        to_upload = self.__get_lecture_content()
        body = self.__create_body(to_upload)
        url = self.base_url + '/lectures'
        req = requests.post(url, json.dumps(body), headers = {
            'Content-Type': 'application/json'
        })
        if req.status_code > 200:
            raise RuntimeError(req.json())
        print(req.json())


class GetLectures(RequestProcessor):

    def __init__(self, args):
        super(GetLectures, self).__init__(args)

    def __build_params(self):
        start = '?'
        arg_list = [self.args.course, self.args.name]
        for arg in arg_list:
            if arg:
                start += '&' + arg if start != '?' else arg
        return start if start != '?' else ''

    def __build_url(self):
        if self.args.lecture_id:
            return '/%s' % self.args.lecture_id
        return self.__build_params()

    def run(self):
        url = self.base_url + '/lectures'
        url += self.__build_url()
        req = requests.get(url, headers = {
            'Content-Type': 'application/json'
        })
        if req.status_code > 200:
            raise RuntimeError(req.json())
        print(req.json())


class CreateSummary(RequestProcessor):

    def __init__(self, args):
        super(CreateSummary, self).__init__(args)

    def __build_body(self):
        return {
            'name': self.args.name,
            'course': self.args.course
        }

    def run(self):
        self.validate_args_all_of(['lecture_id', 'name', 'ratio'])
        body = self.__build_body()
        url = '%s/lectures/%s/summaries' % (self.base_url, self.args.lecture_id)
        self.run_post(url, body)


class GetSummaries(RequestProcessor):

    def __init__(self, args):
        super(GetSummaries, self).__init__(args)

    def run(self):
        pass


class DeleteSummary(RequestProcessor):

    def __init__(self, args):
        super(DeleteSummary, self).__init__(args)

    def run(self):
        pass


factory = {
    'create-lecture': CreateLecture,
    'get-lectures': GetLectures,
    'create-summary': CreateSummary,
    'get-summaries': GetSummaries,
    'delete-summary': DeleteSummary
}


def run():
    parser = argparse.ArgumentParser(description='Process and summarize lectures')
    parser.add_argument('action')
    parser.add_argument('-path', dest='path', default=None, help='File path of lecture')
    parser.add_argument('-course', dest='course', default=None, help='')
    parser.add_argument('-name', dest='name', default=None, help='')
    parser.add_argument('-lecture-id', dest='lecture_id', default=None, help='')
    parser.add_argument('-ratio', dest='path', help='', default=None)
    parser.add_argument('-summary-id', dest='summary_id', default=None, help='')
    parser.add_argument('-base-path', dest='base_path', default='34.234.211.212:5000', help='')

    args = parser.parse_args()

    factory[args.action](args)()


if __name__ == '__main__':
    run()
