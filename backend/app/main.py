from fastapi import FastAPI
from backend.routes.auth import auth_router

app = FastAPI(
    title='ResumeIQ',
    description ='AI-powered Resume Analyzer built with FastAPI, PostgreSQL, Gemini AI, and React.',
    version = '1.0.0'
)


@app.get('/')
def root():
    return {'message': 'App Started Successfully'}

# Register the router into the main app
app.include_router(auth_router)