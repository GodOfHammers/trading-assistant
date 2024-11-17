// frontend/src/services/websocket.ts

type MessageHandler = (data: any) => void;

export class WebSocketService {
  private ws: WebSocket | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout: number | null = null;  // Changed from NodeJS.Timeout

  connect(url: string) {
    this.ws = new WebSocket(url);

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.notifyHandlers(data.type, data.payload);
      } catch (error) {
        console.error('WebSocket message parsing error:', error);
      }
    };

    this.ws.onclose = () => {
      this.attemptReconnect(url);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  private attemptReconnect(url: string) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      const timeout = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      
      // Changed to use window.setTimeout
      this.reconnectTimeout = window.setTimeout(() => {
        this.reconnectAttempts++;
        this.connect(url);
      }, timeout);
    }
  }

  subscribe(type: string, handler: MessageHandler) {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set());
    }
    this.handlers.get(type)?.add(handler);

    return () => {
      this.handlers.get(type)?.delete(handler);
    };
  }

  private notifyHandlers(type: string, data: any) {
    this.handlers.get(type)?.forEach(handler => {
      try {
        handler(data);
      } catch (error) {
        console.error('Handler execution error:', error);
      }
    });
  }

  disconnect() {
    if (this.reconnectTimeout) {
      window.clearTimeout(this.reconnectTimeout);
    }
    this.ws?.close();
    this.ws = null;
    this.handlers.clear();
    this.reconnectAttempts = 0;
  }
}

export const wsService = new WebSocketService();