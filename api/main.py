from fastapi import FastAPI
from fastapi import HTTPException
from app.schemas import WordResponse
from app.routers import words, practice
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware



Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Vocabulary Practice API",
    version="1.0.0",
    description="API for vocabulary practice and learning"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





app.include_router(words.router, prefix="/api", tags=["words"])
app.include_router(practice.router, prefix="/api", tags=["practice"])
'''

@app.get("/api/word", response_model=WordResponse)
def get_random_word():
    """Get a random word"""
    # TODO Write logic here....
    #return {
      #  "word": "example",
      #  "definition": "a representative form or pattern",
       # "difficulty_level": "Beginner"}
  #  return WordResponse(
  #      id=12,
   #     word='book',
    #    definition='This is a book',
     #   difficulty_level='Beginner'
    #)
    words = []
    if len(words) == 0:
        raise HTTPException(
            status_code=404,
            detail="NO word available in database"
        )
   
'''
    

@app.get("/")
def read_root():
    return {
        "message": "Vocabulary Practice API",
        "version": "1.0.0",
        "endpoints": {
            "random_word": "/api/word",
            "validate": "/api/validate-sentence",
            "summary": "/api/summary",
            "history": "/api/history"
        }
    }











