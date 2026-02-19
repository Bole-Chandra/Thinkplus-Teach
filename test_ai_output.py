import urllib.request
import urllib.parse
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def run_demo_test():
    try:
        # A completely unique and long text to get a high score
        new_text = "The rapid evolution of quantum computing represents a paradigm shift in computational science. Unlike classical bits, qubits leverage superposition and entanglement to solve complex problems in cryptography and materials science that were previously thought to be intractable."
        
        data = {"student": 1, "assignment": 1, "text_content": new_text}
        payload = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/submissions/", data=payload, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            output = {
                "submission_id": f"S{res_data['id']}",
                "plagiarism_risk": f"{res_data['plagiarism_score']:.1f}%",
                "feedback_summary": res_data['feedback'],
                "score": res_data.get('grade', 0)
            }
            with open('output_log.json', 'w') as f:
                json.dump(output, f, indent=4)
    except Exception as e:
        with open('output_log.json', 'w') as f:
            f.write(str(e))

if __name__ == "__main__":
    run_demo_test()
