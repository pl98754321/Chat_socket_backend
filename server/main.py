import secrets

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .userManager import ConnectionManager

app = FastAPI()
conn_manager = ConnectionManager()


@app.get("/")
async def get():
    return {"message": "Hello World"}


@app.websocket("/ws/main")
async def websocket_endpoint_main(websocket: WebSocket):
    await websocket.accept()
    # generate a user id
    user_id = secrets.token_hex(8)
    await conn_manager.connect_user(websocket, user_id, "main")
    conn_manager.add_user_to_room(user_id, "main")
    await conn_manager.send_all_user_in_room("main")
    try:
        while True:
            data = await websocket.receive()
            await conn_manager.send_room_message(f"{user_id}: {data} ", "main")
    except WebSocketDisconnect:
        conn_manager.remove_user_from_room(user_id, data["room"])
        conn_manager.disconnect_user(user_id)
        await conn_manager.send_room_message(f"User {user_id} left the chat", "general")


@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    await websocket.accept()
    # generate a user id
    user_id = secrets.token_hex(8)
    await conn_manager.connect_user(websocket, user_id, room_name)
    conn_manager.add_user_to_room(user_id, room_name)
    try:
        while True:
            data = await websocket.receive()
            await conn_manager.send_room_message(f"{user_id}: {data} ", room_name)
    except WebSocketDisconnect:
        conn_manager.remove_user_from_room(user_id, data["room"])
        conn_manager.disconnect_user(user_id)
        await conn_manager.send_room_message(f"User {user_id} left the chat", "general")
