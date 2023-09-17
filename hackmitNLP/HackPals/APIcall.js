function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    const currentState = "start";  // Replace with your actual state

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput, state: currentState }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Update your UI here
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
