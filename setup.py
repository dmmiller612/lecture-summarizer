from setuptools import setup

project = dict(
    name='lecture-summarizer',
    version='0.0.1',
    install_requires=[
        'requests',
    ],
    py_modules=['lecture_summarizer'],
    entry_points={
        'console_scripts': [
            'lecture-summarizer=lecture_summarizer:run'
        ]
    }
)

classifiers = ""
# Beyond this point, code is not project-specific
import io
import os
import re
import sys

try:
    from setuptools import setup
except ImportError as exc:
    raise RuntimeError("Cannot install '{0}', setuptools is missing ({1})"
                       .format(project['name'], exc))

project_root = os.path.abspath(os.path.dirname(__file__))
script_name = os.path.join(project_root, project['py_modules'][0] + '.py')
expected_keys = "version author author_email".split()
with io.open(script_name, encoding='utf-8') as handle:
    for line in handle:
        match = re.match(r"""^__({})__ += (?P<q>['"])(.+?)(?P=q)$"""
                         .format('|'.join(expected_keys)), line)
        if match:
            project[match.group(1)] = match.group(3)

project.update(dict(
    description=__doc__.split('.')[0].split(' - ', 1)[1].strip(),
    long_description=(io.open('README.rst', encoding='UTF-8').read()
                      .split('\n.. _setup-start:', 1)[-1].strip()),
    classifiers=[i.strip()
                 for i in classifiers.splitlines()
                 if i.strip() and not i.strip().startswith('#')],
    keywords=project['keywords'].replace(',', ' ').strip().split(),
))

# Ensure 'setup.py' is importable by other tools, to access the project's metadata
__all__ = ['project', 'project_root']
if __name__ == '__main__':
    if '--metadata' in sys.argv[:2]:
        import json
        json.dump(project, sys.stdout, default=repr, indent=4, sort_keys=True)
        sys.stdout.write('\n')
    else:
        setup(**project)
