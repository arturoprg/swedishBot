import unidecode
import random

import telegram
from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    InlineQueryHandler,
)

from Palabras import Palabras

class SvensBot(object):

    def __init__(self, token):
        self.bot = telegram.Bot(token=token)

        updater = Updater(token=token, use_context=True)
        dispatcher = updater.dispatcher
        echo_handler = MessageHandler(Filters.text & (~Filters.command), self.echo)
        dispatcher.add_handler(echo_handler)
        dispatcher.add_handler(CommandHandler("start", self._start))
        dispatcher.add_handler(CommandHandler("exit", self._exit))
        dispatcher.add_handler(CommandHandler("add", self._add))
        dispatcher.add_handler(CommandHandler("set", self._set))
        dispatcher.add_handler(PollAnswerHandler(self.receive_poll_answer))

        updater.start_polling()

        self.start = False
        self.set = False
        self.message = ""
        self.fallos = []
        self.first_try = False

    def _start(self, update: Update, context: CallbackContext):
        self.start = True
        self.first_try = True
        self.voc = Palabras('sueco.txt')
        self.max = int(self.voc.max)
        categorias = []
        message = context.bot.send_poll(
            update.effective_chat.id,
            "Which cathegories?",
            self.voc.categorias,
            is_anonymous=False,
            allows_multiple_answers=True,
        )
        # Save some info about the poll the bot_data for later use in receive_poll_answer
        payload = {
            message.poll.id: {
                "questions": self.voc.categorias,
                "message_id": message.message_id,
                "chat_id": update.effective_chat.id,
                "answers": 0,
            }
        }
        context.bot_data.update(payload)

    def _exit(self, update: Update, context: CallbackContext):
        self.start = False

    def _set(self, update: Update, context: CallbackContext):
        self.bot.send_message(text=f"The current maximum of words is {self.voc.max}", chat_id=325879868)
        self.set = True

    def _add(self, update: Update, context: CallbackContext):
        pass

    def receive_poll_answer(self, update: Update, context: CallbackContext) -> None:
        answer = update.poll_answer
        poll_id = answer.poll_id
        selected_options = answer.option_ids

        try:
            questions = context.bot_data[poll_id]["questions"]
        # this means this poll answer update is from an old poll, we can't do our answering then
        except KeyError:
            return
        answer = []

        for question_id in selected_options:
            answer.append(questions[question_id])

        context.bot.stop_poll(
            context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
        )
        print(answer)
        self.dictio = self.voc.palabras_seleccionadas(answer)
        self.send_word()

    def echo(self, update: Update, context: CallbackContext):   # Se ejecuta al recibir un mensaje
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Journal updated!")
        self.message = update.message.text

        # Set new maximum of words
        if self.set and not self.start:
            self.set = False
            self.voc = Palabras('sueco.txt')
            try:
                self.max = int(self.message)
                with open(self.voc.listaTxt,encoding='utf-8') as archivo:
                    texto = archivo.readlines()
                texto[0] = self.message+"\n"
                file1 = open(self.voc.listaTxt,"w")
                file1.writelines(texto)
                file1.close()
                self.voc = Palabras('sueco.txt')
                self.bot.send_message(text=f"Maximum set at {self.voc.max}", chat_id=325879868)

            except:
                print("Error setting maximum of words")


        if self.start:
            self.check_word(self.message)
        if self.start:
            self.send_word()

    def send_word(self):
        self.n = random.randint(0,len(self.dictio)-1)
        self.bot.send_message(text=f"{self.dictio[self.n][1].capitalize()} : ", chat_id=325879868)


    def check_word(self, resp):
        if len(resp) > 1:
            resp = resp[0].upper()+resp[1:].lower()

        if resp.capitalize() == self.dictio[self.n][0].capitalize():
            self.bot.send_message(text="Correcto!", chat_id=325879868)

            if self.first_try:
                self.set_deepness(int(self.dictio[self.n][2])+1)


        else:
            self.bot.send_message(text=f"Incorrecto: {self.dictio[self.n][0].capitalize()}", chat_id=325879868)
            self.fallos.append(self.dictio[self.n])
            self.set_deepness(int(self.dictio[self.n][2])-1)
        del self.dictio[self.n]

        if len(self.dictio) == 0:
            self.first_try = False
            if len(self.fallos) == 0:
                self.bot.send_message(text="Has terminado!!", chat_id=325879868)
                self.start = False
            else:
                self.dictio = list(self.fallos)
                self.fallos = []

    def set_deepness(self,number):
        with open(self.voc.listaTxt,encoding='utf-8') as archivo:
            texto = archivo.readlines()
        if number < 0:
            number = 0
        texto = [linea[:-2]+str(number)+"\n" if ((self.dictio[self.n][0] in linea) and (self.dictio[self.n][1] in linea)) else linea for linea in texto]

        file1 = open(self.voc.listaTxt,"w")
        file1.writelines(texto)
        file1.close()



def main():
    Svenska = SvensBot('5243914114:AAGvLalCchjiiBSMP-8aH36vg-5DDvv9hqI')

main()
