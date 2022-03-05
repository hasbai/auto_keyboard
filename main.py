import json
import os
import threading
import time
from datetime import datetime

import pydirectinput
from pynput import keyboard, mouse


def mouse_click(button: str, pressed: bool, x: int, y: int):
    if pressed:
        pydirectinput.mouseDown(button=button, x=x, y=y)
    else:
        pydirectinput.mouseUp(button=button, x=x, y=y)


def keyboard_click(key: str):
    pydirectinput.keyDown(key)
    pydirectinput.keyUp(key)


def time_delay() -> int:
    global timestamp
    now = time.time()
    delay = now - timestamp
    timestamp = now
    return int(delay * 1000)


def run_script(script: list) -> int:
    for i in range(config.get('repeat_times', 1)):
        for command in script:
            if not running:
                return -1
            time.sleep(command[0] / 1000)
            if command[1] == 'keyboard':
                keyboard_click(command[2])
            elif command[1] == 'mouse':
                mouse_click(*command[2:])
    return 0


def run():
    global running

    files = os.listdir(SCRIPT_DIR)
    if not files:
        print('no script recorded yet')
    else:
        file = config.get('current_script', '') or files[0]
        with open(f'{SCRIPT_DIR}/{file}') as f:
            script = json.load(f)
        if run_script(script) == 0:
            print('completed running')
        else:
            print('stopped running')
    running = False


def on_keyboard_press(key):
    global running
    global recording
    global record_data

    # print(f'key pressed: {key}')

    if key == keyboard.Key.esc:
        print('exit......')
        keyboard_listener.stop()
        mouse_listener.stop()
    elif key == keyboard.Key.f6:
        if not running:
            running = True
            threading.Thread(target=run).start()
            print('start running')
        else:
            running = False
    elif key == keyboard.Key.f7:
        if not recording:
            recording = True
            print('start recording')
        else:
            recording = False
            print('end recording')
            filename = f'{SCRIPT_DIR}/{datetime.now().isoformat().replace(":", "-")}.json'
            with open(filename, 'w') as f:
                json.dump(record_data, f)
            print(f'script written to {filename}')
            record_data = []
    elif recording:
        if hasattr(key, 'char'):
            key = key.char
        elif hasattr(key, 'name'):
            key = key.name
        record_data.append([time_delay(), 'keyboard', key])


def on_mouse_click(x, y, button, pressed):
    if recording:
        button = str(button).split('.')[-1]
        record_data.append([time_delay(), 'mouse', button, pressed, x, y])


if __name__ == '__main__':
    SCRIPT_DIR = 'scripts'
    CONFIG_FILE = 'config.json'
    if not os.path.exists(SCRIPT_DIR):
        os.makedirs(SCRIPT_DIR)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'current_script': '', 'repeat_times': 1}, f)
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    running = False
    recording = False
    record_data = []
    timestamp = time.time()

    print('F6开始/停止，F7录制/停止录制，ESC退出')
    print(f'当前脚本为：{config.get("current_script", "")}')
    print(f'循环次数为：{config.get("repeat_times", 1)}')

    keyboard_listener = keyboard.Listener(on_press=on_keyboard_press)
    mouse_listener = mouse.Listener(on_click=on_mouse_click)
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()
