import telebot
import random as rd
from random import randint as rand
from time import sleep 

token = None 
bot = None

while True:
    try:
        with open("token.txt","r") as f:
            f = f.read()
            if len(f) >= 15:
                token = f
        if  token != None:
            try:
                bot = telebot.TeleBot(token)
                break
            except:
                print(f"Введён не правильно токен.")
                token = None
                sleep(5)
        else:
            print("Введите токен бота")
            sleep(5)
        pass
    except:
        with open("token.txt","w"):
            pass

r=0

#Array
Mlist = []
Afr=[]
Friends=[]      #Save a list of friends
HFriends = []   #A list of friend for the randomization function
#1927410642 - id Максима

#Variable
num = -1
com = None
Gmes = None
MId = None
print("Бот начал работу")


@bot.callback_query_handler(func=lambda call: "Fr" in call.data) #
def friends(call):
    global com
    global HFriends
    global MId
    cdata=call.data
    # bot.edit_message_text(f"Введите список вариантов через enter.Пример:\nПридмет1\nПридмет2\n и т.д сколько вам надо.",call.message.chat.id, call.message.message_id)
    # com = "list2"
    if "All" in cdata:
        bot.edit_message_text(f"Введите список вариантов через enter.Пример:\nПридмет1\nПридмет2\n и т.д сколько вам надо.",call.message.chat.id, call.message.message_id)
        com = "list2"
        for i in Friends:
            HFriends.append(i[0])

        MId=call.message.message_id
    
    elif "End" in cdata:
        bot.edit_message_text(f"Введите список вариантов через enter.Пример:\nПридмет1\nПридмет2\n и т.д сколько вам надо.",call.message.chat.id, call.message.message_id)
        com = "list2"
        MId=call.message.message_id
    
    else:
        ID = int(cdata.replace("Fr",""))
        HFriends.append(ID)
        
        if len(Friends) == len(HFriends):
            bot.edit_message_text(f"Введите список вариантов через enter (Shift+enter). Пример:\nПридмет1\nПридмет2\n и т.д сколько вам надо.",call.message.chat.id, call.message.message_id)
            com = "list2"
            MId=call.message.message_id

        else:
            Bfriend(call)
            
@bot.callback_query_handler(func=lambda call: "Fdell" in call.data)
def DellF(call):
    global Friends
    Call = call.data.replace("Fdell","")   
    if Call == "All":
        Friends=[]
        bot.edit_message_text(f"Вы удалили пользователей из своего списка", call.message.chat.id, call.message.message_id)

    else:
        b=None
        for i in Friends:
            if i[0] == int(Call):
                b = i
                Friends.remove(i)

        bot.edit_message_text(f"Вы удалили пользователся: {b[1]} c id: {b[0]}",call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'one') #Выполнение кнопки на один чат
def One(call): #step1.1
    global com
    global Mid
    bot.edit_message_text(f"Введите список вариантов через enter.Пример:\nПридмет1\nПридмет2\n и т.д сколько вам надо.",call.message.chat.id, call.message.message_id)
    com = "list1"
    Mid=call.message.message_id
    

