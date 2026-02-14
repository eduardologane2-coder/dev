from telegram.ext import CommandHandler, MessageHandler, filters
from metrics_engine import metrics_status
from alignment_handler import alignment_status
from long_term_handler import long_term_status_handler

def register_handlers(app, handle):
    app.add_handler(CommandHandler("metrics", lambda u, c: u.message.reply_text(metrics_status())))
    app.add_handler(CommandHandler("alignment", alignment_status))
    app.add_handler(CommandHandler("longterm", long_term_status_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
