# TresPalmerasBot is a Telegram bot to communicate with Thingspeak using
# requests and posts. It provides an interface to command the actuators located
# in a remote farm, as well as a way to retrieve useful information from the
# sensors.
#
# On the farm there is an Arduino that uploads and reads data on Thingspeak with
# a particular URL for each.
#
# Implemented using pyTelegramBotAPI by eternnoir:
# https://github.com/eternnoir/pyTelegramBotAPI
#
# Features:
#  - Whitelist of allowed users to connect to the bot.
#  - Interactive form-type URL building.
#  - Retrieve and send data.
#
# Javier Macías - 2016

import telebot
from telebot import types
import requests

token = 'your_token'
tb = telebot.TeleBot(token)
users = [userid1, userid2] #Permitted access

options_on_off = ['ALL', 'ABONO', 'BOMBA', 'Naranjos', 'M. Bj Del.', 'M. Bj Detras', 'M. Alt Del', 'M. Alt Det', 'Césped', 'Parras 1', 'Parras 2', 'Parras 3', 'Parras 4', 'Parras 5', 'Parras 6', 'Parras Est', 'Bodega lado', 'Bodega Alej', 'Sector 16', 'Sector 17', 'Sector 18', 'Sector 19', 'Sector 20', 'Sector 21', 'Sector 22', 'Sector 23', 'Sector 24']
options_system = ['AUTO', 'MANUAL']
sectors = 24

#command class stores the commands to be sent in the form TURN_atrib1_atrib2_
class command:
    def __init__(self):
        self.atrib1 = None
        self.atrib2 = None

###----Start of function declaration----###

# Build the dynamic keyboard depending on the options to be shown
def make_keyboard(names, row_width, one_time_keyboard, msg, chat_id):
	markup = types.ReplyKeyboardMarkup(row_width = row_width, one_time_keyboard = one_time_keyboard)
	if row_width == 1: #One column
		for i in range(0, len(names), 1): #Each button generation
			markup.add(types.KeyboardButton(names[i]))
	elif row_width == 2: #Two columns
		for i in range(0, len(names), 2): #Each button generation
			markup.add(types.KeyboardButton(names[i]), types.KeyboardButton(names[i+1]))
	else:
		for i in range(0, len(names), 3): #Each button generation
			markup.add(types.KeyboardButton(names[i]), types.KeyboardButton(names[i+1]), types.KeyboardButton(names[i+2]))
	tb.send_message(chat_id, msg, reply_markup = markup)

# Request JSON and extract the data
def read_thingspeak_data(url):
    r = requests.get(url = url)
    result = r.json()
    readings = []
    i = 0
    while True:
        try:
            field_name = "field{}".format(i+1)
            readings.append(float(result['feeds'][0][field_name]))
            i += 1
        except KeyError:
            break
        except TypeError:
            break

    return readings

# Send post URL to send the commands to actuators through Thingspeak
def send_url(atribs):
    try:
        atrib1 = command.atrib1
        url = "https://api.thingspeak.com/talkbacks/11113/commands.json?apikey=B9CYY6EMILIU2WFF&command_string=TURN_"
        if atribs == 1:
            url += atrib1 + "_"
        else:
            atrib2 = command.atrib2
            url += atrib1 + "_" + str(atrib2) + "_"
        requests.post(url)
    except TypeError:
        print("TypeError raised!")
        pass
    except ValueError:
        print("ValueError raised!")
        pass
    return

# Stop the unwelcomed!
def not_welcome(chat_id):
    tb.send_message(chat_id, "Forbidden access!")

###----End of function declaration----###

# Welcome message
@tb.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.from_user.id
    if chat_id in users:
        command.atrib1 = None
        command.atrib2 = None
        tb.send_message(chat_id, "Welcome to TresPalmerasBot! I am here to help you manage your farm. These are the current available commands:\n-/start - Welcome message\n-/help - Obtain help from the bot\n-/keyboard - Display main keyboard\n-/report - Obtain the current state of the farm\n \nDon't forget to run /keyboard once you've sent a command.")
    else:
        not_welcome(chat_id)

