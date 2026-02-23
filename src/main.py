import argparse
import sys
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

from src.agent.graph import build_graph

def main():
    parser = argparse.ArgumentParser(description="Generate MkDocs Standard Framework Documentation")
    parser.add_argument("--topic", type=str, required=True, help="The standard framework topic to generate documentation for. e.g. 'High TPS API Service'")
    parser.add_argument("--description", type=str, required=False, default="", help="Optional detailed description or requirements for the framework.")
    args = parser.parse_args()

    topic = args.topic
    description = args.description
    print(f"Starting documentation generation for: '{topic}'")
    if description:
        print(f"Using description: '{description}'")
    
    # Build LangGraph app
    app = build_graph()
    
    # Initialize state
    initial_state = {
        "framework_name": topic,
        "framework_description": description,
        "diagram_errors": [],
        "diagram_attempts": 0
    }
    
    # Run the graph
    print("Executing workflow...")
    try:
        # Stream the output so we can see progress
        for output in app.stream(initial_state):
            for key, value in output.items():
                print(f"Finished Node: {key}")
                
        print("\nWorkflow completed successfully!")
    except Exception as e:
        print(f"\nWorkflow failed with error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
