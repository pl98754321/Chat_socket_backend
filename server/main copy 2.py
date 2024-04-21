from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from .userManager import UserManager

app = FastAPI()
user_manager = UserManager()


@app.get("/")
async def get():
    with open("client/templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    user_id = await user_manager.connect_user(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await user_manager.broadcast_message(f"User {user_id}: {data}")
    except WebSocketDisconnect:
        user_manager.disconnect_user(user_id)
        await user_manager.broadcast_message(f"User {user_id} left the chat")
