import os
import pathlib
import platform
import re
import string
import subprocess
import time
import traceback

import cv2 as cv
import keyboard
import numpy as np
import pyautogui as pg
import pyperclip
import screeninfo
from PIL import ImageGrab
from pyunpack import Archive

if platform.system() == "Windows":
    import win32api
    import win32clipboard
    import win32con

archive = Archive


def regex(text, capitalize=False, lower=False, upper=False):

    regex_a = ["á", "à", "ã", "â", "ä", "Á", "À", "Ã", "Â", "Ä"]
    regex_e = ["é", "è", "ê", "ë", "É", "È", "Ê", "Ë"]
    regex_i = ["í", "ì", "î", "ï", "Í", "Ì", "Î", "Ï"]
    regex_o = ["ó", "ò", "ô", "õ", "ö", "Ó", "Ò", "Ô", "Õ", "Ö"]
    regex_u = ["ú", "ù", "û", "ü", "Ú", "Ù", "Û", "Ü"]
    regex_c = ["ç", "Ç"]
    regex_another_characters = ["&", ",", "-", "/"]

    for letter in regex_a:
        if letter.isupper():
            text = text.replace(letter, "A")
        else:
            text = text.replace(letter, "a")
    for letter in regex_e:
        if letter.isupper():
            text = text.replace(letter, "E")
        else:
            text = text.replace(letter, "e")

    for letter in regex_i:
        if letter.isupper():
            text = text.replace(letter, "I")
        else:
            text = text.replace(letter, "i")
    for letter in regex_o:
        if letter.isupper():
            text = text.replace(letter, "O")
        else:
            text = text.replace(letter, "o")
    for letter in regex_u:
        if letter.isupper():
            text = text.replace(letter, "U")
        else:
            text = text.replace(letter, "u")
    for letter in regex_c:
        if letter.isupper():
            text = text.replace(letter, "C")
        else:
            text = text.replace(letter, "c")
    for letter in regex_another_characters:
        text = text.replace(letter, "")
    if capitalize:
        return string.capwords(text)
    if lower:
        return text.lower()
    if upper:
        return text.upper()
    return text


