import logging
import re
import subprocess
from dataclasses import dataclass
from time import sleep
from screeninfo import Monitor, get_monitors

logger = logging.getLogger()
monitors = get_monitors()


OFFSET_LEFT = 70


@dataclass
class WindowDimension:
    abs_left_x: int
    abs_left_y: int
    rel_left_x: int
    rel_left_y: int
    width: int
    height: int


def get_active_window_id() -> str:
    return subprocess.check_output(['xdotool', 'getactivewindow']).decode().strip()


def reset_window():

    return subprocess.call(
        ['wmctrl', '-i', '-r', get_active_window_id(), '-b', 'remove,maximized_vert,maximized_horz'])


def window_move_resize(x: int, y: int, width: int, height: int):

    x += OFFSET_LEFT
    reset_window()
    cmd = ['wmctrl', '-i', '-r', get_active_window_id(), '-e', f'1,{x},{y},{width},{height}']
    logger.debug(f"Running cmd: '{' '.join(cmd)}'")
    return subprocess.check_output(cmd)


def get_monitor(x) -> Monitor:
    for i, monitor in enumerate(monitors):
        logger.debug(f"monitor {i} width: {monitor.width}")
        logger.debug(f"monitor {i} height: {monitor.height}")
        logger.debug(f"monitor {i} x: {monitor.x}")
        logger.debug(f"monitor {i} y: {monitor.y}\n")

        if monitor.x <= x <= monitor.x + monitor.width:
            return monitor


def get_window_dimensions() -> WindowDimension:
    win_info = subprocess.check_output(['xwininfo', '-id', get_active_window_id()]).decode()
    logger.debug(win_info)
    abs_left_x = int(re.findall('Absolute upper-left X:  (\d*)', win_info)[0])
    abs_left_y = int(re.findall('Absolute upper-left Y:  (\d*)', win_info)[0])
    rel_left_x = int(re.findall('Relative upper-left X:  (\d*)', win_info)[0])
    rel_left_y = int(re.findall('Relative upper-left Y:  (\d*)', win_info)[0])
    width = int(re.findall('Width: (\d*)', win_info)[0])
    height = int(re.findall('Height: (\d*)', win_info)[0])
    return WindowDimension(
        abs_left_x=abs_left_x, abs_left_y=abs_left_y,
        rel_left_x=rel_left_x, rel_left_y=rel_left_y,
        width=width, height=height)


def configure_logging(verbose: int):
    loglevel = logging.WARNING
    if verbose >= 2:
        loglevel = logging.DEBUG
    elif verbose >= 1:
        loglevel = logging.INFO
    logging.basicConfig(level=loglevel)


def move_window_left():
    dimension = get_window_dimensions()
    win_mon = get_monitor(dimension.abs_left_x)
    logger.debug(f"window monitor: {win_mon}")
    window_move_resize(
            win_mon.x, win_mon.y,
            int(800), int(600))

def run():
    sleep(3)
    move_window_left()