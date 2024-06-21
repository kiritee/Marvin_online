$(document).ready(function() {
    $('.chat-button').on('click', function() {
        $('.chat-button').css({"display": "none"});
        $('.chat-box').css({"visibility": "visible"});
    });

    $('.chat-box .chat-box-header p').on('click', function() {
        $('.chat-button').css({"display": "block"});
        $('.chat-box').css({"visibility": "hidden"});
    });

    $("#addExtra").on("click", function() {
        $("#fileInput").click();
    });

    $("#fileInput").on("change", function() {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            $.ajax({
                url: '/upload',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    console.log('File uploaded successfully');
                    const messagesContainer = document.getElementById('messages');
                    messagesContainer.innerHTML += `<div class="chat-box-body-receive"><p>${response.response}</p><span>${new Date().toLocaleTimeString()}</span></div>`;
                },
                error: function(response) {
                    alert('Error uploading file');
                }
            });
        } else {
            alert('No file selected');
        }
    });

    $('#message-input').on('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
});

async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value;
    if (message.trim() === '') return;

    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML += `<div class="chat-box-body-send"><p>${message}</p><span>${new Date().toLocaleTimeString()}</span></div>`;

    input.value = '';

    const session_id = "{{ session.id }}";

    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message, session_id })
    });

    const data = await response.json();
    messagesContainer.innerHTML += `<div class="chat-box-body-receive"><p>${data.response}</p><span>${new Date().toLocaleTimeString()}</span></div>`;
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
