from flask import Flask, jsonify, request, abort
import json
import random

app = Flask(__name__)

SAMPLE_DATA_PATH = 'sample_firs_irs_api.json'
# Assuming sample data contains these specific values for matching
MOCK_COMPANY_ID_IN_FILE = "GAMCO-003" 
MOCK_TAX_TYPE_IN_FILE = "FCT" # As per sample_firs_irs_api.json

@app.route('/sim/v1/irs/invoices', methods=['GET'])
def get_invoices():
    # Simulate occasional rate limit error
    if random.random() < 0.1: # 10% chance of 429 error
        abort(429, description="Simulated Rate Limit Exceeded")

    company_id_param = request.args.get('companyId')
    tax_type_param = request.args.get('taxType')

    try:
        with open(SAMPLE_DATA_PATH, 'r') as f:
            data = json.load(f)

        # Check if provided params match the data in the sample file
        # This is a simple simulation; a more complex one might handle various param combinations
        # or return lists if multiple invoices could match.
        if (company_id_param == data.get("companyId") and
            tax_type_param == data.get("taxType")):
            return jsonify(data)
        # If no params are provided, one could choose to return the sample,
        # but for this case, let's require matching params for a valid response.
        elif company_id_param is None and tax_type_param is None:
             # Defaulting to returning the sample if no params are provided for broader testing.
             # If strict param matching is required, this should be an abort(400) or abort(404).
             # For now, let's assume if no params, just return the sample as a fallback.
             # This behavior can be tightened if needed.
             # For this iteration, I will enforce that parameters are needed.
            abort(400, description="Missing companyId or taxType query parameters.")
        else:
            # If params are provided but do not match the sample file's content
            abort(404, description="Invoice data not found for the specified companyId and taxType.")

    except FileNotFoundError:
        abort(500, description=f"Sample data file not found: {SAMPLE_DATA_PATH}")
    except json.JSONDecodeError:
        abort(500, description="Error decoding sample data JSON.")

if __name__ == '__main__':
    app.run(port=5003, debug=True)
