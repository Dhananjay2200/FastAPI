from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app = FastAPI()

students = {
    'S001':{'name':'Ravi','marks':85,'grade':"A"},
    'S002':{'name':'Priya','marks':72,'grade':"B"},
    'S003':{'name':'ARjun','marks':91,'grade':"A+"}
}
# input 
class MarksSubmission(BaseModel):
    student_id:str
    marks:int
    subject:str

@app.get("/student/{student_id}")
def get_student(student_id:str):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} does not exists"
        )
    return students[student_id]

@app.post('/submit-marks')
def submit_marks(submission:MarksSubmission):
    # error 1 student dose not exsits
    if submission.student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"student with ID {submission.student_id} does not exists"

        )
    #error 2 vaid range 0 - 120
    if submission.marks < 0 or submission.marks >= 120:
        raise HTTPException(
            status_code=400,
            detail={
                'error':'marks must be in range 0 - 120',
                'marks_recevied':submission.marks,
                'fix':'enter a valid value between 0 and 120'
            }
        )
    # error - 3 subject name empty
    if submission.subject.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="subject name cannot be empty"
        )
    
    try:
        students[submission.student_id]["marks"] = submission.marks
        return {
            'message':'mark submitted successfully',
            'student':students[submission.student_id]["name"],
            'subject':submission.subject,
            'marks':submission.marks
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong on our side: {str(e)}"
        )
