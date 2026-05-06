JD_ANALYSIS_PROMPT = """
You are an expert technical recruiter. Analyze the following job description and extract structured information.

Job Description:
{job_description}

Return your analysis in this exact format:

REQUIRED SKILLS: [comma-separated list]
PREFERRED SKILLS: [comma-separated list]
EXPERIENCE REQUIRED: [e.g., 3-5 years]
KEY RESPONSIBILITIES: [bullet points]
RED FLAGS: [anything unusual or very demanding, or "None"]
ROLE SUMMARY: [2-3 sentence summary of what this role is about]
"""

RESUME_ANALYSIS_PROMPT = """
You are an expert technical recruiter. Analyze the following resume and extract structured information.

Resume:
{resume_text}

Return your analysis in this exact format:

CANDIDATE SKILLS: [comma-separated list of all technical skills]
YEARS OF EXPERIENCE: [total estimated years]
NOTABLE ACHIEVEMENTS: [bullet points of standout accomplishments]
CURRENT/LAST ROLE: [job title and company]
EDUCATION: [degree and field]
OVERALL PROFILE: [2-3 sentence summary of the candidate]
"""

GAP_ANALYSIS_PROMPT = """
You are an expert technical recruiter doing a candidate-job fit analysis.

JD Analysis:
{jd_analysis}

Resume Analysis:
{resume_analysis}

Perform a thorough gap analysis and return in this exact format:

MATCHING SKILLS: [skills present in both JD and resume]
MISSING SKILLS: [required skills from JD not found in resume]
STRONG POINTS: [where the candidate clearly exceeds expectations]
WEAK POINTS: [areas where the candidate falls short]
MATCH SCORE: [a single integer from 0 to 100 representing overall fit]
RECOMMENDATION: [one of: STRONG APPLY / APPLY / BORDERLINE / SKIP]
SUMMARY: [3-4 sentence honest assessment]
"""

COVER_LETTER_PROMPT = """
You are a professional cover letter writer. Write a tailored, compelling cover letter.

Job Description Analysis:
{jd_analysis}

Candidate Resume Analysis:
{resume_analysis}

Gap Analysis:
{gap_analysis}

Instructions:
- Keep it to 3 paragraphs
- Opening: Show genuine interest and hook the reader
- Middle: Highlight matching skills and top 2-3 achievements relevant to this role
- Closing: Confident call to action
- Do NOT use generic phrases like "I am writing to apply for..."
- Sound human, confident, and specific — not like a template
- Do not mention the match score or gap analysis explicitly

Write the complete cover letter below:
"""

INTERVIEW_PREP_PROMPT = """
You are a senior technical interviewer preparing questions based on a candidate's weak areas and the job requirements.

JD Analysis:
{jd_analysis}

Gap Analysis:
{gap_analysis}

Generate exactly 5 interview questions that:
- Target the candidate's identified weak areas
- Are realistic for this role level
- Mix technical and behavioral questions
- Include a brief note on what the interviewer is really testing with each question

Format:
Q1: [question]
WHY THEY ASK THIS: [brief explanation]

Q2: [question]
WHY THEY ASK THIS: [brief explanation]

(and so on for Q3, Q4, Q5)
"""