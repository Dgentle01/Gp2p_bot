import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Define the constants for the different states in the conversation handler
PAYMENT, CONFIRMATION, DISPUTE = range(3)

# Define the 'start' command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to the P2P payment bot. To send money, use the /pay command.')

# Define the 'pay' command handler
def pay(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter the amount you wish to send:')
    return PAYMENT

# Define the function to handle user input for payment
def payment_handler(update, context):
    # Save the payment amount to the user's context
    context.user_data['payment_amount'] = update.message.text

    # Ask for confirmation
    context.bot.send_message(chat_id=update.effective_chat.id, text='You entered: ' + context.user_data['payment_amount'] + '\n\nIs this correct? (yes/no)')
    return CONFIRMATION

# Define the function to handle user confirmation for payment
def confirmation_handler(update, context):
    confirmation = update.message.text.lower()

    if confirmation == 'yes':
        # Proceed with the payment and send a message to the receiver
        receiver_id = '123456789'  # Replace with the receiver's chat ID
        context.bot.send_message(chat_id=receiver_id, text='You have received ' + context.user_data['payment_amount'] + ' from user ' + str(update.effective_chat.id))

        # Clear the user data and end the conversation
        context.user_data.clear()
        context.bot.send_message(chat_id=update.effective_chat.id, text='Payment successful.')
        return ConversationHandler.END
    else:
        # Cancel the payment and end the conversation
        context.user_data.clear()
        context.bot.send_message(chat_id=update.effective_chat.id, text='Payment cancelled.')
        return ConversationHandler.END

# Define the 'cancel' command handler
def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Conversation cancelled.')
    return ConversationHandler.END

# Define the 'dispute' command handler
def dispute(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please describe the dispute in detail:')
    return DISPUTE

# Define the function to handle disputes
def dispute_handler(update, context):
    dispute_message = update.message.text
    dispute_chat_id = update.effective_chat.id

    # Send the dispute message to the dispute resolution channel
    context.bot.send_message(chat_id='dispute_resolution_channel', text='New dispute from user ' + str(dispute_chat_id) + ': ' + dispute_message)

    # Confirm that the dispute has been received
    context.bot.send_message(chat_id=dispute_chat_id, text='Your dispute has been received. An admin will review and respond as soon as possible.')

    return ConversationHandler.END

# Create the updater and dispatcher objects

# updater = Updater('6080004505:AAGILWQ0WlbXEzxKlAU43lfkHMGe4y3O_t4')
# dispatcher = updater.dispatcher

# Add the conversation handlers to the dispatcher
payment_handler = ConversationHandler(
    entry_points=[CommandHandler('pay', pay)],
    states={
        PAYMENT: [MessageHandler(Filters.regex('^[0-9]+(\.[0-9]{1,2})?$'), payment_handler)],
        CONFIRMATION: [MessageHandler(Filters.regex('^(yes|no)$'), confirmation_handler)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

# Set up the updater and dispatcher
updater = Updater(token='6080004505:AAGILWQ0WlbXEzxKlAU43lfkHMGe4y3O_t4', use_context=True)
dispatcher = updater.dispatcher

# Add the conversation handler to the dispatcher
dispatcher.add_handler(conv_handler)

# Start the bot
updater.start_polling()
updater.idle()

print(pay(update, context))