# API Documentation

In this document, we will explain in the initial layout of the REST Api for lecture summarization.

| PATH                                             | Request Action | Description                                                                          | Request or Query Params                                     |
|--------------------------------------------------|----------------|--------------------------------------------------------------------------------------|-------------------------------------------------------------|
| /lectures                                        | POST           | The user can upload  lecture content, which can then be utilized for summarization. | Params: course, content, name                               |
| /lectures                                        | GET            | Get all uploaded lectures.                                                           | Query Params: course, name                                  |
| /lectures/{id}                                   | GET            | Retrieve a lecture.                                                                  | Query Params: None                                          |
| /lectures/{id}/summarizations                    | POST/GET       | Create a summarization or  GET all summarizations for a given lecture.               | Params: name, ratio, Query Params: custom_tag |
| /lectures/{id}/summarizations/{summarization_id} | GET/DELETE     | Get or delete a summarized lecture.                                                  | None                                                        |


## POST /lectures

This endpoint creates a lecture.

```json
{
  "course": "course identifier",
  "content": "Lecture String Content",
  "name": "Lecture name"
}
``` 

## GET /lectures

This endpoint is used to retrieve lectures. The user can supply two query params shown below.
```
/lectures?course=unique_identifier
/lectures?name=course_name
```

## GET /lectures/{id}

This endpoint is used to retrieve a single lecture
```
/lectures/{id}
```

## POST /lectures/{id}/summarizations

This endpoint is used to create a summarization from a lecture
```json
{
  "name": "Summarization name",
  "ratio": "Ratio of sentences to select"
}
```

## GET/DELETE /lectures/{id}/summarizations/{summarization_id} 

This endpoint allows you to get or delete a summarization.
```
/lectures/{id}/summarizations/{summarization_id} 
```