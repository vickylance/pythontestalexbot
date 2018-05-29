# -*- coding: utf-8 -*-
import telebot,os,time,speech_recognition as sr, pydub as p,googletrans,sqlite3,random
if os.path.isdir("tmp") == False:
        os.makedirs("tmp")
if os.path.isdir("downloads") == False:
        os.makedirs("downloads")
def recognize(name,message):
    global half,sound,num_mins
    r = sr.Recognizer()
    div=30
    t=0
    def get_audio(filename):
        global half,sound,num_mins
        with sr.AudioFile(filename) as source:
            audio = r.record(source)
        return audio
    def recogn(filename):
        global half,sound,num_mins
        audio=get_audio(filename)
        a=""
        if num_mins == 0:
                a=r.recognize_google(audio,None,"ru_RU")
        else:
                a+=r.recognize_google(audio,None,"ru_RU")
        half=0
        return a
    def cut(name):
        global half,sound,num_mins
        half=0
        sound=p.AudioSegment.from_file("downloads/"+name,format=name.split(".")[-1])
        if int(len(sound)/1000) > div:
            num_mins=int(len(sound)/1000/div)
            if int(len(sound)/1000) > num_mins* div:
                num_mins+=1
            for i in range(1,num_mins+1):
                if len(sound)/1000-div*i > 0 and i == num_mins:
                    half-=div
                    s=sound[half*1000:]
                    s.export("tmp/test"+str(i)+".wav",format="wav")
                else:
                    s=sound[half*1000:half*1000+div*1000]
                    s.export("tmp/test"+str(i)+".wav",format="wav")
                half+=div 
        half=0
        return half,sound,num_mins
    half=0
    sound=0
    num_mins=0
    t=name
    half,sound,num_mins=cut(t)
    a=""
    if num_mins !=0:
            for i in range(1,num_mins+1):
                try:
                    a+=recogn("tmp/test"+str(i)+".wav")
                except (Exception, ValueError,sr.UnknownValueError) as e:
                    print("Гугл не смог распознать аудио, возможно-это музыка без текста"+str(type(e)))
                    bot.send_message(message.chat.id,"Гугл не смог распознать аудио, возможно-это музыка без текста ")
    else:
        name=name.split(".")
        name=name[0]+".wav"
        sound.export("downloads/"+name,format="wav")
        try:
                a=recogn("downloads/"+name)
        except (Exception, ValueError,sr.UnknownValueError) as e:
                print(name+": Ошибка: "+str(type(e)))
                bot.send_message(message.chat.id,"Не удалось распознать ваше сообщение")
    return a
