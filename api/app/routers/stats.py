from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload 
from sqlalchemy import func
from typing import List, Dict

from app.database import get_db
from app.models import Word, PracticeSession
from app.schemas import SummaryResponse, HistoryItem, DifficultyLevel

router = APIRouter()

@router.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    total_practices = db.query(PracticeSession).count()
    average_score = db.query(func.avg(PracticeSession.score)).scalar()
    avg_score_rounded = round(average_score, 2) if average_score is not None else 0.0
    total_unique_words = db.query(PracticeSession.word_id).distinct().count()

    level_counts = db.query(
        Word.difficulty_level, 
        func.count(PracticeSession.id)
    ).join(Word, PracticeSession.word_id == Word.id).group_by(Word.difficulty_level).all()
    
    level_distribution: Dict[str, int] = {
        level: count for level, count in level_counts
    }
    all_levels: List[DifficultyLevel] = ['Beginner', 'Intermediate', 'Advanced']
    final_distribution = {level: level_distribution.get(level, 0) for level in all_levels}
    
    return SummaryResponse(
        total_practices=total_practices,
        average_score=avg_score_rounded,
        total_words_practiced=total_unique_words,
        level_distribution=final_distribution
    )


@router.get("/history", response_model=List[HistoryItem])
def get_history(limit: int = 10, db: Session = Depends(get_db)):
    history_records = db.query(PracticeSession).options(joinedload(PracticeSession.word_rel))\
        .order_by(PracticeSession.practiced_at.desc())\
        .limit(limit).all()

    history_list: List[HistoryItem] = [
        HistoryItem(
            id=item.id,
            word=item.word_rel.word,
            user_sentence=item.user_sentence,
            score=float(item.score),
            practiced_at=item.practiced_at
        )
        for item in history_records
    ]
    return history_list





# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from typing import List

# from app.database import get_db
# from app.models import Word, PracticeSession
# from app.schemas import SummaryResponse, HistoryItem

# router = APIRouter()


# @router.get("/summary", response_model=SummaryResponse)
# def get_summary(db: Session = Depends(get_db)):
#     """Get overall practice statistics"""
    
#     # Total practice sessions
#     # Average score
#     # Total unique words practiced
    
#     # Distribution by level
#     ...


# @router.get("/history", response_model=List[HistoryItem])
# def get_history(limit: int = 10, db: Session = Depends(get_db)):
#     """Get last 10 practice sessions"""
#     ...