from fastapi import HTTPException,APIRouter
from .models import Quizz,QuizzResponse,QuizzRequest
from services.ai import call_llm,AIServiceError
from services.errors import ai_error_http
router = APIRouter(prefix="/quizz",tags=["quizz"])
@router.post('/')
def quizz(request:QuizzRequest):
    questions = []
    for index in range(1,request.number_quizzes+1):
         
        if not request.subject:
                raise HTTPException(status_code=400,
                                    detail="Message can not be empty")
        try:
                optionsanswer = call_llm(request.subject,QuizzResponse)
        except AIServiceError as error:
                raise ai_error_http(error)
        return optionsanswer
         
    
    return QuizzResponse(
        topic=request.subject,
        nb_questions=request.number_quizzes,
        quizz=questions
    )