from typing import TypedDict, List

class ApplicationState(TypedDict):
    job_description: str
    resume_text: str
    jd_analysis: str
    resume_analysis: str
    gap_analysis: str
    match_score: int        # 0 to 100
    decision: str           # "apply" or "skip"
    cover_letter: str
    interview_questions: str