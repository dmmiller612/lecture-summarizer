# lecture-summarizer

This project utilizes the BERT model to perform extractive text summarization on lecture transcripts. The contents of 
this project include a RESTful API to serve these summaries, and a command line interface for easier interaction. You can 
find more about the specs of this service and CLI in our documentation directory.


## Installation of CLI

The CLI tool can be downloaded using pip with the following command:

```bash
pip install git+https://github.com/dmmiller612/lecture-summarizer.git
```

To test the tool, try getting the current lectures in the service with the command: 
```bash
lecture-summarizer get-lectures
```

Note, that this tool automatically uses our cloud based service by default. You can use your local service by supplying 
the `-base_path` option, such as `-base_path localhost:5000`.
