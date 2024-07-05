import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from modules.csv_read_and_classify import classify_order_id
from modules.scrapper_thestore import scrap_status_thestore
from modules.scrapper_webstore import track_order_web
from modules.dump_to_csv import dump_to_csv
import pandas as pd

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define your functions to handle commands and messages
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Send me a CSV file with order numbers to start.')

async def handle_file(update: Update, context: CallbackContext) -> None:
    file = await update.message.document.get_file()
    await file.download_to_drive('input.csv')
    await update.message.reply_text('File received. Processing...')

    # Process the file
    try:
        income_df = pd.read_csv('input.csv')
        thestore_orders_ids, webstore_orders_ids = classify_order_id(income_df)
        the_results = scrap_status_thestore(thestore_orders_ids)
        web_results = track_order_web(webstore_orders_ids) or {}
        all_results = {**the_results, **web_results}
        dump_to_csv(all_results, 'output/orders.csv')

        # Send the result file back to the user
        with open('output/orders.csv', 'rb') as f:
            await update.message.reply_document(f)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6259933715:AAFUWA4AEhTQJEd1yd1kHr1JiYkRr75I1ng").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - handle CSV file
    application.add_handler(MessageHandler(filters.Document.FileExtension("csv"), handle_file))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
