from fastapi import APIRouter, HTTPException
from .models import SummarizeRequest,SummarizeResponse
from services.ai import call_llm,AIServiceError
from services.errors import ai_error_http
router = APIRouter(prefix="/summarize",tags=['summarize'])

@router.post("/",response_model=SummarizeResponse)
def summarize(request:SummarizeRequest):
    words = request.text.split()
    if not words:
            raise HTTPException(status_code=400,
                                        detail="Message can not be empty")
    try:
        summarize_reply = call_llm(request.subject,SummarizeResponse)
    except AIServiceError as error:
                    raise ai_error_http(error)
    return SummarizeResponse(
        summary=[
            "Normalement summary",
            "The Real summary"[:summarize_reply["max_bullets"]],
            
        ],
        word_count=len(words)
    )
