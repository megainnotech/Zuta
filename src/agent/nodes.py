import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import json

from src.agent.state import AgentState
from src.agent.llm import get_llm
from src.utils.mermaid import validate_mermaid_syntax

# --- Output Schemas ---
class ArchitectOutput(BaseModel):
    core_concept_directive: str = Field(description="The central architectural directive to guide all other agents.")
    p1_business_purpose: str = Field(description="Purpose of this framework")
    p1_problem_solved: str = Field(description="What problem this solves")
    p1_key_characteristics: str = Field(description="Key characteristics (bullet points)")

class VisualArchitectOutput(BaseModel):
    p1_overview_architecture_mermaid: str = Field(description="Mermaid code for high-level architecture diagram")
    p1_overview_flow_mermaid: str = Field(description="Mermaid code for high-level interaction happy path flow")
    p2_deep_architecture_mermaid: str = Field(description="Mermaid code for deep, detailed component-level architecture diagram")
    p2_deep_flow_mermaid: str = Field(description="Mermaid code for deep interaction flow including edge cases")

class BackendEngineerOutput(BaseModel):
    p2_data_architecture: str = Field(description="Markdown description of the Data Architecture")
    p2_interface_spec: str = Field(description="Markdown Interface Specification (REST, gRPC, Pub/Sub, etc.)")
    p3_coding_standards: str = Field(description="Markdown Coding Standards (Circuit Breaker, Retry Logic, Saga, etc.)")
    p3_error_handling: str = Field(description="Markdown Error Handling & Exception Strategy")

class InfraDevOpsOutput(BaseModel):
    p3_infra_model: str = Field(description="Markdown Built-in Platform & Infrastructure Model")
    p4_security_control: str = Field(description="Markdown Built-in Security Control")
    p4_nfr_baseline: str = Field(description="Markdown NFR Baseline expectations")
    p4_observability: str = Field(description="Markdown Observability architecture")
    p5_deployment_topology: str = Field(description="Markdown Deployment Topology")

class GovernanceOutput(BaseModel):
    p6_risks_and_antipatterns: str = Field(description="Markdown Risks and Anti-patterns")
    p6_trade_offs: str = Field(description="Markdown Trade-offs")
    p7_when_to_use: str = Field(description="Markdown When to Use")
    p7_when_not_to_use: str = Field(description="Markdown When NOT to Use")


def _run_agent_with_fallback(llm, prompt_template, parser, input_vars):
    """Helper to run the chain and natively fallback to basic JSON parsing if Gemini injects ticks."""
    chain = prompt_template | llm | parser
    try:
        return chain.invoke(input_vars)
    except Exception as e:
        print(f"Primary parsing failed: {e}. Retrying raw invoke...")
        res = llm.invoke(prompt_template.format_prompt(**input_vars))
        try:
            return parser.invoke(res)
        except Exception as e2:
            print(f"Fallback parsing failed: {e2}. Attempting manual extract.")
            text = res.content.strip()
            # Try to find the start and end of a JSON object
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError as je:
                    print(f"Critical Parsing Failure: {je}")
            
            print("Could not locate valid JSON in response. Returning mapping of empty strings.")
            # Return a dict with empty strings for expected keys based on the Pydantic model
            if hasattr(parser, 'pydantic_object'):
                 return {k: "" for k in parser.pydantic_object.__fields__.keys()}
            return {}

# --- Nodes ---

def lead_architect(state: AgentState):
    print(f"--- NODE: lead_architect ---")
    llm = get_llm()
    parser = JsonOutputParser(pydantic_object=ArchitectOutput)
    
    desc = f"\nUser Requirements:\n{state.get('framework_description', '')}" if state.get('framework_description') else ""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Lead Solutions Architect. Your job is to define the P1 Overview and the Core Directive for the standard framework. Provide deep, professional markdown for the text fields. Output valid JSON.\n\n{format_instructions}"),
        ("human", "Framework Topic: {framework_name}{desc}")
    ])
    
    result = _run_agent_with_fallback(llm, prompt, parser, {
        "framework_name": state["framework_name"],
        "desc": desc,
        "format_instructions": parser.get_format_instructions()
    })
    return result