# Help message prints the available commands.
@tb.message_handler(commands=['help'])
def send_help(message):
    chat_id = message.from_user.id
    if chat_id in users:
        command.atrib1 = None
        command.atrib2 = None
        tb.send_message(chat_id, "I am here to help you, what are you willing to do? Available commands:\n-/start - Welcome message\n-/help - Obtain help from the bot\n-/keyboard - Display main keyboard\n-/report - Obtain the current state of the farm\n \nDon't forget to run /keyboard once you've sent a command.")
    else:
        not_welcome(chat_id)

# Report message prints the current state of all sensors in the farm
@tb.message_handler(commands=['report'])
def send_report(message):
    chat_id = message.from_user.id
    if chat_id in users:
        try:
            command.atrib1 = None
            command.atrib2 = None
            url = 'https://api.thingspeak.com/channels/98203/feeds.json?api_key=AUMY5ZJB0YMIUFJW&results=1'
            readings_1 = read_thingspeak_data(url)
            url = 'https://api.thingspeak.com/channels/160122/feeds.json?api_key=WR3UQ2QP7HAGUX1R&results=1'
            readings_2 = read_thingspeak_data(url)
            url = 'https://api.thingspeak.com/channels/160124/feeds.json?api_key=HTCAB7K2JKKROPDR&results=1'
            readings_3 = read_thingspeak_data(url)
            url = 'https://api.thingspeak.com/channels/208230/feeds.json?api_key=HMIW6EJ078RV5K4R&results=1'
            readings_4 = read_thingspeak_data(url)

            readings = readings_1 + readings_2 + readings_3 + readings_4
            print("len(readings) = ")
            print(len(readings))
            tb.send_message(chat_id, "Temperature: %.1f\nRelative humidity: %.1f\nWater flow: %.1f\nPump pressure: %.1f\nPond level: %.1f\nPump power: %.1f\n \nCanales:\nNaranjos: %.1f\nMangos bajos delante: %.1f\nMangos bajos detrás: %.1f\nMangos altos delante: %.1f\nMangos altos detrás: %.1f\nCésped: %.1f\nParras 1: %.1f\nParras 2: %.1f\nParras 3: %.1f\nParras 4: %.1f\nParras 5: %.1f\nParras 6: %.1f\nParras estanque: %.1f\nBodega lado: %.1f\nBodega alejado: %.1f\nAbono: %.1f\nField Label 1:   %.1f\nField Label 2: %.1f\nBomba: %.1f\nAbono: %.1f\nField Label 5: %.1f\nField Label 6: %.1f\nField Label 7: %.1f\nField Label 8: %.1f" % (readings[0], readings[1], readings[2], readings[3], readings[4], readings[5], readings[6], readings[7], readings[8], readings[9], readings[10], readings[11], readings[12], readings[13], readings[14], readings[15], readings[16], readings[17], readings[18], readings[19], readings[20], readings[21], readings[22], readings[23], readings[24],     readings[25], readings[26], readings[27], readings[28], readings[29]))
            tb.send_message(chat_id, "/keyboard, /report?")
        except IndexError:
            print("IndexError in send_report function")
            tb.send_message(chat_id, "There was an IndexError. Try again, if the error persist, report the issue to your system administrator")
            tb.send_message(chat_id, "/keyboard, /report?")
    else:
        not_welcome(chat_id)

# Create the keyboard for dynamic input
@tb.message_handler(commands=['keyboard'])
def program(message):
    chat_id = message.from_user.id
    if chat_id in users:
        command.atrib1 = None
        command.atrib2 = None
        names = ['Control', 'Read data']
        row_width = 1
        one_time_keyboard = True
        msg = "Select an option to get started:"
        make_keyboard(names, row_width, one_time_keyboard, msg, chat_id)
        types.ReplyKeyboardRemove()
    else:
        not_welcome(chat_id)

