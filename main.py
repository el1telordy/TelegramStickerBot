import telebot
import json
import PIL
from PIL import Image
from telebot import apihelper

bot = telebot.TeleBot('Token')
 
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'test')
    
def get_stickerid(message):
 
    # JSON DICTIONARY
 
    all_stick_data = {"file_id": message.sticker.file_id, "width": message.sticker.width,
              "height": message.sticker.height,
              "emoji": message.sticker.emoji, "set_name": message.sticker.set_name,
              "mask_position": message.sticker.mask_position, "file_size": message.sticker.file_size,
              "is_animated": message.sticker.is_animated}
 
    with open('sticker_data.json', 'w') as outfile:
         json.dump(all_stick_data, outfile)
 
    #загрузка и сохранение стикера в png в корень папки
 
    sticker_file_info = bot.get_file(all_stick_data.get("file_id"))
    new_sticker_file = bot.download_file(sticker_file_info.file_path)
    with open("sticker.webp", 'wb') as new_file:
        new_file.write(new_sticker_file)
    imgbp = Image.open("sticker.webp")
    imgbp.save("sticker.png", "png")
 
    # удаление вебп с хоста
    import os
    os.remove("sticker.webp")
 
@bot.message_handler(content_types=['photo'])
def get_photodata(message):
    #выводим = мессадж - словарь{}, в котором словарь{} жсон, в котором лист[] фото, в котором 3 словаря{} и берем индекс -1 (самый последний)
    picID = message.json['photo'][-1]['file_id'];
 
    # загрузка и сохранение фото в png в корень папки
    file_info = bot.get_file(picID)
    new = bot.download_file(file_info.file_path)
    with open("image.png", 'wb') as new_file:
        new_file.write(new)
 
    # ресайз пикчи до 512/512 с учетом соотношения сторон
    imgrsz = Image.open("image.png")
    imgrsz.thumbnail((512, 512))
    imgrsz.save("image.png")
 
@bot.message_handler(commands=['addsticker'])
def start(message):
  sent = bot.send_message(message.chat.id, "Send emoji to assign it to sticker")
  bot.register_next_step_handler(sent, get_emoji)
 
def get_emoji(message):
    emoji = message.text
    sent = bot.send_message(message.chat.id, 'Now send your stiker')
    bot.register_next_step_handler(sent, getstik, emoji)
 
def getstik(message, emoji):
    if (message.content_type == 'photo'):
        get_photodata(message)
        fID = bot.upload_sticker_file(<userid>, open("image.png", "rb")).file_id
    if (message.content_type == 'sticker'):
        get_stickerid(message)
        fID = bot.upload_sticker_file(<userid>, open("sticker.png", "rb")).file_id
    bot.add_sticker_to_set(<userid>, '<stickerpackname>_by_<botname>bot', fID, emoji)
    bot.send_message(message.chat.id, "Sticker has been added successfully")
 
if __name__ == '__main__':
    bot.infinity_polling()
