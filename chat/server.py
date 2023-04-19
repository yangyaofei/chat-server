# coding=utf-8
import json
import typing

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_offline import FastAPIOffline
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from chat.model.chat_glm import ChatGLM
from chat.schemas import ChatResponse, ChatRequest


class NanJSONResponse(JSONResponse):
    # parse Nan to 'NaN' inside null

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=True,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


app = FastAPIOffline(default_response_class=NanJSONResponse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat = ChatGLM()


@app.post(
    "/chat/request",
    response_model=ChatResponse,
)
def chat_request(
        body: ChatRequest,
) -> ChatResponse:
    response, history = chat.chat(body.query, body.history)
    return ChatResponse(answer=response, history=history)


@app.websocket(
    "/chat/request-ws",
    # response_model=ChatResponse,
)
async def chat_request_websocket(
        websocket: WebSocket,
):
    await websocket.accept()
    try:
        json_data = await websocket.receive_json()
        body: ChatRequest = ChatRequest(**json_data)
    except json.decoder.JSONDecodeError:
        await websocket.send_text("Invalid JSON")
        await websocket.close()
        return
    except ValidationError as e:
        await websocket.send_text(e.json())
        await websocket.close()
        return
    try:
        for response, history in chat.stream_chat(body.query, body.history):
            await websocket.send_text(ChatResponse(answer=response, history=history).json(ensure_ascii=False))
    except WebSocketDisconnect:
        pass
    await websocket.close()
