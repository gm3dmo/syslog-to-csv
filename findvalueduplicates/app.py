from flask import Flask, render_template, request, jsonify
import re
from collections import OrderedDict

app = Flask(__name__)

def calculate_bytes_duplicated(value, keys, count):
    """Calculate total bytes duplicated: sum of (1 + len(key) + len(value)) for each duplicate"""
    if count <= 1:
        return 0
    return sum(1 + len(key) + len(str(value)) for key in keys) - (1 + len(keys[0]) + len(str(value)))

def parse_log_line(log_line):
    try:
        # Extract key-value pairs into an OrderedDict
        log_kv = OrderedDict()
        # Updated pattern to handle both quoted and unquoted values
        pattern = r'(\w+(?:\.\w+)*?)=(?:"([^"]*)"|(\S+))'
        matches = re.findall(pattern, log_line)

        print(f"Found matches: {matches}")  # Debug print

        for match in matches:
            key = match[0]
            # Take the quoted value if it exists, otherwise take the unquoted value
            value = match[1] if match[1] else match[2]
            log_kv[key] = value

        print(f"Parsed key-values: {log_kv}")  # Debug print

        # Find duplicates
        value_dict = {}
        for k, v in log_kv.items():
            if v not in value_dict:
                value_dict[v] = {"count": 0, "keys": [], "bytes_duplicated": 0}
            value_dict[v]["count"] += 1
            value_dict[v]["keys"].append(k)

        print(f"Value dictionary: {value_dict}")  # Debug print

        # Filter for duplicates only and calculate bytes
        duplicates = {}
        total_bytes_duplicated = 0
        for val, info in value_dict.items():
            if info["count"] > 1 and val != "nil":
                bytes_dup = calculate_bytes_duplicated(val, info["keys"], info["count"])
                info["bytes_duplicated"] = bytes_dup
                total_bytes_duplicated += bytes_dup
                duplicates[val] = info

        if duplicates:
            duplicates["_summary"] = {"total_bytes_duplicated": total_bytes_duplicated}
        
        print(f"Final duplicates: {duplicates}")  # Debug print
        
        return duplicates

    except Exception as e:
        print(f"Error in parse_log_line: {str(e)}")  # Debug print
        return {"error": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        line = data.get('line', '')
        print(f"Received line: {line}")  # Debug print
        result = parse_log_line(line)
        print(f"Analysis result: {result}")  # Debug print
        return jsonify(result)
    except Exception as e:
        print(f"Error in analyze endpoint: {str(e)}")  # Debug print
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8001, host='127.0.0.1') 