# Read data from a particular JSON, depending on the regexp pressed
@tb.message_handler(regexp="Read data")
def read_data(message):
    chat_id = message.from_user.id
    if chat_id in users:
        command.atrib1 = None
        command.atrib2 = None
        sending = False
        names = ['Temperature', 'Relative humidity', 'Water flow', 'Pump pressure', 'Pond level', 'Pump power']
        row_width = 2
        one_time_keyboard = True
        msg = "What data do you want to read?"
        make_keyboard(names, row_width, one_time_keyboard, msg, chat_id)
        types.ReplyKeyboardRemove()
    else:
        not_welcome(chat_id)

    @tb.message_handler(regexp="Temperature")
    def temperature(message):
        chat_id = message.from_user.id
        if chat_id in users:
            url = 'https://api.thingspeak.com/channels/98203/feeds.json?api_key=AUMY5ZJB0YMIUFJW&results=1'
            readings = read_thingspeak_data(url)
            tb.send_message(chat_id, "Temperature: %.1f" % (readings[0]))
            types.ReplyKeyboardRemove()
            tb.send_message(chat_id, "/keyboard, /report?")
        else:
            not_welcome(chat_id)

    @tb.message_handler(regexp="Relative humidity")
    def relative_humidity(message):
        chat_id = message.from_user.id
        if chat_id in users:
            url = 'https://api.thingspeak.com/channels/98203/feeds.json?api_key=AUMY5ZJB0YMIUFJW&results=1'
            readings = read_thingspeak_data(url)
            tb.send_message(chat_id, "Relative humidity: %.1f" % (readings[1]))
            types.ReplyKeyboardRemove()
            tb.send_message(chat_id, "/keyboard, /report?")
        else:
            not_welcome(chat_id)

    @tb.message_handler(regexp="Water flow")
    def water_flow(message):
        chat_id = message.from_user.id
        if chat_id in users:
            url = 'https://api.thingspeak.com/channels/98203/feeds.json?api_key=AUMY5ZJB0YMIUFJW&results=1'
            readings = read_thingspeak_data(url)
            tb.send_message(chat_id, "Water flow: %.1f" % (readings[2]))
            types.ReplyKeyboardRemove()
            tb.send_message(chat_id, "/keyboard, /report?")
        else:
            not_welcome(chat_id)

    @tb.message_handler(regexp="Pump pressure")
    def pump_pressure(message):
        chat_id = message.from_user.id
        if chat_id in users:
            url = 'https://api.thingspeak.com/channels/98203/feeds.json?api_key=AUMY5ZJB0YMIUFJW&results=1'
            readings = read_thingspeak_data(url)
            tb.send_message(chat_id, "Pump pressure: %.1f" % (readings[3]))
            types.ReplyKeyboardRemove()
            tb.send_message(chat_id, "/keyboard, /report?")
        else:
            not_welcome(chat_id)

    @tb.message_handler(regexp="Pond level")
    def pond_level(message):
        chat_id = message.from_user.id
        if chat_id in users:
            url = 'https://api.thingspeak.com/channels/98203/feeds.json?api_key=AUMY5ZJB0YMIUFJW&results=1'
            readings = read_thingspeak_data(url)
            tb.send_message(chat_id, "Pond level: %.1f" % (readings[4]))
            types.ReplyKeyboardRemove()
            tb.send_message(chat_id, "/keyboard, /report?")
        else:
            not_welcome(chat_id)

    @tb.message_handler(regexp="Pump power")
    def pump_power(message):
        chat_id = message.from_user.id
        if chat_id in users:
            url = 'https://api.thingspeak.com/channels/98203/feeds.json?api_key=AUMY5ZJB0YMIUFJW&results=1'
            readings = read_thingspeak_data(url)
            tb.send_message(chat_id, "Pump power: %.1f" % (readings[5]))
            types.ReplyKeyboardRemove()
            tb.send_message(chat_id, "/keyboard, /report?")
        else:
            not_welcome(chat_id)

###----Sectors names in Thingspeak----###

