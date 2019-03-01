# API Documentation

In this document, we will explain in the initial layout of the REST Api for lecture summarization.

| PATH                                             | Request Action | Description                                                                          | Request or Query Params                                     |
|--------------------------------------------------|----------------|--------------------------------------------------------------------------------------|-------------------------------------------------------------|
| /lectures                                        | POST           | The user can upload  lecture content, which can then be utilized for  summarization. | Params: course, content, name                               |
| /lectures                                        | GET            | Get all uploaded lectures.                                                           | Query Params: course, name                                  |
| /lectures/{id}                                   | GET            | Retrieve a lecture.                                                                  | Query Params: None                                          |
| /lectures/{id}/summarizations                    | POST/GET       | Create a summarization or  GET all summarizations for a given lecture.               | Params: name, number_of_sentences, Query Params: custom_tag |
| /lectures/{id}/summarizations/{summarization_id} | GET/DELETE     | Get or delete a summarized lecture.                                                  | None                                                        |


