class WebSocketService {
  constructor() {
    this.ws = null;
    this.listeners = {};
  }

  connect(url) {
    this.ws = new WebSocket(url);
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const handlers = this.listeners[data.type] || [];
      handlers.forEach(handler => handler(data));
    };
    this.ws.onclose = () => {
      setTimeout(() => this.connect(url), 3000);
    };
  }

  on(eventType, handler) {
    if (!this.listeners[eventType]) {
      this.listeners[eventType] = [];
    }
    this.listeners[eventType].push(handler);
  }

  send(data) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect() {
    this.ws?.close();
    this.listeners = {};
  }
}

export default new WebSocketService();
