from aiogram import Dispatcher, types, Bot, executor 
from pytube import YouTube
import os
from config import TOKEN_API


bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start_msg(message: types.Message):
    '''Ответ бота на команды /start и /help'''
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Привет! Я могу скачивать видео с YouTube. Отправь мне ссылку!')


@dp.message_handler()
async def text_message(message: types.Message):
    '''Ответ бота на ссылку и инициация скачивания видео'''
    chat_id = message.chat.id
    url = message.text
    yt = YouTube(url)
    if message.text.startswith == 'https://youtu.be/' or 'https://www.youtube.com/':
        await bot.send_message(chat_id, f'Скачиваю видео {yt.title} с канала {yt.author}')
        await downloader_video(url, message, bot)


async def downloader_video(url, message, bot):
    '''Скачивает видео с ютуба и отправляет пользователю'''
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4')
    stream.get_highest_resolution().download(f'{message.chat.id}', f'{message.chat.id}_{yt.title}')
    with open(f'{message.chat.id}/{message.chat.id}_{yt.title}', 'rb') as video:
        await bot.send_video(message.chat.id, video, caption='Вот ваше видео!')
        os.remove(f'{message.chat.id}/{message.chat.id}_{yt.title}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)