let dataText = ["sustainability", "education", "interactive media"];
let textContainer = document.getElementById("typed-output");
let interval;
let currentText = "";
let textIndex = 0;
let charIndex = 0;

function typeText() {
    if (charIndex < dataText[textIndex].length) {
        currentText += dataText[textIndex].charAt(charIndex);
        textContainer.innerHTML = currentText;
        charIndex++;
        setTimeout(typeText, 100);
    } else {
        setTimeout(eraseText, 2000);
    }
}

function eraseText() {
    if (charIndex > 0) {
        currentText = currentText.slice(0, -1);
        textContainer.innerHTML = currentText;
        charIndex--;
        setTimeout(eraseText, 100);
    } else {
        textIndex++;
        if (textIndex >= dataText.length) textIndex = 0;
        setTimeout(typeText, 1000);
    }
}

typeText();

let i = 0;
const txt = 'sustainability';  // The text to be typed
const speed = 100; 

function typeEffect() {
    if (i < txt.length) {
        document.getElementById("typed-output").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeEffect, speed);
    }
}

typeEffect();

function sendMessage() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('input-field');

    if (userInput.value.trim() === '') {
        return;  
    }

    // User's Message
    let userMessage = document.createElement('div');
    userMessage.textContent = userInput.value;
    userMessage.style.textAlign = 'left';
    userMessage.style.backgroundColor = "#ADD8E6";
    userMessage.style.borderRadius = "10px";
    userMessage.style.padding = "10px";
    userMessage.style.margin = "10px";
    chatBox.appendChild(userMessage);

    // Call to Flask server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: userInput.value
        })
    })
    .then(response => response.json())
    .then(data => {
        let botMessage = document.createElement('div');
        botMessage.textContent = data.response;  // get the response from Flask
        botMessage.style.textAlign = 'right';
        botMessage.style.backgroundColor = "#F9DA82";
        botMessage.style.borderRadius = "10px";
        botMessage.style.padding = "10px";
        botMessage.style.margin = "10px";
        chatBox.appendChild(botMessage);
    });

    userInput.value = '';  
}



const inputField = document.getElementById('input-field');

inputField.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();  
        sendMessage();
    }
});
