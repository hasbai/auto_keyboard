# Auto Keyboard ---- python 实现的按键精灵

## Features

- 录制脚本并运行
- 可调节运行次数
- 使用 PyDirectInput 库，可以在游戏中正常使用

## Build

windows

```shell
pyinstaller -F \
  --hidden-import "pynput.keyboard._win32" \
  --hidden-import "pynput.mouse._win32" \
  main.py
```

linux

```shell
pyinstaller -F \
  --hidden-import "pynput.keyboard._xorg" \
  --hidden-import "pynput.mouse._xorg" \
  main.py
```

## Usage

F6 开始运行 / 停止运行

F7 录制 / 停止录制

ESC 退出

程序运行后会在同级目录下生成脚本目录 scripts 和配置文件 config.json，用户可自行配置 current_script 和 repeat_times 的选项

脚本数据格式：Array<Array[3 or 6]>

| index | type | description                                            |
| ----- | ---- | ------------------------------------------------------ |
| 0     | int  | 等待时间（毫秒），等待后执行当前命令                   |
| 1     | str  | 输入设备类型，目前支持 keyboard 和 mouse               |
| 2     | str  | 键位名称，支持大部分键盘键位和鼠标的 left right middle |
| 3     | bool | （仅鼠标）true 为按下按键，false 为松开按键            |
| 4     | int  | （仅鼠标）点击的 x 坐标                                |
| 5     | int  | （仅鼠标）点击的 y 坐标                                |

样例：

```json
[
  [
    88,
    "mouse",
    "right",
    true,
    1280,
    720
  ],
  [
    119,
    "mouse",
    "right",
    false,
    1280,
    720
  ],
  [
    2500,
    "keyboard",
    "e"
  ]
]

```
