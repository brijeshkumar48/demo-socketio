import datetime
from urllib.parse import parse_qs

import socketio
from termcolor import colored

# Start Server: uvicorn socket_test.asgi:application --host 127.0.0.1 --port 8080
# daphne -b 127.0.0.1 -p 8080 socket_test.asgi:application

# Initialize the Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid, environ):
    try:
        query_string = environ.get("QUERY_STRING", "")
        query_params = parse_qs(query_string)
        user_id = query_params.get("userId", [None])[0]
        org_id = query_params.get("orgId", [None])[0]

        if user_id and org_id:
            org_room = f"org_{org_id}"
            sio.enter_room(sid, org_room)
            data = {
                "userId": user_id,
                "orgId": org_id,
                "status": "success",
                "message": "Socket Connection created Successfully",
                "eventName": "connect",
                "date_time": str(datetime.datetime.now()),
                "room": org_room,
            }
            await sio.emit("connect", data, room=sid)

            message = f"Socketio connection created successfully for user: {user_id} in organization: {org_id}"
            print(colored(message, "green", attrs=["bold"]))

        else:
            await sio.disconnect(sid)
            print(f"Invalid connection attempt by {sid}. Missing userId or orgId.")

    except Exception as e:
        print(f"Error during connect event: {e}")


@sio.event
async def disconnect(sid):
    print(f"======User disconnected: {sid}=======")


@sio.event
async def send_message(sid, data):
    try:
        room = data.get("room")
        message = data.get("message")

        if room and message:
            print(f"======Message from {sid} to room {room}: {message}=======")
            data = {"sid": sid, "message": message, "room": room}
            await sio.emit("receive_message", data, room=room)

        else:
            print(f"Invalid send_message event data from {sid}: Missing room or message.")

    except Exception as e:
        print(f"Error handling send_message event from {sid}: {e}")
