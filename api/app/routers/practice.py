from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Word, PracticeSession
from app.schemas import ValidateSentenceRequest, ValidateSentenceResponse
from app.utils import mock_ai_validation
from app import crud

router = APIRouter()

@router.post("/validate-sentence", response_model=ValidateSentenceResponse)
def validate_sentence(
    request: ValidateSentenceRequest,
    db: Session = Depends(get_db)
):
    word_data = db.query(Word).filter(Word.id == request.word_id).first()
    if not word_data:
        raise HTTPException(status_code=404, detail=f"Word ID {request.word_id} not found.")

    result = mock_ai_validation(
        request.sentence,
        word_data.word,           
        word_data.difficulty_level 
    )

    user_id = 1 
    crud.create_practice_submission(
        db,
        user_id=user_id,
        word_id=request.word_id,
        submitted_sentence=request.sentence,
        score=result['score'],
        feedback=result['suggestion'],
        corrected_sentence=result['corrected_sentence']
    )
    return ValidateSentenceResponse(**result)





# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.routers import practice
# from app.database import get_db
# from app.models import Word, PracticeSession
# from app.schemas import ValidateSentenceRequest, ValidateSentenceResponse
# from app.utils import mock_ai_validation

# router = APIRouter()


# @router.post("/validate-sentence", response_model=ValidateSentenceResponse)
# def validate_sentence(
#     request: ValidateSentenceRequest,
#     db: Session = Depends(get_db)
# ):
#     """
#     Receive user sentence and validate it (mock AI)
#     Save results to database
#     """
#     # Get word data
#     # Mock AI validation
#     # Save to database
#     return ValidateSentenceResponse(
#         score=85,
#         level="Intermediate",
#         suggestion="Good job! Just a minor correction needed.",
#         corrected_sentence="This is the corrected sentence."
#     )