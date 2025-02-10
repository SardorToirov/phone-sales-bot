from telegram.ext import ContextTypes,Application,CommandHandler,MessageHandler,CallbackQueryHandler,filters
from telegram import Update,KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove
from telegram.constants import ChatAction
TOKEN = "YOUR_TOKEN"

import json

notebooks  = json.loads(open("./j.json").read())
global place

async def stat_funct(update:Update,context:ContextTypes.DEFAULT_TYPE):

    buttons = [
        [KeyboardButton(text="My info"),KeyboardButton(text="Product")]
    ]
    await update.message.reply_text(
        text="Menu",

        reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True,one_time_keyboard=True)
    )

async def message_h(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    user = update.message.from_user
    if query == "My info":
        info = (f"ism: {user.first_name}\n"
                f"familyasi: {user.last_name}\n"
                f"username: @{user.username}\n"
                f"user id: {user.id}"
                )

        await update.message.reply_text(info)

    elif query == "Product":

        place = []
        for i in range(len(notebooks)):
            place.append([InlineKeyboardButton(text=f"{notebooks[i]['model']}", callback_data=f"notebooks_elements_{i}")])

        place.append([InlineKeyboardButton(text="back",callback_data="Notebooks_back")])
        await update.message.reply_text(text="Telefonlar royhati:",reply_markup=InlineKeyboardMarkup(place))

async def inline_h(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data_sp = str(query.data).split('_')
    if data_sp[0] == "notebooks":
        if data_sp[1] == "back":
            print(data_sp[1])
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)

        elif data_sp[1] == "elements":
            if data_sp[2] == "back":
                await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)

                buttons = []

                for i in range(len(notebooks)):
                    # i da element raqami kevoti bottinga jsondagi malumotimiz bervomiz
                    buttons.append(
                        [InlineKeyboardButton(text=notebooks[i]['model'], callback_data=f"notebooks_elements_{i}")])
                buttons.append([InlineKeyboardButton(text="back", callback_data="notebooks_back")])
                await query.message.reply_text(text="<b>Notebooks tanlang </b>",
                                               reply_markup=InlineKeyboardMarkup(buttons),
                                               parse_mode="HTML")
            else:

                index = int(data_sp[2])
                notebook = notebooks[index]
                details = (
                           f"Model: {notebook['model']}\n"
                           f"Brend: {notebook['brend']}\n"
                           f"Narxi: {notebook['narx']}\n"
                           f"Rangi: {notebook['rang']}\n"
                           f"Miqdori: {notebook['miqdor']}\n"
                           f"rasmi: {notebook['profile_picture']}"
                          )
                buton = [[InlineKeyboardButton(text="back", callback_data="notebooks_back")]]
                await query.message.reply_text(text=details, reply_markup=InlineKeyboardMarkup(buton),
                                               parse_mode="HTML")


applicaton = Application.builder().token(TOKEN).build()
applicaton.add_handler(CommandHandler('start',stat_funct))
applicaton.add_handler(MessageHandler(filters.TEXT,message_h))
applicaton.add_handler(CallbackQueryHandler(inline_h))
applicaton.run_polling()



