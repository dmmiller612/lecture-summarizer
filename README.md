# lecture-summarizer

This project utilizes the BERT model to perform extractive text summarization on lecture transcripts. The contents of 
this project include a RESTful API to serve these summaries, and a command line interface for easier interaction. You can 
find more about the specs of this service and CLI in our `Documentation` directory.

Paper: https://arxiv.org/abs/1906.04165

## Running the service locally
First, docker is required to run the service locally. To start the service, run the command:
```bash
make docker-build-run
```
On the first run of a service, this may take quite some time to complete.


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
the `-base_path` option, such as `-base_path localhost:5000`. As an example, to get lectures locally, you could run: 

```bash
lecture-summarizer get-lectures -base-path localhost:5000
``` 


## How to use CLI tool

After installing the CLI, the service should be ready to use. The lecture-summarizer uses the API service as 
it's backend. This backend defaults to the currently hosted one on AWS. The user can supply a specific URL if the 
service is hosted elsewhere. Below, briefly discusses how to use the CLI tool.

### Creating a Lecture

Before one can do anything with summarizations, there needs to be at least one lecture in the system. Taking an Udacity 
lecture, using the `raw_lecture.txt` file at the parent of the lecture-summarizer directory as an example, one can upload 
the content issuing the following command:

```bash
lecture-summarizer create-lecture -path ./raw_lecture.txt -name example_first_lecture -course IHI
```

Currently, the lecture-summarizer can parse sdp file formats, which are common for Udacity-based lectures. Notice that one 
needs to supply a `name` and a `course` as metadata.

### Retrieving Lectures

One can retrieve lectures with a couple of options. Those options can be found in the Documentation/CLI_Documentation.md 
file in the base of the repo. Some example commands are shown below:

##### Get a Single Lecture
```bash
lecture-summarizer get-lectures -lecture-id 1
```

##### Get All  Lectures
```bash
lecture-summarizer get-lectures
```

##### Get Lectures by Name
```bash
lecture-summarizer get-lectures -name example_first_lecture
```

##### Get Lectures by Course
```bash
lecture-summarizer get-lectures -course ihi
```

### Creating a Summary

Just like creating a lecture, creating a summary is a painless process. Below is an example of creating a summary from 
a specified lecture.

```bash
lecture-summarizer create-summary -lecture-id 1 -name 'my summary name' -ratio 0.2
``` 

The `ratio` specifies approximately how much of the lecture that you want to summarize.

### Retrieving Summaries

Just like with retrieving lectures, one can also list summaries. Below are a couple of examples:

##### Get a Single Summary
```bash
lecture-summarizer get-summaries -lecture-id 1 -summary-id 1
```

##### Get All Summaries
```bash
lecture-summarizer get-summaries -lecture-id 1
```

##### Get All Summaries by Name
```bash
lecture-summarizer get-summaries -lecture-id 1 -name 'my summary name'
```

##### Delete a Summary
```bash
lecture-summarizer delete-summary -lecture-id 1 -summary-id 1
```

## RESTful API Docs

##### POST /lectures

This endpoint creates a lecture.

```json
{
  "course": "course identifier",
  "content": "Lecture String Content",
  "name": "Lecture name"
}
``` 

##### GET /lectures

This endpoint is used to retrieve lectures. The user can supply two query params shown below.
```
/lectures?course=unique_identifier
/lectures?name=course_name
```

##### GET /lectures/{id}

This endpoint is used to retrieve a single lecture
```
/lectures/{id}
```

##### POST /lectures/{id}/summaries

This endpoint is used to create a summarization from a lecture
```json
{
  "name": "Summarization name",
  "ratio": "Ratio of sentences to select"
}
```

##### GET /lectures/{id}/summaries
```
/lectures/{id}/summaries?name=course_name
/lectures/{id}/summaries
```

##### GET/DELETE /lectures/{id}/summaries/{summarization_id} 

This endpoint allows you to get or delete a summarization.
```
/lectures/{id}/summaries/{summarization_id} 
```
