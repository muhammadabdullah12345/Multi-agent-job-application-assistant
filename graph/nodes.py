import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from graph.state import ApplicationState
from prompts.templates import (
    JD_ANALYSIS_PROMPT,
    RESUME_ANALYSIS_PROMPT,
    GAP_ANALYSIS_PROMPT,
    COVER_LETTER_PROMPT,
    INTERVIEW_PREP_PROMPT,
)

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


def analyze_jd(state: ApplicationState) -> dict:
    """Node 1: Analyzes the job description."""
    prompt = JD_ANALYSIS_PROMPT.format(
        job_description=state["job_description"]
    )
    response = llm.invoke(prompt)
    return {"jd_analysis": response.content}


def analyze_resume(state: ApplicationState) -> dict:
    """Node 2: Analyzes the candidate's resume."""
    prompt = RESUME_ANALYSIS_PROMPT.format(
        resume_text=state["resume_text"]
    )
    response = llm.invoke(prompt)
    return {"resume_analysis": response.content}


def analyze_gaps(state: ApplicationState) -> dict:
    """Node 3: Compares JD and resume, produces gap analysis and match score."""
    prompt = GAP_ANALYSIS_PROMPT.format(
        jd_analysis=state["jd_analysis"],
        resume_analysis=state["resume_analysis"],
    )
    response = llm.invoke(prompt)
    content = response.content

    # Extract match score from the response
    match_score = 50  # default fallback
    for line in content.split("\n"):
        if line.startswith("MATCH SCORE:"):
            try:
                score_str = line.replace("MATCH SCORE:", "").strip()
                match_score = int("".join(filter(str.isdigit, score_str)))
            except ValueError:
                pass

    # Extract decision from recommendation
    decision = "apply"
    for line in content.split("\n"):
        if line.startswith("RECOMMENDATION:"):
            rec = line.replace("RECOMMENDATION:", "").strip().upper()
            if "SKIP" in rec:
                decision = "skip"
            else:
                decision = "apply"

    return {
        "gap_analysis": content,
        "match_score": match_score,
        "decision": decision,
    }


def write_cover_letter(state: ApplicationState) -> dict:
    """Node 4: Writes a tailored cover letter."""
    prompt = COVER_LETTER_PROMPT.format(
        jd_analysis=state["jd_analysis"],
        resume_analysis=state["resume_analysis"],
        gap_analysis=state["gap_analysis"],
    )
    response = llm.invoke(prompt)
    return {"cover_letter": response.content}


def generate_interview_questions(state: ApplicationState) -> dict:
    """Node 5: Generates targeted interview prep questions."""
    prompt = INTERVIEW_PREP_PROMPT.format(
        jd_analysis=state["jd_analysis"],
        gap_analysis=state["gap_analysis"],
    )
    response = llm.invoke(prompt)
    return {"interview_questions": response.content}