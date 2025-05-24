from flask import Flask, jsonify, request, abort
import json
import random

app = Flask(__name__)

SAMPLE_DATA_PATH = 'sample_bank_api.json'
MOCK_COMPANY_ID_IN_FILE = "GAMCO-001" # As per sample_bank_api.json

@app.route('/sim/v1/payments/transactions', methods=['GET'])
def get_transactions():
    # Simulate occasional unauthorized error
    if random.random() < 0.1: # 10% chance of 401 error
        abort(401, description="Simulated Unauthorized Access")

    company_id_param = request.args.get('companyId')
    # startDate = request.args.get('startDate') # Ignored for basic simulation
    # endDate = request.args.get('endDate')     # Ignored for basic simulation

    if company_id_param is None:
        abort(400, description="Missing companyId query parameter.")

    try:
        with open(SAMPLE_DATA_PATH, 'r') as f:
            data = json.load(f)
        
        # Check if the requested companyId matches the data in the file
        if company_id_param == data.get("companyId"):
            return jsonify(data)
        else:
            abort(404, description="Transaction data not found for the specified companyId.")
            
    except FileNotFoundError:
        abort(500, description=f"Sample data file not found: {SAMPLE_DATA_PATH}")
    except json.JSONDecodeError:
        abort(500, description="Error decoding sample data JSON.")

if __name__ == '__main__':
    app.run(port=5004, debug=True)
