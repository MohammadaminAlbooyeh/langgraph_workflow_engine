import { useEffect } from 'react';
import wsService from '../services/websocket';

export function useWebSocket(eventType, handler) {
  useEffect(() => {
    wsService.on(eventType, handler);
    return () => { };
  }, [eventType, handler]);
}
