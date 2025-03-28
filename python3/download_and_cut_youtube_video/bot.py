from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from download_and_cut import download_and_cut
from download_and_cut import download_video

ALLOWED_USERS = [
]
TOKEN = ""


def check_permissions(update: Update):
    if update.effective_user.id not in ALLOWED_USERS:
        print(f"{update.effective_user.id} {update.message.text} - rejected.")
        return False

    return True


async def start(update: Update, context):
    if check_permissions(update):
        await update.message.reply_text("Commands:\n{}\n{}\n\n{}\n{}".format(
            "/download url - download youtube video",
            "example:\n/download https://www.youtube.com/watch?v=1a2b3c4d5e",
            "/cut url time1 time2 - download and cut a piece from it",
            "example:\n/cut https://www.youtube.com/watch?v=1a2b3c4d5e 0:25 1:10"
        ))


async def cut(update: Update, context):
    if check_permissions(update):
        text = update.message.text
        args = text.split(" ")
        args.pop(0)
        try:
            await update.message.reply_text("Your cut request is processing ...")
            video = download_and_cut(args)
            await update.message.reply_video(video=open(video, "rb"))
        except Exception as exception:
            await update.message.reply_text(f"{exception}")
        return


async def download(update: Update, context):
    if check_permissions(update):
        text = update.message.text
        args = text.split(" ")
        args.pop(0)
        try:
            await update.message.reply_text("Your download request is processing ...")
            video = download_video(args[0])
            await update.message.reply_video(video=open(video, "rb"))
        except Exception as exception:
            await update.message.reply_text(f"{exception}")
        return


async def echo(update: Update, context):
    if check_permissions(update):
        await update.message.reply_text(f"use /start")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cut", cut))
    app.add_handler(CommandHandler("download", download))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot is running")
    app.run_polling()


if __name__ == "__main__":
    main()
