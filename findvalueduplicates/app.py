from flask import Flask, render_template, request, jsonify
import re
from collections import OrderedDict

app = Flask(__name__)

def parse_log_line(log_line):
    # Extract key-value pairs into an OrderedDict
    log_kv = OrderedDict()
    # Updated pattern to handle both quoted and unquoted values
    pattern = r'(\w+(?:\.\w+)*?)=(?:"([^"]*)"|(\S+))'
    matches = re.findall(pattern, log_line)

    for match in matches:
        key = match[0]
        # Take the quoted value if it exists, otherwise take the unquoted value
        value = match[1] if match[1] else match[2]
        log_kv[key] = value

    # Find duplicates
    value_dict = {}
    for k, v in log_kv.items():
        if v not in value_dict:
            value_dict[v] = {"count": 0, "keys": []}
        value_dict[v]["count"] += 1
        value_dict[v]["keys"].append(k)

    # Filter for duplicates only
    duplicates = {
        val: info
        for val, info in value_dict.items()
        if info["count"] > 1 and val != "nil"  # Exclude "nil" values
    }
    
    print(f"Parsed key-values: {log_kv}")  # Debug print
    print(f"Found duplicates: {duplicates}")  # Debug print
    
    return duplicates

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    line = data.get('line', '')
    print(f"Received line: {line}")  # Debug print
    result = parse_log_line(line)
    print(f"Analysis result: {result}")  # Debug print
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 