@bot.callback_query_handler(func=lambda call: call.data == 'friends') #Выполнение кнопки на выбор нескольких чатов 
def Bfriend(call): #step1.2
    if len(Friends)>0:
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i in Friends:
            print(i)
            if not i[0] in HFriends:
                button = telebot.types.InlineKeyboardButton(text=f"{i[-1]}", callback_data=f'Fr{i[0]}')
                keyboard.add(button)

        button = telebot.types.InlineKeyboardButton(text=f"Все", callback_data=f'FrAll')
        keyboard.add(button)
        if len(HFriends):
            button = telebot.types.InlineKeyboardButton(text=f"Завершить", callback_data=f'FrEnd')
            keyboard.add(button)
        
        bot.edit_message_text("Выберите дрезей", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        pass
    else:
        bot.edit_message_text(f"У вас нету к сожелению друзей:(\nМожете их добавить через /friends и узнать свой id через команду /id",call.message.chat.id, call.message.message_id)
    


@bot.callback_query_handler(func=lambda call: "Repeat" in call.data)
def RePeat(call):
    global MId
    Cal=call.data
    Call = int(Cal.replace("Repeat",""))
    MId = call.message.message_id
    bot.delete_message(call.message.chat.id, MId)
    randomize.AnonRand(Call, MId)




#{-----------------
@bot.callback_query_handler(func=lambda call: True) #Выполняет исход выбранной кнопки на кол-во исходов рандома
def Creat_button(call): #step3 \/4  <-- step2  
    global num
  
    num=int(call.data)
    bot.edit_message_text(f"Вы сделали выбор: {num+1}",call.message.chat.id, call.message.message_id)
    randomize.Logic(call.message,0,num,call.message.message_id)#Step4.1 \/

def Button(Id, numb): #step2 /\3  <-- step1       #Создаёт кнопку выбора кол-ва исходов
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(numb):
        button = telebot.types.InlineKeyboardButton(text=f"{i+1}",
                                                        callback_data=f'{i}')
        keyboard.add(button)

    bot.send_message(Id, "Кол-во исходов", reply_markup=keyboard)

#-----------------}



class randomize:   #Класс на всю логику рандома в боте   
    def base():  #База данных класса
        Id = None
        Mlist = None

    def Logic(message, fr , num=0, Mid=None): #step2.1 <-- step0 & step3  #Основная логика обработки информации и распределения процессов
        global HFriends
        #print(f"Input:\n1) {message}\n{'--'*5}\n2){num}")
        db=randomize.base
        #randomize.Logic(call.message,1,num,call.message.message_id)
        
        db.Id = message.chat.id
        mes = message.text
        if fr==0:  
            if Mid!=None: #Step 5.1
                #randomize.Logic(call.message,0,num,call.message.message_id)<--
                    
                bot.edit_message_text(f"Вам выпало:{randomize.Rand(num)}",db.Id, Mid)

            else: #step2.1
                db.Mlist = mes.split("\n")
                keyboard = telebot.types.InlineKeyboardMarkup()
                for i in range(len(db.Mlist)):        
                    button = telebot.types.InlineKeyboardButton(text=f"{i+1}", callback_data=f'{i}',)
                    keyboard.add(button)
                bot.send_message(db.Id, f"Сколько ответов вы желаете:",reply_markup=keyboard)

        elif fr>0:
            HFriends.append(db.Id)
            db.Mlist = mes.split("\n")
            if len(db.Mlist) < len(HFriends):
                keyboard = telebot.types.InlineKeyboardMarkup()
                button = telebot.types.InlineKeyboardButton(text="Повторять",callback_data=f"Repeat1")
                keyboard.add(button)
                button = telebot.types.InlineKeyboardButton(text="Не повторять",callback_data=f"Repeat0")
                keyboard.add(button)
                bot.send_message(db.Id, "Могу ли я повторять варианты из списка? Если нет, то не все пользователи получат вариант.", reply_markup=keyboard)
            

            else:
                randomize.AnonRand(-1, message.from_user.username)
                    

                pass
            
            pass

        else: #step4 <-- step3

            #Function calls  !!!!ПЕРЕДЕЛАТЬ!!!!
            Out = randomize.Rand(num)
            bot.send_message(db.Id, f"вам выпало: {Out}")

            pass
        
    def Rand(var=0): #Рандом в 1 чате
        db=randomize.base
        Output = ""
        #print(f"Var: {var}; type: {type(var)}")
        if var==0: #Random with one variable
            Output = f"\n{db.Mlist[rand(0,var)]}"
                              
        elif var>0: #random with more variable
            Inp = db.Mlist
            for i in range(3):
                rd.shuffle(Inp)

            for i in range(var+1):
                r = rand(0,var)
                Output+=f'\n{db.Mlist[r]}'
                Inp.pop(r)
    
        return Output     
    
    def AnonRand(R,user):  #R - repeat, user - @username
        db = randomize.base
        List = db.Mlist
        Users = HFriends

        for _ in range(3):
            rd.shuffle(List)
            rd.shuffle(Users)

        if R==1:            
            for i in HFriends:
                if i == db.Id:
                    bot.send_message(i,f"Вам выпало: {List[rand(0,len(List)-1)]}")

                else:
                    bot.send_message(i,f"От пользователя @{user}\nВам выпало: {List[rand(0,len(List)-1)]}")
        
        elif R==-1:
            for i in HFriends:
                text = List[rand(0,len(List)-1)]
                List.remove(text)

                if i == db.Id:
                    bot.send_message(i,f"Вам выпало: {text}")

                else:
                    bot.send_message(i,f"От пользователя @{user}\nВам выпало: {text}")


        else:
            Send=[]
            for i in HFriends:
                if len(List):
                    RD = List[rand(0,len(List)-1)]
                    if i == db.Id:
                        bot.send_message(i,f"Вам выпало: {RD}")
                        

                    else:
                        bot.send_message(i,f"От пользователя @{user}\nВам выпало: {RD}")
                        
                    Send.append(i)
                    List.remove(RD)
                else:
                    break
            Ulist = ""
            for i in Friends:
                for I in Users:
                    if i[0] == I:
                        Ulist+=f" {i[1]}"

            bot.send_message(db.Id, f"Все пользователи которые получили итоги:{Ulist}")


def commands(message):
    global com
    global Gmes
    global HFriends
    mes = message.text.lower()
    Id = message.chat.id

    if mes == "/start":
        bot.send_message(Id,"/help - вызов этого окна\n/id - Узнать свой id\n/friends - добавить друга в список\n/randomize - рандомайзер\n/delfriend - Удалить пользователся из списка")

    if mes == "/delfriend":
        if len(Friends):
            keyboard = telebot.types.InlineKeyboardMarkup()
            for i in Friends:               
                button = telebot.types.InlineKeyboardButton(text=f"{i[-1]}", callback_data=f'Fdell{i[0]}')
                keyboard.add(button)

            button = telebot.types.InlineKeyboardButton(text=f"Всех", callback_data=f'FdellAll')
            keyboard.add(button)
            bot.send_message(Id, f"Кого вы хотите удалить?",reply_markup=keyboard)
        else:
            bot.send_message(Id,f"У вас нету к сожелению друзей:(\nМожете их добавить через /friends и узнать свой id через команду /id")

    if mes == "/help":
        bot.send_message(Id,"/help - вызов этого окна\n/id - Узнать свой id\n/friends - добавить друга в список\n/randomize - рандомайзер\n/delfriend - Удалить пользователся из списка")

    if mes == "/id":
        bot.send_message(Id, f"Ваш id:  {message.from_user.id}\nПоделитесь им с другом что бы он добавил вас в \"друзья\"")
    
    if mes == "/friends":
        bot.send_message(Id, f"Что бы добавить друга введите его id")
        return "add"

    if "/randomize" == mes:      #Step_1  
        HFriends=[]
        keyboard = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text=f"Только этот чат", callback_data=f'one',)
        keyboard.add(button)
        button = telebot.types.InlineKeyboardButton(text=f"С другими чатами(друзей)", callback_data=f'friends',)
        keyboard.add(button)
        bot.send_message(Id, "Выдать исход только вам или ещё с друзьями уникальным(-и) исходами?", reply_markup=keyboard)

        Gmes = message

        #randomize.Logic(message) #step0 /\1
        

