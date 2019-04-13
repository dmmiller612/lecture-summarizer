from setuptools import setup

setup(
    name='lecture-summarizer',
    version='0.0.1',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'lecture-summarizer=lecture_summarizer:run'
        ]
    }
)