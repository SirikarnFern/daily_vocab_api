from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Word, PracticeSession
from app.schemas import ValidateSentenceRequest, ValidateSentenceResponse
from app.utils import mock_ai_validation

router = APIRouter()


@router.post("/validate-sentence", response_model=ValidateSentenceResponse)
def validate_sentence(
    request: ValidateSentenceRequest,
    db: Session = Depends(get_db)
):
    """
    Receive user sentence and validate it (mock AI)
    Save results to database
    """
    # Get word data

    word_obj = db.query(Word).filter(Word.id == request.word_id).first()
    if not word_obj:
        raise HTTPException(status_code=404, detail="Word not found")

    word = word_obj.word
    difficulty_level = word_obj.difficulty_level


    # Mock AI validation
    result = mock_ai_validation(request.sentence, word, difficulty_level)

    # Save to database
    practice = PracticeSession(
        user_id=1,  # สมมติ user_id=1, สามารถแก้ให้รับจาก JWT หรือ request ได้
        word_id=request.word_id,
        submitted_sentence=request.sentence,
        score=result["score"],
        timestamp=datetime.utcnow()
    )
    db.add(practice)
    db.commit()
    db.refresh(practice)    

    
    return ValidateSentenceResponse(
       score=85,
       level="Intermediate",
       suggestion="Good job! Just a minor correction needed.",
       corrected_sentence="This is the corrected sentence."
   )