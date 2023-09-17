from flask import Flask, request, jsonify
from hackMIT import df  # Import your DialogueFlow object from hackpal.py

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')  # Get user input from POST request payload
    state = 'start'  # Initialize to the start state of your DialogueFlow
    response = ''

    # Execute your chatbot logic here
    # For example, you could call df.run() or similar to get the response
    # This is a placeholder; replace with your actual logic
    if state == 'start':
        response = "Hey! I'm HackPal, here to help brainstorm your hackathon ideas! What's your name?"
        state = 'get_name'
    elif state == 'get_name':
        # ... (your logic here)
        pass
    # ... (more states and logic)

    return jsonify({'response': response, 'state': state})


if __name__ == '__main__':
    app.run(debug=True)