def visual_architect(state: AgentState):
    print(f"--- NODE: visual_architect ---")
    llm = get_llm()
    parser = JsonOutputParser(pydantic_object=VisualArchitectOutput)
    
    error_msg = ""
    if state.get("diagram_errors"):
        error_msg = f"Previous attempts failed with these errors:\n{state['diagram_errors'][-1]}\n\nPlease fix your Mermaid syntax."
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Visual Architect Specialist. Generate exactly 4 valid, complex Mermaid.js diagrams based strictly on the Core Directive. DO NOT wrap the mermaid code in markdown backticks inside the JSON.\n\n{format_instructions}"),
        ("human", "Core Directive:\n{core_directive}\n\n{error_msg}")
    ])
    
    result = _run_agent_with_fallback(llm, prompt, parser, {
        "core_directive": state.get("core_concept_directive", ""),
        "error_msg": error_msg,
        "format_instructions": parser.get_format_instructions()
    })
    
    # Strip backticks just in case
    for key in result:
        val = result[key].strip()
        if val.startswith("```mermaid"): val = val[10:]
        elif val.startswith("```"): val = val[3:]
        if val.endswith("```"): val = val[:-3]
        result[key] = val.strip()
        
    result["diagram_attempts"] = state.get("diagram_attempts", 0) + 1
    return result

def diagram_validator(state: AgentState):
    print(f"--- NODE: diagram_validator ---")
    
    errors = []
    diagrams_to_check = {
        "P1 Arch": state.get("p1_overview_architecture_mermaid", ""),
        "P1 Flow": state.get("p1_overview_flow_mermaid", ""),
        "P2 Arch": state.get("p2_deep_architecture_mermaid", ""),
        "P2 Flow": state.get("p2_deep_flow_mermaid", "")
    }
    
    for name, code in diagrams_to_check.items():
        err = validate_mermaid_syntax(code)
        if err: errors.append(f"{name} Diagram Error:\n{err}")
    
    existing_errors = state.get("diagram_errors", [])
    if errors:
        existing_errors.append("\n\n".join(errors))
        print("Validation Failed. Routing back to visual_architect.")
    else:
        print("Validation Passed!")
        
    return {"diagram_errors": existing_errors}

def backend_engineer(state: AgentState):
    print(f"--- NODE: backend_engineer ---")
    llm = get_llm()
    parser = JsonOutputParser(pydantic_object=BackendEngineerOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Senior Backend Engineer. Write deep, practical Markdown content for P2 (Data, Interfaces) and P3 (Coding standards, Error handling) based strictly on the Core Directive. Output valid JSON.\n\n{format_instructions}"),
        ("human", "Framework: {framework_name}\nCore Directive:\n{core_directive}")
    ])
    
    result = _run_agent_with_fallback(llm, prompt, parser, {
        "framework_name": state["framework_name"],
        "core_directive": state.get("core_concept_directive", ""),
        "format_instructions": parser.get_format_instructions()
    })
    return result

def infra_security_devops(state: AgentState):
    print(f"--- NODE: infra_security_devops ---")
    llm = get_llm()
    parser = JsonOutputParser(pydantic_object=InfraDevOpsOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a DevOps & Security Lead. Write deep, practical Markdown content for Infra, Security, Observability, and Deployment Topology based strictly on the Core Directive. Output valid JSON.\n\n{format_instructions}"),
        ("human", "Framework: {framework_name}\nCore Directive:\n{core_directive}")
    ])
    
    result = _run_agent_with_fallback(llm, prompt, parser, {
        "framework_name": state["framework_name"],
        "core_directive": state.get("core_concept_directive", ""),
        "format_instructions": parser.get_format_instructions()
    })
    return result

def governance_lead(state: AgentState):
    print(f"--- NODE: governance_lead ---")
    llm = get_llm()
    parser = JsonOutputParser(pydantic_object=GovernanceOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an Enterprise Architecture Governance Lead. Write deep, practical Markdown content for P6 (Risks/Trade-offs) and P7 (Decision Guide) based strictly on the Core Directive. Output valid JSON.\n\n{format_instructions}"),
        ("human", "Framework: {framework_name}\nCore Directive:\n{core_directive}")
    ])
    
    result = _run_agent_with_fallback(llm, prompt, parser, {
        "framework_name": state["framework_name"],
        "core_directive": state.get("core_concept_directive", ""),
        "format_instructions": parser.get_format_instructions()
    })
    return result

