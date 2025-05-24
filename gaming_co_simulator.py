from flask import Flask, jsonify, request, abort
import json
import random

app = Flask(__name__)

SAMPLE_DATA_PATH = 'sample_gaming_company_api.json'
# Assuming the sample file contains data for this specific company ID
MOCK_COMPANY_ID_IN_FILE = "GAMCO-001" 

@app.route('/sim/v1/gamingco/<string:companyId>/revenue', methods=['GET'])
def get_revenue(companyId):
    # Simulate occasional server error
    if random.random() < 0.1: # 10% chance of 500 error
        abort(500, description="Simulated Server Error")

    # report_date = request.args.get('reportDate') # Optional: use if needed for more complex simulation

    if companyId == MOCK_COMPANY_ID_IN_FILE: # Check against the ID expected in the path
        try:
            with open(SAMPLE_DATA_PATH, 'r') as f:
                data = json.load(f)
            
            # Additionally verify that the data in the file corresponds to the companyId,
            # especially if the file could theoretically contain data for other companies.
            # For this setup, we assume the sample file is specific to MOCK_COMPANY_ID_IN_FILE.
            if data.get("companyId") == companyId:
                return jsonify(data)
            else:
                # This case would mean the MOCK_COMPANY_ID_IN_FILE is not consistent with the file content.
                abort(404, description="Data in sample file does not match the requested companyId.")
        except FileNotFoundError:
            abort(500, description=f"Sample data file not found: {SAMPLE_DATA_PATH}")
        except json.JSONDecodeError:
            abort(500, description="Error decoding sample data JSON.")
    else:
        abort(404, description="Company ID not found.")

if __name__ == '__main__':
    app.run(port=5001, debug=True)