n=0
token="some token"
bot_username="@pythontestalexbot"
bot = telebot.TeleBot(token,num_threads=4)
logger=telebot.logger
translator=googletrans.Translator()
markup=telebot.types.InlineKeyboardMarkup()
types=telebot.types
item_photo=types.InlineKeyboardButton("Команда /photo",callback_data="1")
item_video=types.InlineKeyboardButton("Команда /video",callback_data="2")
item_game=types.InlineKeyboardButton("Команда /game",callback_data="3")
'''item_message=types.InlineKeyboardButton("Ответ на каждое сообщение",callback_data="4")'''
item_photo_2=types.InlineKeyboardButton("Ответ на каждую картинку",callback_data="4")
item_audio=types.InlineKeyboardButton("Распознавание речи",callback_data="5")
markup.row(item_photo,item_video,item_game)
markup.row(item_photo_2,item_audio)
#Описание переменных блокировки
global voice_block,text_block,photo_2_block,photo_block,game_block,video_block
voice_block=0
text_block=0
photo_2_block=2
photo_block=0
game_block=0
video_block=0
#Хэндлеры
@bot.message_handler(content_types=["voice"])
def voice(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[1] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).status == "creator" or message.chat.type != "supergroup")) and data_chat[1] != 2:
            if message.from_user.username != None:
                print("@"+message.from_user.username+"("+message.from_user.first_name+"): "+"Отправил голосовое сообщение")
            else:
                print("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+"Отправил голосовое сообщение")
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            name=file_info.file_path.split("/")[-1]
            name=name.split(".")
            name=name[0]+".ogg"
            with open("downloads/"+name,"wb") as f:
                f.write(downloaded_file)
            a=recognize(name,message)
            if a != "":
                    bot.send_message(message.chat.id,a,reply_to_message_id=message.message_id)
            else:
                bot.send_message(message.chat.id,"Не было распознано никакого текста",reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,"Эта функция заблокирована администратором.",reply_to_message_id=message.message_id)
@bot.message_handler(content_types=["audio"])
def audio(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[1] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).status == "creator" or message.chat.type != "supergroup")) and data_chat[1] != 2:
        if message.from_user.username != None:
            print("@"+message.from_user.username+"("+message.from_user.first_name+"): "+"Отправил аудио")
        else:
            print("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+"Отправил аудио")
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name=file_info.file_path.split("/")[-1]
        with open("downloads/"+name,"wb") as f:
            f.write(downloaded_file)
        a=recognize(name,message)
        if a != "":
            bot.send_message(message.chat.id,a,reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id,"Не было распознано никакого текста",reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,"Эта функция заблокирована администратором.",reply_to_message_id=message.message_id)
@bot.message_handler(commands=["help","start"])
def help(message):
        register_group(message)
        bot.send_message(message.chat.id,
                         '''Привет, я Naif Studios Bot!
Я умею распознавать речь и переводить текст на любой из языков мира!
Команды:
/help - выводит эту справку
/photo - отправляет кучу фото
/game - отправляет кучу музыки
/video - отправляет кучу видео
/translate - переводит текст. Полный список языков:
https://cloud.google.com/translate/docs/languages
/upload - загружает ваши файлы на сервер (они могут получены с помощью команд /photo, /audio и /video)
/clear_user_data - очищает все данные пользователей на сервере (нужно быть администратором)
/lock - изменяет настройки доступа к командам (нужно быть администратором)
Бот создан пользователем MrNaif (@MrNaif_bel)''')
@bot.message_handler(commands=["lock"])
def lock(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,data
    for i in data:
        if i[0] == message.chat.id:
            data_chat = i
    if bot.get_chat_member(message.chat.id,message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).status == "creator" or message.chat.type != "supergroup":
        global back
        sent=bot.send_message(message.chat.id,"Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
        back=sent
    else:
        bot.send_message(message.chat.id,"Извини, это команда только для админов. Ты не админ",reply_to_message_id=message.message_id)
@bot.callback_query_handler(func=lambda sent: True)
def test(sent):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block,back,data
    for i in data:
        if i[0] == sent.message.chat.id:
            data_chat=i
    connection=sqlite3.connect("base.db")
    cursor=connection.cursor()
    data_chat=list(data_chat)
    try:
            if sent.data == "1":
                if bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "administrator" or bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "creator" or sent.message.chat.type != "supergroup":
                    if data_chat[3] == 0:
                        data_chat[3]=1
                        bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                    elif data_chat[3] == 1:
                        data_chat[3]=2
                        bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                    elif data_chat[3] == 2:
                        data_chat[3]=0
                        bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                    sql='''UPDATE chats SET voice_block = {0}, photo_2_block = {1}, photo_block = {2}, game_block = {3}, video_block = {4} WHERE chat_id = {5}'''.format(data_chat[1],data_chat[2],data_chat[3],data_chat[4],data_chat[5],back.chat.id)
                    cursor.execute(sql)
                    connection.commit()
                    data=cursor.execute("SELECT * FROM chats").fetchall()
            if sent.data == "2":
                if bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "administrator" or bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "creator" or sent.message.chat.type != "supergroup":
                        if data_chat[5] == 0:
                                data_chat[5]=1
                                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        elif data_chat[5] == 1:
                                data_chat[5]=2
                                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        elif data_chat[5] == 2:
                                data_chat[5]=0
                                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        sql='''UPDATE chats SET voice_block = {0}, photo_2_block = {1}, photo_block = {2}, game_block = {3}, video_block = {4} WHERE chat_id = {5}'''.format(data_chat[1],data_chat[2],data_chat[3],data_chat[4],data_chat[5],back.chat.id)
                        cursor.execute(sql)
                        connection.commit()
                        data=cursor.execute("SELECT * FROM chats").fetchall()
            if sent.data == "3":
                if bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "administrator" or bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "creator" or sent.message.chat.type != "supergroup":
                        if data_chat[4] == 0:
                                data_chat[4]=1
                                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        elif data_chat[4] == 1:
                                data_chat[4]=2
                                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        elif data_chat[4] == 2:
                                data_chat[4]=0
                                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        sql='''UPDATE chats SET voice_block = {0}, photo_2_block = {1}, photo_block = {2}, game_block = {3}, video_block = {4} WHERE chat_id = {5}'''.format(data_chat[1],data_chat[2],data_chat[3],data_chat[4],data_chat[5],back.chat.id)
                        cursor.execute(sql)
                        connection.commit()
                        data=cursor.execute("SELECT * FROM chats").fetchall()
            if sent.data == "4":
                if bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "administrator" or bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "creator" or sent.message.chat.type != "supergroup":
                        if data_chat[2] == 0:
                            data_chat[2]=1
                            bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        elif data_chat[2] == 1:
                            data_chat[2]=2
                            bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        elif data_chat[2] == 2:
                            data_chat[2]=0
                            bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        sql='''UPDATE chats SET voice_block = {0}, photo_2_block = {1}, photo_block = {2}, game_block = {3}, video_block = {4} WHERE chat_id = {5}'''.format(data_chat[1],data_chat[2],data_chat[3],data_chat[4],data_chat[5],back.chat.id)
                        cursor.execute(sql)
                        connection.commit()
                        data=cursor.execute("SELECT * FROM chats").fetchall()
            if sent.data == "5":
                if bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "administrator" or bot.get_chat_member(sent.message.chat.id,sent.from_user.id).status == "creator" or sent.message.chat.type != "supergroup":
                        if data_chat[1] == 0:
                                data_chat[1]=1
                                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        elif data_chat[1] == 1:
                                data_chat[1]=2
                                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        elif data_chat[1] == 2:
                                data_chat[1]=0
                                bot.edit_message_text(chat_id=sent.message.chat.id,message_id=sent.message.message_id,text="Настройки доступа к командам(0-включено для всех, 1-только для админов,2-выключено)\n"+"Команда /photo - "+str(data_chat[3])+"\n"+"Команда /video - "+str(data_chat[5])+"\n"+"Команда /game - "+str(data_chat[4])+"\n"+"Ответ на каждую картинку - "+str(data_chat[2])+"\n"+"Распознавание речи - "+str(data_chat[1]),reply_markup=markup)
                        sql='''UPDATE chats SET voice_block = {0}, photo_2_block = {1}, photo_block = {2}, game_block = {3}, video_block = {4} WHERE chat_id = {5}'''.format(data_chat[1],data_chat[2],data_chat[3],data_chat[4],data_chat[5],back.chat.id)
                        cursor.execute(sql)
                        connection.commit()
                        data=cursor.execute("SELECT * FROM chats").fetchall()
    except NameError as e:
        print(e)
        print("Бот был перезапущен. Запустите команду /lock еще раз")
        bot.send_message(sent.message.chat.id,"Бот был перезапущен. Запустите команду /lock еще раз",reply_to_message_id=sent.message.message_id)
    connection.close()
@bot.message_handler(commands=["photo","video","game","translate","upload","clear_user_data"])
def ask(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block
    text=message.text
    text=text.split("/")[-1]
    if text.split("/")[-1] == "photo" or text.split("/")[-1] == "photo"+bot_username:
        sent=bot.send_message(message.chat.id,"Сколько фото отправить?")
        bot.register_next_step_handler(sent,photo)
    if message.text.split("/")[-1] == "video" or message.text.split("/")[-1] == "video"+bot_username:
        sent=bot.send_message(message.chat.id,"Сколько видео отправить?")
        bot.register_next_step_handler(sent,video)
    if message.text.split("/")[-1] == "game" or message.text.split("/")[-1] == "game"+bot_username:
        sent=bot.send_message(message.chat.id,"Сколько аудио отправить?")
        bot.register_next_step_handler(sent,game)
    if message.text.split("/")[-1] == "translate" or message.text.split("/")[-1] == "translate"+bot_username:
        sent=bot.send_message(message.chat.id,"Введите сообщение для перевода:")
        bot.register_next_step_handler(sent,translate_ask)
    if message.text.split("/")[-1] == "upload" or message.text.split("/")[-1] == "upload"+bot_username:
        sent=bot.send_message(message.chat.id,"Пришлите файл для загрузки на сервер:")
        bot.register_next_step_handler(sent,upload)
    if message.text.split("/")[-1] == "clear_user_data" or message.text.split("/")[-1] == "clear_user_data"+bot_username:
        if bot.get_chat_member(message.chat.id,message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).status == "creator"  or message.chat.type != "supergroup":
            sent=bot.send_message(message.chat.id,"Вы уверены, что хотите очистить данные пользователей?(Варианты ответов: да и нет)")
            bot.register_next_step_handler(sent,clear_user_data)
        else:
            bot.send_message(message.chat.id,"Извини, это команда только для админов. Ты не админ",reply_to_message_id=message.message_id)
def game(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[4] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).status == "creator")) and data_chat[4] != 2:
        text=message.text
        try:
            text=int(text)
            max_=message.text
            max_=int(max_)
            for i in os.listdir("user_audio/"):
                if max_ > 0:
                    with open("user_audio/"+i,"rb") as v:
                        bot.send_voice(message.chat.id,v,None)
                        print("Удачно отправлено:",i)
                        time.sleep(3)
                    max_-=1
            for i in os.listdir("ogg/"):
                if max_ > 0:
                    with open("ogg/"+i,"rb") as v:
                        bot.send_voice(message.chat.id,v,None)
                        print("Удачно отправлено:",i)
                        time.sleep(3)
                    max_-=1
            bot.send_message(message.chat.id, "Все отправлено: аудио")
            print("Все отправлено: аудио")
        except ValueError:
            print("Введите цифры")
            bot.send_message(message.chat.id,"Введите цифры",reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,"Эта функция заблокирована администратором.",reply_to_message_id=message.message_id)
def photo(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[3] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).status == "creator")) and data_chat[3] != 2:
        text=message.text
        try:
            text=int(text)
            max_=message.text
            max_=int(max_)
            for i in os.listdir("user_photo/"):
                if max_ > 0:
                    with open("user_photo/"+i,"rb") as p:
                        bot.send_photo(message.chat.id,p,None)
                        print("Удачно отправлено:",i)
                        time.sleep(3)
                    max_-=1
            for i in os.listdir("фото_робопарк/"):
                if i.split(".")[-1] == "jpg" and max_ > 0:
                    with open("фото_робопарк/"+i,"rb") as p:
                        bot.send_photo(message.chat.id,p,None)
                        print("Удачно отправлено:",i)
                        time.sleep(3)
                    max_-=1
            for i in os.listdir("2018-05/"):
                if i.split(".")[-1] == "png" and max_ > 0:
                    with open("2018-05/"+i,"rb") as p:
                        bot.send_photo(message.chat.id,p,None)
                        print("Удачно отправлено:",i)
                        time.sleep(3)
                    max_-=1
            for i in os.listdir("2018-04/"):
                if i.split(".")[-1] == "png" and max_ > 0:
                    with open("2018-04/"+i,"rb") as p:
                        bot.send_photo(message.chat.id,p,None)
                        print("Удачно отправлено:",i)
                        time.sleep(3)
                    max_-=1
            bot.send_message(message.chat.id, "Все отправлено: фото")
            print("Все отправлено: фото")
        except ValueError:
            print("Введите цифры")
            bot.send_message(message.chat.id,"Введите цифры",reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,"Эта функция заблокирована администратором.",reply_to_message_id=message.message_id)
