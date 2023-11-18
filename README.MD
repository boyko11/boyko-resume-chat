# Boyko Resume Chat

A Python web application using FastAPI to interact with OpenAI's Assistant API.
The Assistant API is used to funny chat with Boyko's resume

## Setup and Installation

### Prerequisites

- Python 3.11 or higher
- pip

### Installing Dependencies

Run the following command to install the required packages:

```shell
pip install -r requirements.txt
```


## Running the Application

### local
Execute the following command to start the FastAPI server:

```shell
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000/chat`.

### Docker
build the image
```shell
docker build -t boyko-resume-chat .
```
start it up
```shell
docker run -p 8099:80 -e OPENAI_API_KEY={you_openai_api_key} boyko-resume-chat
```
access it at `http://127.0.0.1:8099/chat`.

## Usage

Just Chat Away

## Contributing

Unlikely that you will need to, but a PR would work


