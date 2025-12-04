## Backend Setup Guide (Flask + Llama + RAG + Bookings API)

This powers the Child Health and Wellness AI Assistant, it includes:

- Flask API
- Llama AI integration (text generation, structured output, RAG)
- Booking Endpoints (vaccine, eye test, dental)
- Sick-abscence logging
- Simple SQlite database
- Optional RAG (vector search using ChromaDB)


### Getting started

1. Clone Repo, Create and Activate Virtual Environment
```bash
git clone <repository-url>
cd backend

#linux/mac
python3 -m venv venv
source venv/bin/activate

#windows
python -m venv venv
venv\Scripts\activate #For Command Prompt
#or
.\venv\Scripts\Activate.ps1 # for PowerShell
#or
source venv/Scripts/activate #for Git Bash

   ```

2. Install Dependencies
```bash

pip install -r requirements.txt
   ```

3. Run the Flask server
```text
python app.py

```
You should see :
```text

{"message": "Hello, Flask is running!"}


#on your browser
```