def video(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[5] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).status == "creator")) and data_chat[5] != 2:
        text=message.text
        try:
            text=int(text)
            max_=message.text
            max_=int(max_)
            for i in os.listdir("user_video/"):
                if max_ > 0:
                    with open("user_video/"+i,"rb") as vid:
                        vid.seek(0, os.SEEK_END)
                        size=vid.tell()
                        if size < 50000000:
                            vid.seek(0)
                            bot.send_video(message.chat.id,vid,None,timeout=2000)
                            print("Удачно отправлено:",i)
                            time.sleep(5)
                        else:
                            print(i+": "+"Файл весит больше 50 мегабайт, он не был отправлен")
                            bot.send_message(message.chat.id,i+": "+"Файл весит больше 50 мегабайт, он не был отправлен")
                    max_-=1

            for i in os.listdir("фото_робопарк/"):
                if i.split(".")[-1] == "mp4" and max_ > 0:
                    with open("фото_робопарк/"+i,"rb") as vid:
                        vid.seek(0, os.SEEK_END)
                        size=vid.tell()
                        if size < 50000000:
                            vid.seek(0)
                            bot.send_video(message.chat.id,vid,None,timeout=2000)
                            print("Удачно отправлено:",i)
                            time.sleep(5)
                        else:
                            print(i+": "+"Файл весит больше 50 мегабайт, он не был отправлен")
                            bot.send_message(message.chat.id,i+": "+"Файл весит больше 50 мегабайт, он не был отправлен")
                    max_-=1
            for i in os.listdir("2018-05/"):
                if i.split(".")[-1] == "mp4" and max_ > 0:
                    with open("2018-05/"+i,"rb") as vid:
                        bot.send_video(message.chat.id,vid,None)
                        print("Удачно отправлено:",i)
                        time.sleep(3)
                    max_-=1
            for i in os.listdir("2018-04/"):
                if i.split(".")[-1] == "mp4" and max_ > 0:
                    with open("2018-04/"+i,"rb") as vid:
                        bot.send_video(message.chat.id,vid,None)
                        print("Удачно отправлено:",i)
                        time.sleep(3)
                    max_-=1
            bot.send_message(message.chat.id, "Все отправлено: видео")
            print("Все отправлено: видео")
        except ValueError:
            print("Введите цифры")
            bot.send_message(message.chat.id,"Введите цифры",reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,"Эта функция заблокирована администратором.",reply_to_message_id=message.message_id)
