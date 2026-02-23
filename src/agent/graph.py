from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent.nodes import (
    lead_architect,
    visual_architect,
    diagram_validator,
    backend_engineer,
    infra_security_devops,
    governance_lead,
    mkdocs_compiler
)

def build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    # 1. Add all specialized node actors
    workflow.add_node("lead_architect", lead_architect)
    workflow.add_node("visual_architect", visual_architect)
    workflow.add_node("diagram_validator", diagram_validator)
    workflow.add_node("backend_engineer", backend_engineer)
    workflow.add_node("infra_security_devops", infra_security_devops)
    workflow.add_node("governance_lead", governance_lead)
    workflow.add_node("mkdocs_compiler", mkdocs_compiler)
    
    # 2. Define standard forward edges
    workflow.add_edge(START, "lead_architect")
    workflow.add_edge("lead_architect", "visual_architect")
    workflow.add_edge("visual_architect", "diagram_validator")
    
    # 3. Conditional validation loop for Mermaid
    def route_validation(state: AgentState):
        errors = state.get("diagram_errors", [])
        attempts = state.get("diagram_attempts", 0)
        
        # If there are NO errors -> Continue to next worker
        # OR if we tried too many times (cap at 3) -> Give up and continue anyway
        if len(errors) == 0 or attempts >= 3:
            return "backend_engineer"
            
        # If errors exist and attempts < 3, keep retrying drawing
        return "visual_architect"

    workflow.add_conditional_edges(
        "diagram_validator",
        route_validation,
        {
            "backend_engineer": "backend_engineer",
            "visual_architect": "visual_architect"
        }
    )
    
    # 4. Resume the specialized chain
    workflow.add_edge("backend_engineer", "infra_security_devops")
    workflow.add_edge("infra_security_devops", "governance_lead")
    workflow.add_edge("governance_lead", "mkdocs_compiler")
    workflow.add_edge("mkdocs_compiler", END)
    
    return workflow.compile()
