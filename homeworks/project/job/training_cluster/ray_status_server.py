from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route("/ray_status", methods=["GET"])
def ray_status():
    try:
        result = subprocess.run(["ray", "status"], capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({"status": "success", "output": result.stdout})
        
        else:
            return jsonify({"status": "error", "error": result.stderr}), 500
        
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)