def translate_ask(message):
    global text
    text=message.text
    sent=bot.send_message(message.chat.id,"На какой язык перевести?(Например, Русcкий - ru, английский - en) Список всех языков: https://cloud.google.com/translate/docs/languages")
    bot.register_next_step_handler(sent,translate)
def translate(message):
    global text
    try:
        a=translator.translate(text,dest=message.text).text
        bot.send_message(message.chat.id,a,reply_to_message_id=message.message_id)
        if message.from_user.username != None:
            print("@"+message.from_user.username+"("+message.from_user.first_name+"): "+a)
        else:
            print("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+a)
    except ValueError:
        bot.send_message(message.chat.id,"Нет такого языка, попробуйте еще раз!",reply_to_message_id=message.message_id)
@bot.message_handler(content_types=["new_chat_members"], func=lambda message:message.chat.type != "supergroup")
def register_group(message):
    global data
    r=0
    for i in data:
        if i[0] == message.chat.id:
            r=1
    if r == 0:
        connection=sqlite3.connect("base.db")
        cursor=connection.cursor()
        sql='''INSERT INTO chats(chat_id,voice_block,photo_2_block,photo_block,game_block,video_block,name)
              VALUES(?,?,?,?,?,?,?)'''
        cursor.execute(sql,(message.chat.id,0,2,0,0,0,message.chat.title))
        connection.commit()
        data=cursor.execute("SELECT * FROM chats").fetchall()
        connection.close()
def upload(message):
    if message.content_type == "photo":
        file_info = bot.get_file(message.photo[2].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name=file_info.file_path.split("/")[-1]
        with open("user_photo/"+name,"wb") as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id,"Успешно отправлено!",reply_to_message_id=message.message_id)
    elif message.content_type == "audio":
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name=file_info.file_path.split("/")[-1]
        with open("user_audio/"+name,"wb") as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id,"Успешно отправлено!",reply_to_message_id=message.message_id)
    elif message.content_type == "voice":
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name=file_info.file_path.split("/")[-1]
        name=name.split(".")
        name=name[0]+".ogg"
        with open("user_audio/"+name,"wb") as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id,"Успешно отправлено!",reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,"Формат файла не был распознан!",reply_to_message_id=message.message_id)
