import streamlit as st
from dotenv import load_dotenv
from graph.graph import build_graph
from utils.pdf_parser import extract_text_from_pdf

load_dotenv()

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Multi-Agent Job Application Assistant")
st.markdown(
    "Paste a job description and upload your resume. "
    "The AI pipeline will analyze fit, write a cover letter, and prep you for interviews."
)
st.divider()

# ── Inputs ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the full job description here",
        height=350,
        placeholder="Copy and paste the job description...",
    )

with col2:
    st.subheader("📄 Your Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"],
    )

st.divider()

# ── Run Button ────────────────────────────────────────────────
run_button = st.button("🚀 Analyze My Application", use_container_width=True)

if run_button:
    # Validation
    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()
    if uploaded_file is None:
        st.error("Please upload your resume PDF.")
        st.stop()

    # Extract resume text
    with st.spinner("Reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    if not resume_text.strip():
        st.error("Could not extract text from the PDF. Make sure it's not a scanned image.")
        st.stop()

    # Build graph
    graph = build_graph()

    initial_state = {
        "job_description": job_description,
        "resume_text": resume_text,
        "jd_analysis": "",
        "resume_analysis": "",
        "gap_analysis": "",
        "match_score": 0,
        "decision": "",
        "cover_letter": "",
        "interview_questions": "",
    }

    # ── Run pipeline with live status updates ─────────────────
    st.subheader("⚙️ Pipeline Running...")

    status_placeholder = st.empty()
    results = {}

    node_labels = {
        "jd_analyzer": "🔍 Analyzing job description...",
        "resume_analyzer": "📖 Analyzing your resume...",
        "gap_analyzer": "⚖️ Running gap analysis...",
        "cover_letter_writer": "✍️ Writing cover letter...",
        "interview_prep": "🎯 Generating interview questions...",
    }

    for event in graph.stream(initial_state):
        for node_name, node_output in event.items():
            label = node_labels.get(node_name, f"Running {node_name}...")
            status_placeholder.info(label)
            results.update(node_output)

    status_placeholder.success("✅ Pipeline complete!")
    st.divider()

    # ── Results ───────────────────────────────────────────────
    st.subheader("📊 Results")

    # Match Score
    score = results.get("match_score", 0)
    decision = results.get("decision", "apply")

    score_col, decision_col = st.columns(2)
    with score_col:
        st.metric("Match Score", f"{score} / 100")
        st.progress(score / 100)
    with decision_col:
        if decision == "apply":
            st.success("✅ Recommendation: APPLY")
        else:
            st.error("❌ Recommendation: SKIP — Poor fit for this role")

    st.divider()

    # Tabs for detailed output
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "JD Analysis",
        "Resume Analysis",
        "Gap Analysis",
        "Cover Letter",
        "Interview Prep",
    ])

    with tab1:
        st.markdown(results.get("jd_analysis", "Not available"))

    with tab2:
        st.markdown(results.get("resume_analysis", "Not available"))

    with tab3:
        st.markdown(results.get("gap_analysis", "Not available"))

    with tab4:
        if decision == "skip":
            st.warning("Cover letter not generated — match score too low.")
        else:
            cover_letter = results.get("cover_letter", "")
            st.markdown(cover_letter)
            st.download_button(
                label="📥 Download Cover Letter",
                data=cover_letter,
                file_name="cover_letter.txt",
                mime="text/plain",
            )

    with tab5:
        if decision == "skip":
            st.warning("Interview prep not generated — match score too low.")
        else:
            st.markdown(results.get("interview_questions", "Not available"))