def IS_CAPS_LOCK_ON():
    if platform.system() == "Windows":
        return win32api.GetKeyState(win32con.VK_CAPITAL)

    if platform.system() == "Linux":
        p1 = subprocess.Popen(["xset", "q"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "LED"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        out, err = p2.communicate()
        if out.decode("utf-8")[65] == "1":
            p2.terminate()
            return True
        else:
            return False


def IS_NUM_LOCK_ON():
    if platform.system() == "Windows":
        return win32api.GetKeyState(win32con.VK_NUMLOCK)


def decrement(value):
    value -= 1
    return value


def increment(value):
    value += 1
    return value


def get_clipboard():
    try:
        value = pyperclip.paste()
        print("The clipboard value is: ", value)
        return value

    except Exception as error:
        print(error)
        return ""


def setClipboardText(value: str):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(value, win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
    except Exception as error:
        print(":::: ERROR ON CLIPBOARD ::::")
        print(error)


def disable_capslock():
    is_on = IS_CAPS_LOCK_ON()
    if is_on:
        return keyboard.press_and_release("caps lock")


def disable_numlock():
    if IS_NUM_LOCK_ON():
        return keyboard.press_and_release("num lock")


def select_all():
    time.sleep(0.1)
    keyboard.press_and_release("home")
    time.sleep(0.1)
    keyboard.press("shift")
    time.sleep(0.1)
    keyboard.press_and_release("end")
    time.sleep(0.1)
    keyboard.release("shift")


def select_all_rows():
    time.sleep(0.1)
    keyboard.press("ctrl")
    time.sleep(0.1)
    select_all()
    time.sleep(0.1)
    keyboard.release("ctrl")


def clearClipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    return win32clipboard.CloseClipboard()


def copy_value(all_rows=False):
    disable_capslock()
    disable_numlock()
    pyperclip.copy("")  # clear clipboard
    select_all() if (not all_rows) else select_all_rows()
    time.sleep(0.1)
    keyboard.press("ctrl")
    time.sleep(0.1)
    keyboard.press_and_release("c")
    time.sleep(0.1)
    keyboard.release("ctrl")
    try:
        value = get_clipboard()
    except:
        value = ""
    print(value)
    return value


def verify_entered_value(value):
    print("Verifying if value was entered...")
    inserted_value = re.sub("[^a-zA-Z0-9\?]", "", copy_value())
    print("The value inserted is: ", inserted_value)
    value = re.sub("[^a-zA-Z0-9\?]", "", value)
    print(value)
    return inserted_value == value


def _get_monitor_points():
    for monitor in screeninfo.get_monitors():
        if monitor.is_primary:
            monitor_x = monitor.x
            monitor_y = monitor.y
            height = monitor.height
            width = monitor.width
            return (monitor_x, monitor_y, height, width)
    return (0, 0, 0, 0)


def __validate_methods_find_image(method):
    accepted_methods = [
        "cv.TM_CCOEFF",
        "cv.TM_CCOEFF_NORMED",
        "cv.TM_CCORR",
        "cv.TM_CCORR_NORMED",
        "cv.TM_SQDIFF",
        "cv.TM_SQDIFF_NORMED",
    ]
    if method not in accepted_methods:
        raise ValueError(f"METHOD MUST BE ONE OF {accepted_methods}")


def __get_image_to_find(image_to_find: str, region: tuple[int, int, int, int]):
    full_desktop_screenshot = ImageGrab.grab(bbox=region)
    full_desktop_screenshot = cv.cvtColor(
        np.array(full_desktop_screenshot), cv.COLOR_RGB2BGR
    )

    image_to_find = cv.imread(image_to_find)  # type: ignore
    return image_to_find, full_desktop_screenshot


def __treat_position_to_center(
    width_of_searched_image,
    height_of_searched_image,
    top_left_position,
    monitor_x,
    monitor_y,
):
    _x = int(top_left_position[0] + monitor_x)
    _x = int(_x + (width_of_searched_image / 2))
    _y = int(top_left_position[1] + monitor_y)
    _y = int(_y + (height_of_searched_image / 2))
    return _x, _y


def _find_image(
    image_to_find: str,
    method: str = "cv.TM_CCOEFF_NORMED",
    region: tuple[int, int, int, int] = None,
    accuracy: float = 0.95,
):
    monitor_x, monitor_y, height, width = _get_monitor_points()

    if region is None:
        region = (monitor_x, monitor_y, monitor_x + width, height)

    __validate_methods_find_image(method)
    image_to_find, full_desktop_screenshot = __get_image_to_find(image_to_find, region)
    _, _w, _h = image_to_find.shape[::-1]  # type: ignore

    res = cv.matchTemplate(
        image_to_find, full_desktop_screenshot, eval(method)
    )  # type: ignore
    min_val, located_accuracy, min_loc, finded_position = cv.minMaxLoc(res)

    if located_accuracy >= accuracy:
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left_position = min_loc
        else:
            top_left_position = finded_position
        _x, _y = __treat_position_to_center(
            _w, _h, top_left_position, monitor_x, monitor_y
        )
        return (_x, _y)
    else:
        return (None, None)


def exists(img, seconds: float = 5.0, accuracy=0.95) -> bool:
    """
    JA REALIZA O pg.locateCenterOnScreen(img, confidence=0.9)
    """
    seconds_counter = 0
    while True:

        if seconds_counter >= seconds:
            return False

        image = _find_image(img, accuracy=accuracy)

        if image != (None, None):
            return True

        time.sleep(0.1)
        seconds_counter = seconds_counter + 0.1


def wait_until_vanish(img):
    """
    JA REALIZA O pg.locateCenterOnScreen(img, confidence=0.9)
    """
    while True:
        time.sleep(1)
        image = _find_image(img)
        if image == (None, None):
            print("IMAGE VANISHED")
            return True


def verify_if_isnt_exists(img, message, time):
    if not exists(img, time):
        raise Exception(message)


def goto_pattern(_shortcut, img, message, modifier=True, TIME=10, LIMITER=3, key="alt"):
    if not LIMITER:
        return False

    if modifier:
        keyboard.press_and_release(key)

    time.sleep(0.2)
    keyboard.press_and_release(_shortcut)
    time.sleep(1)

    try:
        verify_if_isnt_exists(img, message, TIME)
        return True

    except Exception as error:
        print(error)
        print(traceback.print_exc())
        return goto_pattern(
            _shortcut, img, message, modifier, TIME, decrement(LIMITER), key
        )


def write(text, delay: float = 0.0, verify_text=True, LIMITER=5):
    if not LIMITER:
        pg.PAUSE = 0
        raise Exception("ERRO AO DIGITAR INFORMACAO")
    keyboard.write(text,delay=delay)
    if verify_text and not verify_entered_value(text):
        return write(text, delay, verify_text, decrement(LIMITER))
    pg.PAUSE = 0

def keyboard_hotkey(Key):
    pass

def fill_input(value, verify_text=True, modifier="tab", delay=0, seconds=0.5):
    write(value, delay=delay, verify_text=verify_text)
    if not modifier is None:
        keyboard.press_and_release(modifier, interval=delay)
    # if(not verify_entered_value(value)):
    #   return fill_input(value, modifier, time)

    # keyboard.press_and_release(modifier)
    time.sleep(seconds)


def click_if_exists(img, seconds=8, x=0, y=0, accuracy: float = 0.95):
    if exists(img, seconds, accuracy=accuracy):
        _x, _y = _find_image(img, accuracy=accuracy)  # type: ignore
        time.sleep(0.2)
        pg.click(_x + x, _y + y)


def to_click(img, seconds=8, x=0, y=0, accuracy: float = 0.90):
    """
    img = The image that will be clicked\n
    seconds = The time that will wait until the image shows up\n
    x = The X coordinate of the image if needs target another area\n
    y = The Y coordinate of the image if needs target another area\n
    """
    if exists(img, seconds, accuracy=accuracy):
        _x, _y = _find_image(img, accuracy=accuracy)  # type: ignore
        pg.click(_x + x, _y + y)

    else:
        raise Exception("IMAGE NOT EXISTS")

def right_click(img, seconds=8, x=0, y=0, accuracy: float = 0.90):
    """
    img = The image that will be clicked\n
    seconds = The time that will wait until the image shows up\n
    x = The X coordinate of the image if needs target another area\n
    y = The Y coordinate of the image if needs target another area\n
    """
    if exists(img, seconds, accuracy=accuracy):
        _x, _y = _find_image(img, accuracy=accuracy)  # type: ignore
        pg.click(_x + x, _y + y, button="right")

    else:
        raise Exception("IMAGE NOT EXISTS")


def double_click(img, seconds=8, x=0, y=0):
    """
    img = The image that will be clicked\n
    seconds = The time that will wait untill the image shows up\n
    x = The X coordinate of the image if needs target another area\n
    y = The Y coordinate of the image if needs target another area\n
    """
    if exists(img, seconds):
        _x, _y = _find_image(img)  # type: ignore
        pg.doubleClick(_x + x, _y + y)

    else:
        raise Exception("IMAGE NOT EXISTS")


def click_and_write(
    img, text, delay: float = 0.0, seconds=5, x=0, y=0, verify_text=True, LIMITER=3
):
    if not LIMITER:
        raise Exception("VALUE NOT INSERTED CORRECTLY!")
    if exists(img, seconds):
        _x, _y = _find_image(img)
        pg.click(_x + x, _y + y)
        select_all()
        write(text, delay=delay, verify_text=verify_text)

        if verify_text:
            verify_entered_value(text)
            return True
        if not verify_text:
            return True

    return click_and_write(
        img, text, delay, seconds, x, y, verify_text, decrement(LIMITER)
    )


def get_folder_from_file_path(path: str) -> str:
    regex = r"\.\w+"
    if re.search(regex, path, re.IGNORECASE):
        return os.path.dirname(os.path.abspath(path))
    return path


def execute(path, delay: float = 0.0, LIMITER=3):
    if not LIMITER:
        return False
    try:
        time.sleep(0.5)
        keyboard.press_and_release("win + r")
        write(path, delay=delay)
        keyboard.press_and_release("enter")
        return True
    except:
        return execute(path, delay, decrement(LIMITER))


def write_doc(path_doc, regs_doc, method="a+"):
    folder = get_folder_from_file_path(path_doc)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    with open(path_doc, method) as doc:
        doc.write(regs_doc)


def save_register(log_path, regs_company, name_process, company_code, company_name):
    def register(stage, status, message):
        write_doc(log_path, ("{}|{}|{}\n".format(regs_company, stage, status)))

    return register


def create_folder_os(path, print_error=True):
    try:
        os.system(f'if not exist "{path}" mkdir "{path}"')
        return True

    except Exception as e:
        if print_error:
            print(e)
        return False


def copy_file_os(origin, destiny):
    try:
        print(os.system(f'cmd.exe /c copy "{origin}" "{destiny}"'))
        return True
    except Exception as e:
        print(e)
        return False


def move_file_os(origin, destiny):
    try:
        print(os.system(f'move "{origin}" "{destiny}"'))
        return True
    except Exception as e:
        print(e)
        return False


def rename_and_move_file_os(src, dst):
    try:
        print(os.rename(src, dst))
        return True
    except Exception as e:
        print(e)
        return False


def remove_folder_os(path):
    rmdir = os.system(f'cmd.exe /c rmdir "{path}" /s /q')
    if not rmdir == 0:
        return False
    return True


def remove_files_os(path):
    try:
        print(os.system(f'cmd.exe /c del /f /q "{path}"'))
        return True
    except Exception as error:
        print(error)
        return False, "ERROR WHILE DELETING DIRECTORY"


def exclude_certification(index: int = 10):
    command = f"certutil -delstore -user My 0"
    for x in range(index):
        os.system(command)
    return True


def install_certification(password, path, file_name):
    command = (
        rf'certutil -f -user -p "{password}" -importpfx "{path}\{file_name}" NoExport'
    )
    output = subprocess.Popen(
        command, stdout=subprocess.PIPE, encoding="latin-1"
    ).communicate()[0]
    return output


def compress_file(
    origin, destiny, winrar_path: str = "c:\Program Files (x86)\WinRAR\WinRAR.exe"
):
    command = rf'"{winrar_path}" m -ep1 -idq -r -y "{destiny}" "{origin}"'
    return execute(command)


def unzip_file(compact_file, destiny):
    return archive(compact_file).extractall(destiny)


def close_windows(index: int):
    for x in range(index):
        keyboard.press_and_release("alt+f4")
        time.sleep(1)


# def hotkey(*keys, seconds=2):
#     time.sleep(seconds)
#     pg.hotkey(*keys)

def hotkey(*keys, seconds=2):
    time.sleep(seconds)
    for key in keys:
        keyboard.press(key)
    for key in keys[::-1]:
        keyboard.release(key)


def moveToPosition(x, y, duration=0.25):
    pg.moveTo(x, y, duration=duration)


def take_app_screenshot(path_to_save: pathlib.Path, filename: str = "ERRO_EXECUCAO"):
    try:
        if not path_to_save.is_dir():
            raise Exception("Caminho não encontrado!")

        if not filename.endswith(".png"):
            filename += ".png"
        screenshot_file = str(path_to_save / filename)
        pg.screenshot(screenshot_file)
    except:
        raise Exception("Erro ao tirar screenshoot")

def click_on_image_by_offset(path_to_image: pathlib.Path, x=0, y=0, wait = 0):
    time.sleep(wait)
    icon_location = pg.locateOnScreen(path_to_image)
    img_center = pg.center(icon_location)
    img_x, img_y = img_center
    pg.moveTo(img_x, img_y)
    time.sleep(wait)

    pg.click(img_x + x, img_y + y)

def move_and_scroll(scroll_number, path_to_image: pathlib.Path, x=0, y=0, wait = 0):
    time.sleep(wait)
    icon_location = pg.locateOnScreen(path_to_image, confidence=0.9)
    img_center = pg.center(icon_location)
    img_x, img_y = img_center
    pg.moveTo(img_x + x, img_y + y)
    time.sleep(wait)

    pg.scroll(scroll_number)