# function                button name         command
# "TURN_SYSTEM_MANUAL()"  TURN_SYSTEM_MANUAL  TURN_SYSTEM_AUTO_
# "TURN_SYSTEM_AUTO()"    TURN_SYSTEM_AUTO	  TURN_SYSTEM_MANUAL_
# "TURN_LEAKTEST()"       TURN_LEAKTEST       TURN_LEAKTEST_
# "TURN_ON_ABONO()"       TURN_ON_ABONO       TURN_ON_ABONO_
# "TURN_OFF_ABONO()"      TURN_OFF_ABONO      TURN_OFF_ABONO_
# "TURN_ON_BOMBA()"       TURN_ON_BOMBA       TURN_ON_BOMBA_
# "TURN_OFF_BOMBA()"      TURN_OFF_BOMBA      TURN_OFF_BOMBA_
# "TURN_ON_ALL()"         TURN_ON_ALL         TURN_ON_ALL_
# "TURN_OFF_ALL()"        TURN_OFF_ALL        TURN_OFF_ALL_
#
# "sectorON_1()"          Naranjos ON         TURN_ON_1_
# "sectorOFF_1()"         Naranjos OFF		  TURN_OFF_1_
# "sectorON_2()"          M. Bj Del. ON		  TURN_ON_2_
# "sectorOFF_2()"         M. Bj Del.OFF		  TURN_OFF_2_
# "sectorON_3()"          M. Bj Detras ON	  TURN_ON_3_
# "sectorOFF_3()"         M. Bj Detras OFF	  TURN_OFF_3_
# "sectorON_4()"          M. Alt Del ON		  TURN_ON_4_
# "sectorOFF_4()"         M. Alt Del OFF	  TURN_OFF_4_
# "sectorON_5()"          M. Alt Det ON		  TURN_ON_5_
# "sectorOFF_5()"         M. Alt Det OFF	  TURN_OFF_5_
# "sectorON_6()"          Cesped ON			  TURN_ON_6_
# "sectorOFF_6()"         Cesped OFF		  TURN_OFF_6_
# "sectorON_7()"          Parras 1 ON		  TURN_ON_7_
# "sectorOFF_7()"         Parras 1 OFF		  TURN_OFF_7_
# "sectorON_8()"          Parras 2 ON		  TURN_ON_8_
# "sectorOFF_8()"         Parras 2 OFF		  TURN_OFF_8_
# "sectorON_9()"          Parras 3 ON		  TURN_ON_9_
# "sectorOFF_9()"         Parras 3 OFF		  TURN_OFF_9_
# "sectorON_10()"         Parras 4 ON		  TURN_ON_10_
# "sectorOFF_10()"        Parras 4 OFF		  TURN_OFF_10_
# "sectorON_11()"         Parras 5 ON		  TURN_ON_11_
# "sectorOFF_11()"        Parras 5 OFF		  TURN_OFF_11_
# "sectorON_12()"         Parras 6 ON		  TURN_ON_12_
# "sectorOFF_12()"        Parras 6 OFF		  TURN_OFF_12_
# "sectorON_13()"         Parras Est ON		  TURN_ON_13_
# "sectorOFF_13()"        Parras Est OFF	  TURN_OFF_13_
# "sectorON_14()"         Bodega lado ON	  TURN_ON_14_
# "sectorOFF_14()"        Bodega lado OFF	  TURN_OFF_14_
# "sectorON_15()"         Bodega Alej ON	  TURN_ON_15_
# "sectorOFF_15()"        Bodega Alej OFF	  TURN_OFF_15_
# "sectorON_16()"         Sector 16 ON		  TURN_ON_16_
# "sectorOFF_16()"        Sector 16 OFF		  TURN_OFF_16_
# "sectorON_17()"         Sector 17 ON		  TURN_ON_17_
# "sectorOFF_17()"        Sector 17 OFF		  TURN_OFF_17_
# "sectorON_18()"         Sector 18 ON		  TURN_ON_18_
# "sectorOFF_18()"        Sector 18 OFF		  TURN_OFF_18_

