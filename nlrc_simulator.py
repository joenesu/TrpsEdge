from flask import Flask, jsonify, request, abort
import json
import random

app = Flask(__name__)

SAMPLE_DATA_PATH = 'sample_nlrc_api.json'
MOCK_COMPANY_ID_IN_FILE = "GAMCO-001" # As per sample_nlrc_api.json

@app.route('/sim/v1/nlrc/licenses', methods=['GET'])
def get_licenses():
    # Simulate occasional service unavailable error
    if random.random() < 0.1: # 10% chance of 503 error
        abort(503, description="Simulated Service Unavailable")

    company_id_param = request.args.get('companyId')

    try:
        with open(SAMPLE_DATA_PATH, 'r') as f:
            data = json.load(f)
        
        # If no companyId param, or if it matches the one in the file, return the sample.
        # This is a simple simulation; a more complex one might return a list or filter.
        if company_id_param is None or company_id_param == data.get("companyId"):
            # Check if the requested companyId matches the data in the file,
            # if a companyId was provided in the request.
            if company_id_param and data.get("companyId") != company_id_param:
                 abort(404, description="License data not found for the specified companyId.")
            return jsonify(data)
        elif company_id_param and data.get("companyId") != company_id_param:
            abort(404, description="License data not found for the specified companyId.")
        else:
            # If company_id_param is provided but doesn't match, and for some reason the above didn't catch it.
            # Or, if you want to be strict and only return if company_id_param is NOT None.
            # For this version, we allow no company_id_param to return the sample.
            # If strict matching is desired when company_id_param is present:
            abort(404, description="License data not found for the specified companyId.")

    except FileNotFoundError:
        abort(500, description=f"Sample data file not found: {SAMPLE_DATA_PATH}")
    except json.JSONDecodeError:
        abort(500, description="Error decoding sample data JSON.")

if __name__ == '__main__':
    app.run(port=5002, debug=True)
