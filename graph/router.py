from graph.state import ApplicationState


def route_decision(state: ApplicationState) -> str:
    """
    Conditional edge function.
    Reads the decision field from state and routes accordingly.
    Returns "apply" or "skip".
    """
    decision = state.get("decision", "apply")
    return decision