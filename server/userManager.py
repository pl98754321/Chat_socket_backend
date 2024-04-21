from typing import List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.rooms: dict[str, list[str]] = {}

    async def connect_user(self, websocket: WebSocket, user_id: str, room_name: str):
        self.active_connections[user_id] = websocket

    def disconnect_user(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        for room in self.rooms.values():
            if user_id in room:
                room.remove(user_id)

    async def send_all_user_in_room(self, room_id: str):
        massage_all_user = ""
        for user_id in self.rooms[room_id]:
            massage_all_user += user_id + " "
        for user_id in self.rooms[room_id]:
            try:
                await self.send_personal_message(massage_all_user, user_id)
            except Exception as e:
                print(e)

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(message)

    async def send_room_message(self, message: str, room_id: str):
        if room_id in self.rooms:
            for user_id in self.rooms[room_id]:
                try:
                    await self.send_personal_message(message, user_id)
                except Exception as e:
                    print(e)

    def add_user_to_room(self, user_id: str, room_id: str):
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append(user_id)

    def remove_user_from_room(self, user_id: str, room_id: str):
        if room_id in self.rooms and user_id in self.rooms[room_id]:
            self.rooms[room_id].remove(user_id)


from fastapi import WebSocket


class UserManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect_user(self, websocket: WebSocket):
        self.active_connections.append(websocket)
        return "User" + str(len(self.active_connections))

    def disconnect_user(self, user_id):
        self.active_connections.remove(user_id)

    async def broadcast_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
