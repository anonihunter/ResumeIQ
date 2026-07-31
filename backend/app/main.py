from fastapi import FastAPI

app = FastAPI(
    title='ResumeIQ',
    description ='AI-powered Resume Analyzer built with FastAPI, PostgreSQL, Gemini AI, and React.',
    version = '1.0.0'
)

@app.get('/')
def root():
    return {'message': 'Hello World'}