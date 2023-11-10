import time

from MyTelegramBot import MyTelegramBot
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


async def get_prices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html("Пару сек")

    await stop_bot(bot_class.bot)

def start_bot(bot):
    bot.run_polling(allowed_updates=Update.ALL_TYPES)

async def stop_bot(bot):
    await bot.updater.shutdown()

    d = 1





if __name__ == "__main__":
    bot_class = MyTelegramBot()
    bot_class.bot.add_handler(CommandHandler("get_prices", get_prices))
    start_bot(bot_class.bot)

    print("Start")









