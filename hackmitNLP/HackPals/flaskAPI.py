from flask import Flask, request, jsonify
from hackMIT import run_hackMIT
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('user_input')
    state = data.get('state', 'start')

    next_state, response = run_hackMIT(state, user_input)

    return jsonify({'state': next_state, 'response': response})




