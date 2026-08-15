from fastapi import FastAPI

app = FastAPI(
    title="AI Image Understanding & Content Matching Engine",
    description="FlyRank Backend Capstone",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Image Understanding & Content Matching Engine!"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }