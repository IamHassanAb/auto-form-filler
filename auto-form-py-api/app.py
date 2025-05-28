import logging
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from states.fieldsState import FieldsState
from pds.RequestDS import RequestDS
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI()

fields = [
    RequestDS(field_name="name", field_description="The Name of the person filling the form"),
    RequestDS(field_name="email", field_description="The email address of the person filling the form"),
    RequestDS(field_name="message", field_description="The message or feedback of the person filling the form"),
]


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    state = FieldsState()
    logging.info("WebSocket connection accepted.")
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"Received data: {data}")
            if data:
                try:
                    msg = json.loads(data)
                except Exception:
                    msg = {"type": "text", "text": data}
                if msg.get("type") == "start_auto_fill":
                    logging.info("Starting auto-fill process.")
                    for field in fields:
                        question = state.ask(repr(field))
                        field.question = question
                        logging.info(f"Asking question for field '{field.field_name}': {question}")
                        await websocket.send_text(json.dumps({
                            "type": "question",
                            "field": field.field_name,
                            "question": field.question
                        }))
                        answer_data = await websocket.receive_text()
                        logging.info(f"Received answer for field '{field.field_name}': {answer_data}")
                        answer_msg = json.loads(answer_data)
                        field.answer = answer_msg.get("value", "")
                        field_value = state.process(field)
                        logging.info(f"Processed value for field '{field.field_name}': {field_value}")
                        await websocket.send_text(json.dumps({
                            "type": "field_value",
                            "field": field.field_name,
                            "value": field_value
                        }))
                    logging.info("Form auto-fill complete.")
                    await websocket.send_text(json.dumps({
                        "type": "system",
                        "message": "Form auto-fill complete."
                    }))
                else:
                    logging.info(f"Echoing message: {msg.get('text', data)}")
                    await websocket.send_text(json.dumps({
                        "type": "system",
                        "message": f"Echo: {msg.get('text', data)}"
                    }))
    except Exception as e:
        logging.error(f"WebSocket connection closed with error: {e}")
        await websocket.close()
