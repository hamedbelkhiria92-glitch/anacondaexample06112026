from fastapi import APIRouter,HTTPException
from .models import FlashCard,FlashCardsRequest,FlashCardsResponse
from services.ai import call_llm,AIServiceError
from services.errors import ai_error_http
router = APIRouter(prefix="/flashcard",tags=["flashcards"])

@router.post("/",response_model=FlashCardsResponse)
def flashcard(request:FlashCardsRequest):
    clean_topic = request.topic.strip()
    if not clean_topic:
        raise HTTPException(status_code=400,
                            detail="Topic can not be empty")
    try:
            flashcards = call_llm(clean_topic,FlashCardsResponse)
    except AIServiceError as error:
            raise ai_error_http(error)
     
     
    
    return FlashCardsResponse(
        topic=flashcards["topic"],
        flashcards=flashcards["flashcards"])