@bot.message_handler(func=lambda message: True)
def main(message):
    global com
    global Afr
    
    if "/" in message.text:
        com = None
        com = commands(message)    


    elif com=="add":
        Afr=[]
        try:
            Fid=int(message.text)
            Afr.append(Fid)
            print(Afr)
            com="AddName"
            bot.send_message(message.chat.id, "Дайте имя этому пользователю")

        except Exception as er:
            bot.send_message(message.chat.id, "Вы ввели не айди или совершили в нём ошибку.")
            com = None
        

    elif com=="AddName":
        try:
            Afr.append(message.text)          
            print(f"Afr: {Afr}\nFriend: {Friends}")
            bot.send_message(Afr[0],f"Вас добавил в друзья пользователь: @{message.from_user.username}")
            bot.send_message(message.chat.id, "Данный пользователь добавлен")
            Friends.append(Afr)
        except Exception as e:
            bot.send_message(message.chat.id, "Пользователь с этим id не найден")
            Afr = []

    elif "list" in str(com):  #Step_2
        text = message.text
        if "1" in str(com) and '\n' in text: #step2.1/\
            randomize.Logic(message,0) #
            
            pass

        elif "2" in com and '\n' in text:
            print("------1111-----------")
            randomize.Logic(message,1)

        com=None

    else:
        print(f"No work: {com}")
        com=None
        #print(f"{com}")

bot.infinity_polling()
