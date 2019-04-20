# CLI Documentation

| Command                           | Options                                                                                                                                | Description                                                                                                  |
|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| lecture-summarizer create-lecture | -path Local path to lecture -course Specify the course in which the lecture belongs -name Name of the lecture                          | This uploads a lecture from files on the user's local machine.                                               |
| lecture-summarizer get-lectures   | -course specified course (optional) -name Name of the lecture(optional) -lecture_id (optional)                                         | Based on the supplied options, this will either retrieve all lectures or specific ones based on the request. |
| lecture-summarizer create-summary | -lecture-id -name -ratio                                                                                                               | This will create a summary for a  given lecture.                                                             |
| lecture-summarizer get-summaries  | -lecture-id -name -summary-id                                                                                                          | This will retrieve all summaries  for a given lecture or requested ones through the options.                 |
| lecture-summarizer delete-summary | -lecture-id -summary-id                                                                                                                | This will delete the summary.                                                                                |


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


## How to use CLI tool

After installing the CLI, the service should be ready to use. The lecture-summarizer uses the API service as 
it's backend. This backend defaults to the currently hosted one on AWS. The user can supply a specific URL if the 
service is hosted elsewhere. Below, briefly discusses how to use the CLI tool.

### Creating a Lecture

Before one can do anything with summarizations, there needs to be at least one lecture in the system. Taking an Udacity 
lecture, using the `raw_lecture.txt` file at the parent of the lecture-summarizer directory as an example, one can upload 
the content issuing the following command:

```bash
lecture-summarizer create-summary -path ./raw_lecture.txt -name example_first_lecture -course IHI
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
lecture-summarizer get-lectures -lecture-id 1
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
