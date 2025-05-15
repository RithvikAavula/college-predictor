from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load data from extracted CSV with all columns
df = pd.read_csv("cutoff_data.csv")

# Route to serve homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to get all colleges
@app.route('/colleges', methods=['GET'])
def get_all_colleges():
    colleges = df[['INST_CODE', 'INSTITUTE_NAME', 'PLACE', 'DIST']].drop_duplicates()
    return jsonify(colleges.to_dict(orient='records'))

# Route to get all branches of a particular college
@app.route('/branches/<inst_code>', methods=['GET'])
def get_college_branches(inst_code):
    branches = df[df['INST_CODE'] == inst_code][['BRANCH', 'BRANCH_NAME']].drop_duplicates()
    return jsonify(branches.to_dict(orient='records'))

# Route to get cutoff ranks for a specific branch in a specific college
@app.route('/cutoff/<inst_code>/<branch>', methods=['GET'])
def get_cutoff_data(inst_code, branch):
    result = df[(df['INST_CODE'] == inst_code) & (df['BRANCH'] == branch)]
    return jsonify(result.to_dict(orient='records'))

# Search by rank and category (with optional branch filter)
@app.route('/search', methods=['GET'])
def search_by_rank():
    category = request.args.get('category')  # e.g., 'OC_BOYS'
    rank = request.args.get('rank')
    branch = request.args.get('branch', '').upper()

    # Basic validation
    if not category or not rank:
        return jsonify({"error": "Please provide 'category' and 'rank' parameters."}), 400

    try:
        rank = int(rank)
    except ValueError:
        return jsonify({"error": "'rank' must be an integer."}), 400

    if category not in df.columns:
        return jsonify({"error": f"Category '{category}' not found in data columns."}), 400

    filtered = df[df[category].notna()]  # Filter out missing ranks
    filtered = filtered[filtered[category] >= rank]

    if branch:
        filtered = filtered[filtered['BRANCH'].str.upper() == branch]

    filtered = filtered.sort_values(by=category)

    return jsonify(filtered.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
