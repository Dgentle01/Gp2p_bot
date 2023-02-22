bot_token = os.environ.get('6080004505:AAGILWQ0WlbXEzxKlAU43lfkHMGe4y3O_t4')
bot = telegram.Bot(token=bot_token)

webhook_url = "https://github.com/Dgentle01/Gp2p_bots.git"
bot.setWebhook(webhook_url)