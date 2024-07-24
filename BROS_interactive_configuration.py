import asyncio
import base64
import time
import cv2
import websockets
import json
from sensor.camera import ThreadedCamera, ProcessedFrame
from logger_br import logger


# 命令处理函数
async def set_camera_threshold(data):
    threshold = data['threshold']
    logger.info(f"Setting camera threshold to {threshold}")
    camera.thresh = threshold
    time.sleep(camera.fps_sleep * 5)
    frame: ProcessedFrame = camera.processed_frame

    # if frame is no None, then return a base64 encoded img
    if frame is not None:
        # encode img
        _, img = cv2.imencode('.jpg', frame.frame)
        img_base64 = base64.b64encode(img.tobytes()).decode('utf-8')
        # add header
        img_base64 = f"data:image/jpeg;base64,{img_base64}"
        return {"status": "success", "img": img_base64}

    return {"status": "error", "img": None}


async def another_command(data):
    # 添加其他命令的处理逻辑
    return "Another command executed"


# 命令到函数的映射
command_handlers = {
    "set_camera_threshold": set_camera_threshold,
    "another_command": another_command,
}


async def handle_command(data):
    command = data.get('cmd')
    if command in command_handlers:
        response = await command_handlers[command](data['data'])
        return response
    else:
        return "Unknown command"


async def server(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        logger.debug(f"Received: {data}")
        response = await handle_command(data)
        await websocket.send(json.dumps({"cmd": data.get('cmd'), "data": response}))


if __name__ == "__main__":
    camera = ThreadedCamera('BROS-camera', fps=10, interactive_debug=True)

    start_server = websockets.serve(server, "localhost", 10502)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
