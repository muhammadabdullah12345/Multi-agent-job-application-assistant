from langgraph.graph import StateGraph, END
from graph.state import ApplicationState
from graph.nodes import (
    analyze_jd,
    analyze_resume,
    analyze_gaps,
    write_cover_letter,
    generate_interview_questions,
)
from graph.router import route_decision


def build_graph():
    """Assembles and compiles the full LangGraph pipeline."""

    workflow = StateGraph(ApplicationState)

    # Register all nodes
    workflow.add_node("jd_analyzer", analyze_jd)
    workflow.add_node("resume_analyzer", analyze_resume)
    workflow.add_node("gap_analyzer", analyze_gaps)
    workflow.add_node("cover_letter_writer", write_cover_letter)
    workflow.add_node("interview_prep", generate_interview_questions)

    # Entry point
    workflow.set_entry_point("jd_analyzer")

    # Linear edges
    workflow.add_edge("jd_analyzer", "resume_analyzer")
    workflow.add_edge("resume_analyzer", "gap_analyzer")

    # Conditional branching after gap analysis
    workflow.add_conditional_edges(
        "gap_analyzer",
        route_decision,
        {
            "apply": "cover_letter_writer",
            "skip": END,
        },
    )

    # Continue pipeline if applying
    workflow.add_edge("cover_letter_writer", "interview_prep")
    workflow.add_edge("interview_prep", END)

    return workflow.compile()