def clear_user_data(message):
    if bot.get_chat_member(message.chat.id,message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).status == "creator" or message.chat.type != "supergroup":
        if message.text == "да":
            for i in os.listdir("user_photo"):
                os.remove("user_photo/"+i)
            for ii in os.listdir("user_video"):
                os.remove("user_video/"+ii)
            for iii in os.listdir("user_audio"):
                os.remove("user_audio/"+iii)
            bot.send_message(message.chat.id,"Успешно очищено!",reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id,"Нет так нет, ничего не было очищено.",reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id,"Извини, это команда только для админов. Ты не админ",reply_to_message_id=message.message_id)
@bot.message_handler(content_types=["photo"])
def repeat_all_photos(message):
    global data
    global voice_block,text_block,photo_2_block,photo_block,game_block,video_block
    for i in data:
        if i[0] == message.chat.id:
            data_chat=i
    if ((data_chat[2] != 1) or (bot.get_chat_member(message.chat.id,message.from_user.id).status == "administrator" or bot.get_chat_member(message.chat.id,message.from_user.id).status == "creator")) and data_chat[2] != 2:
        with open("image.jpg","rb") as ph:
            a=bot.send_photo(message.chat.id,ph,None)
            if message.from_user.username != None:
                print("@"+message.from_user.username+"("+message.from_user.first_name+"): "+"Отправил фото")
            else:
                print("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+"Отправил фото")
    else:
        if message.from_user.username != None:
                print("@"+message.from_user.username+"("+message.from_user.first_name+"): "+"Отправил фото")
        else:
                print("@"+message.from_user.first_name+"("+message.from_user.first_name+"): "+"Отправил фото")
def get_data():
        connection=sqlite3.connect("base.db")
        cursor=connection.cursor()
        data=cursor.execute("SELECT * FROM chats").fetchall()
        connection.close()
        return data
global data
data=get_data()
if __name__ == "__main__":
    try:
        bot.infinity_polling(none_stop=True)
    except (Exception,ConnectionResetError,ConnectionError) as e:
        print("Ошибка!!!!\n",str(e))
        logger.error(e)
        time.sleep(15)
