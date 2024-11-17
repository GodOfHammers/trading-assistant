# backend/api/websocket.py

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, List
import json
import asyncio
import logging

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.running_tasks = set()
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Connect new client."""
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = set()
        self.active_connections[client_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        """Disconnect client."""
        self.active_connections[client_id].remove(websocket)
        if not self.active_connections[client_id]:
            del self.active_connections[client_id]
    
    async def broadcast_update(self, client_id: str, data: Dict):
        """Broadcast update to specific client."""
        if client_id in self.active_connections:
            dead_connections = set()
            for connection in self.active_connections[client_id]:
                try:
                    await connection.send_json(data)
                except Exception as e:
                    logging.error(f"Broadcast error: {str(e)}")
                    dead_connections.add(connection)
            
            # Clean up dead connections
            for dead in dead_connections:
                self.active_connections[client_id].remove(dead)
    
    async def start_streaming(self, client_id: str, symbols: List[str]):
        """Start streaming updates for symbols."""
        task = asyncio.create_task(
            self._stream_updates(client_id, symbols)
        )
        self.running_tasks.add(task)
        task.add_done_callback(self.running_tasks.remove)
    
    async def _stream_updates(self, client_id: str, symbols: List[str]):
        """Stream real-time updates."""
        try:
            while True:
                for symbol in symbols:
                    try:
                        # Get latest data
                        price_data = await data_service.get_real_time_price(symbol)
                        analysis = await trading_engine.get_quick_analysis(symbol)
                        
                        # Send update
                        await self.broadcast_update(
                            client_id,
                            {
                                'type': 'price_update',
                                'symbol': symbol,
                                'data': {
                                    'price': price_data,
                                    'analysis': analysis
                                }
                            }
                        )
                        
                    except Exception as e:
                        logging.error(f"Stream error for {symbol}: {str(e)}")
                        continue
                        
                await asyncio.sleep(1)  # Update every second
                
        except asyncio.CancelledError:
            logging.info(f"Streaming stopped for client {client_id}")
        except Exception as e:
            logging.error(f"Streaming error: {str(e)}")

socket_manager = WebSocketManager()

async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    symbols: List[str]
):
    """WebSocket endpoint for real-time updates."""
    try:
        await socket_manager.connect(websocket, client_id)
        await socket_manager.start_streaming(client_id, symbols)
        
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle client messages
                if message['type'] == 'subscribe':
                    await socket_manager.start_streaming(
                        client_id,
                        message['symbols']
                    )
                elif message['type'] == 'unsubscribe':
                    # Handle unsubscribe
                    pass
                
        except WebSocketDisconnect:
            socket_manager.disconnect(websocket, client_id)
            
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
        if websocket in socket_manager.active_connections.get(client_id, set()):
            socket_manager.disconnect(websocket, client_id)