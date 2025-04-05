from flask import Flask
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World from Chandu!"

@app.route('/compute')
def compute():
    start_time = time.time()
    result = sum(i * i for i in range(10_000))  # Simulating CPU-intensive task
    end_time = time.time()
    return f"Computation done in {end_time - start_time:.4f} seconds"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
