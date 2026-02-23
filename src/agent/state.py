from typing import Dict, List, TypedDict, Annotated
import operator

class AgentState(TypedDict):
    # Base Inputs
    framework_name: str
    framework_description: str
    
    # Core Concept (P1 context to guide all agents)
    core_concept_directive: str
    
    # --- Content Fields (20 fields enforced by schema) ---
    # P1
    p1_business_purpose: str
    p1_problem_solved: str
    p1_key_characteristics: str
    p1_overview_architecture_mermaid: str
    p1_overview_flow_mermaid: str
    
    # P2
    p2_deep_architecture_mermaid: str
    p2_deep_flow_mermaid: str
    p2_data_architecture: str
    p2_interface_spec: str
    
    # P3
    p3_coding_standards: str
    p3_error_handling: str
    p3_infra_model: str
    
    # P4
    p4_security_control: str
    p4_nfr_baseline: str
    p4_observability: str
    
    # P5, P6, P7
    p5_deployment_topology: str
    p6_risks_and_antipatterns: str
    p6_trade_offs: str
    p7_when_to_use: str
    p7_when_not_to_use: str
    
    # Validation & Status
    diagram_errors: List[str]
    diagram_attempts: int
    mkdocs_status: str