def mkdocs_compiler(state: AgentState):
    print(f"--- NODE: mkdocs_compiler ---")
    
    output_dir = "output"
    docs_dir = os.path.join(output_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    # Safely get variables
    def _g(key): return state.get(key, "")

    # Write Markdowns mapped precisely to P1-P7
    files_map = {
         "index.md": f"# {state['framework_name']}\n\n"
                     f"## 1. Business Context\n\n### Purpose\n{_g('p1_business_purpose')}\n\n"
                     f"### What problem this solves?\n{_g('p1_problem_solved')}\n\n"
                     f"### Key characteristics\n{_g('p1_key_characteristics')}\n\n"
                     f"## 2. Architecture Overview\n\n```mermaid\n{_g('p1_overview_architecture_mermaid')}\n```\n\n"
                     f"## 3. Interaction Flow (Happy path)\n\n```mermaid\n{_g('p1_overview_flow_mermaid')}\n```",
                     
         "p2-architecture.md": f"# P2. Architecture\n\n"
                               f"## 1. Architecture Diagram (deep)\n\n```mermaid\n{_g('p2_deep_architecture_mermaid')}\n```\n\n"
                               f"## 2. Interaction Flow (deep)\n\n```mermaid\n{_g('p2_deep_flow_mermaid')}\n```\n\n"
                               f"## 3. Data Architecture\n\n{_g('p2_data_architecture')}\n\n"
                               f"## 4. Interface Specification\n\n{_g('p2_interface_spec')}",
                               
         "p3-design.md": f"# P3. App Design Pattern\n\n"
                         f"## 1. Coding Standards\n\n{_g('p3_coding_standards')}\n\n"
                         f"## 2. Error Handling & Exception Strategy\n\n{_g('p3_error_handling')}\n\n"
                         f"# Platform & Infrastructure\n\n"
                         f"## 1. Built-in Infra Model\n\n{_g('p3_infra_model')}",
                         
         "p4-security.md": f"# P4. Security & NFR\n\n"
                           f"## 1. Built-in Security Control\n\n{_g('p4_security_control')}\n\n"
                           f"## 2. NFR Baseline\n\n{_g('p4_nfr_baseline')}\n\n"
                           f"## 3. Observability\n\n{_g('p4_observability')}",
                           
         "p5-deployment.md": f"# P5. Deployment\n\n"
                             f"## 1. Deployment Topology\n\n{_g('p5_deployment_topology')}",
                             
         "p6-risks.md": f"# P6. Risks & Anti-patterns\n\n"
                        f"## 1. Risk & Anti-pattern\n\n{_g('p6_risks_and_antipatterns')}\n\n"
                        f"## 2. Trade-offs (ได้อย่าง เสียอย่าง)\n\n{_g('p6_trade_offs')}",
                        
         "p7-decision.md": f"# P7. Decision Guide\n\n"
                           f"## 1. When to Use\n\n{_g('p7_when_to_use')}\n\n"
                           f"## 2. When NOT to Use\n\n{_g('p7_when_not_to_use')}"
    }
    
    for filename, content in files_map.items():
         with open(os.path.join(docs_dir, filename), "w", encoding="utf-8") as f:
             f.write(content)
             
    # Write mkdocs.yml (keeping original structure)
    mkdocs_yml_content = f"""site_name: {state['framework_name']} Standard
theme:
  name: material
  features:
    - navigation.tabs
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format

nav:
  - P1. Overview: index.md
  - P2. Architecture: p2-architecture.md
  - P3. App Design Pattern: p3-design.md
  - P4. Security & NFR: p4-security.md
  - P5. Deployment: p5-deployment.md
  - P6. Risks & Anti-patterns: p6-risks.md
  - P7. Decision Guide: p7-decision.md
"""
    with open(os.path.join(output_dir, "mkdocs.yml"), "w", encoding="utf-8") as f:
         f.write(mkdocs_yml_content)
         
    return {"mkdocs_status": "Success! Documentation generated in ./output"}