# sectors_index = ['Naranjos', 'M. Bj Del.', 'M. Bj Detras', 'M. Alt Del', 'M. Alt Det', 'Césped', 'Parras 1', 'Parras 2', 'Parras 3', 'Parras 4', 'Parras 5', 'Parras 6', 'Parras Est', 'Bodega lado', 'Bodega Alej', 'Sector 16', 'Sector 17', 'Sector 18', 'Sector 19', 'Sector 20', 'Sector 21', 'Sector 22', 'Sector 23', 'Sector 24']
# index = [1, 2, 3, 4, ... ,]

###----End of sectors names----###

# Send a custom command to open or close valves or command actuators
@tb.message_handler(regexp="Control")
def control(message):
    chat_id = message.from_user.id
    if chat_id in users:
        command.atrib1 = None
        command.atrib2 = None
        names = ['SYSTEM','LEAKTEST','ON','OFF']
        row_width = 2
        one_time_keyboard = True
        msg = "Select action:"
        make_keyboard(names, row_width, one_time_keyboard, msg, chat_id)
        types.ReplyKeyboardRemove()
    else:
        not_welcome(chat_id)

    @tb.message_handler(regexp="SYSTEM")
    def system(message):
        chat_id = message.from_user.id
        if chat_id in users:
            command.atrib1 = message.text
            names = []
            for i in range(len(options_system)):
                names.append(options_system[i])
            row_width = 2
            one_time_keyboard = True
            msg = "Automatic or manual?"
            make_keyboard(names, row_width, one_time_keyboard, msg, chat_id)
            types.ReplyKeyboardRemove()
            sending = True  #Used to avoid always sending no matter the message
            if sending == True:
                @tb.message_handler(func=lambda message: message.text in options_system)
                def send_command(message):
                    chat_id = message.from_user.id
                    command.atrib2 = message.text
                    atribs = 2
                    send_url(atribs)
                    tb.send_message(chat_id, "/keyboard, /report?")
        else:
            not_welcome(chat_id)

    @tb.message_handler(regexp="LEAKTEST")
    def leaktest(message):
        chat_id = message.from_user.id
        if chat_id in users:
            command.atrib1 = message.text
            atribs = 1
            send_url(atribs)
            tb.send_message(chat_id, "/keyboard, /report?")
        else:
            not_welcome(chat_id)

    @tb.message_handler(regexp="^ON$")
    def run_sector(message):
        chat_id = message.from_user.id

        if chat_id in users:
            command.atrib1 = message.text
            names = options_on_off
            row_width = 3
            one_time_keyboard = True
            msg = "Select sector:"
            make_keyboard(names, row_width, one_time_keyboard, msg, chat_id)
            types.ReplyKeyboardRemove()
            sending = True #Used to avoid always sending no matter the message

            if sending == True:
                @tb.message_handler(func=lambda message: message.text in options_on_off)
                def send_command(message):
                    chat_id = message.from_user.id
                    msg = message.text
                    command.atrib2 = options_on_off.index(msg) - 2 #-2 to correct the index
                    atribs = 2
                    if command.atrib2 < 1: #This means it is either ALL, ABONO or BOMBA
                        command.atrib2 = msg
                    send_url(atribs)
                    tb.send_message(chat_id, "/keyboard, /report?")
        else:
            not_welcome(chat_id)

    @tb.message_handler(regexp="OFF")
    def stop_sector(message):
        chat_id = message.from_user.id

        if chat_id in users:
            command.atrib1 = message.text
            names = options_on_off
            row_width = 3
            one_time_keyboard = True
            msg = "Select sector:"
            make_keyboard(names, row_width, one_time_keyboard, msg, chat_id)
            types.ReplyKeyboardRemove()
            sending = True #Used to avoid always sending no matter the message

            if sending == True:
                @tb.message_handler(func=lambda message: message.text in options_on_off)
                def send_command(message):
                    chat_id = message.from_user.id
                    msg = message.text
                    command.atrib2 = options_on_off.index(msg) - 2 #-2 to correct the index
                    atribs = 2

                    if command.atrib2 < 1: #This means it is either ALL, ABONO or BOMBA
                        command.atrib2 = msg
                    send_url(atribs)
                    tb.send_message(chat_id, "/keyboard, /report?")

        else:
            not_welcome(chat_id)

tb.polling()
