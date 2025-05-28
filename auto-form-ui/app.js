// filepath: auto-form-ui/app.js
console.log("app.js loaded");
class ChatApp {
    constructor() {
        console.log('ChatApp constructor called');
        this.socket = null;
        this.initializeElements();
        this.setupEventListeners();
        this.connectWebSocket();
    }

    initializeElements() {
        console.log('Initializing DOM elements');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.name = document.getElementById('name');
        this.email = document.getElementById('email');
        this.message = document.getElementById('message');
        this.autoFillButton = document.getElementById('autoFillButton');
    }

    setupEventListeners() {
        console.log('Setting up event listeners');
        this.sendButton.addEventListener('click', () => this.sendMessage())
        this.messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.sendMessage();
            }
        });
        if (this.autoFillButton) {
            this.autoFillButton.addEventListener('click', () => this.startAutoFill());
        }
    }

    startAutoFill() {
        console.log('startAutoFill called');
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            console.log('WebSocket not open, connecting...');
            this.connectWebSocket();
            setTimeout(() => this.sendAutoFillRequest(), 500); // Wait for connection
        } else {
            this.sendAutoFillRequest();
        }
    }

    sendAutoFillRequest() {
        console.log('Sending auto-fill request');
        this.socket.send(JSON.stringify({ type: 'start_auto_fill' }));
        this.addSystemMessage('Started auto-fill Q&A session.');
    }

    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const host = window.location.hostname; // Use localhost if hostname is not available
        const port = 8080; // Default port for WebSocket, adjust if needed
        const wsUrl = `${protocol}://${host}:${port}/ws`;

        console.log('Connecting to WebSocket:', wsUrl);

        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = () => {
            console.log('WebSocket connection established');
            this.sendButton.disabled = false;
            this.messageInput.disabled = false;
        }
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Message received:', data);
            this.handleMessage(data);
        };
        this.socket.onclose = () => {
            console.log('WebSocket connection closed');
            this.addSystemMessage('Disconnected from chat server');
            setTimeout(() => this.connectWebSocket(), 5000);
        };
        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.addSystemMessage('Connection error occurred');
        };
    }

    handleMessage(data) {
        console.log('Handling message:', data);
        if (data.type === 'system') {
            this.addSystemMessage(data.message);
        } else if (data.type === 'status') {
            this.addStatusMessage(data.message);
            this.showNotification('info', data.message);
        } else if (data.type === 'question') {
            this.addMessage(data.question, 'received');
            this.awaitingField = data.field;
            console.log('Awaiting field:', data.field);
        } else if (data.type === 'field_value') {
            this.setFormField(data.field, data.value);
            this.addMessage(`Filled ${data.field}: ${data.value}`, 'received');
        } else {
            this.addMessage(data.text, 'received', data.field_value);
        }
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        console.log('sendMessage called with:', message);
        if (!message || !this.socket || this.socket.readyState !== WebSocket.OPEN) return;

        if (this.awaitingField) {
            console.log('Sending field answer for:', this.awaitingField);
            this.socket.send(JSON.stringify({ type: 'field_answer', field: this.awaitingField, value: message }));
            this.awaitingField = null;
        } else {
            const data = { text: message };
            this.socket.send(JSON.stringify(data));
        }
        this.addMessage(message, 'sent');
        this.messageInput.value = '';
    }

    setFormField(field, value) {
        console.log(`Setting form field ${field} to ${value}`);
        if (this[field]) {
            this[field].value = value;
        }
    }
    addMessage(text, type, field_value = null) {
        console.log(`Adding message: ${text}, type: ${type}`);
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    addSystemMessage(message) {
        console.log(`Adding system message: ${message}`);
        const systemDiv = document.createElement('div');
        systemDiv.className = 'message system';
        systemDiv.textContent = message;
        this.chatMessages.appendChild(systemDiv);
        this.scrollToBottom();
    }
    addStatusMessage(message) {
        console.log(`Adding status message: ${message}`);
        const statusDiv = document.createElement('div');
        statusDiv.className = 'message status';
        statusDiv.textContent = message;
        this.chatMessages.appendChild(statusDiv);
        this.scrollToBottom();
    }
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Initialize the chat application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});