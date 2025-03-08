from flask import Flask, request, jsonify
from main import run_agent  # Import the run_agent function from the module
import yaml
app = Flask(__name__)

# Route to call the agent with the company name
@app.route('/agent', methods=['GET'])
def agent():
    company_name = request.args.get('company', type=str)  # Get the company name from the query params
    
    if not company_name:
        return jsonify({"error": "Company name is required"}), 400
    
    try:
        # Call the agent function with the company name
        research_results = run_agent(company_name)
        
        # If results contain an error, return it
        if "error" in research_results:
            return jsonify(research_results), 500
        
        # Return the research results as YAML (could also return as JSON)
        return yaml.dump(research_results, default_flow_style=False, allow_unicode=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
