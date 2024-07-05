from aiogram.utils import executor
from create_google_parser_bot import dp, bot
from handlers import client
import config as cfg



API_TOKEN = cfg.TOKEN
WEBHOOK_HOST = 'https://vlasadasa.ru'
WEBHOOK_PATH = f'/{cfg.TOKEN}/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

async def on_startup(_):
    print('Бот вышел в онлайн\n')
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(_):
    print('Бот вышел в офлайн')
    await bot.delete_webhook()


client.register_handlers_clients(dp)

def main():
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="localhost",
        port=8443
    )

if __name__ == '__main__':
    variant_start = input('Variant start:\n1. Long polling;\n2. Webhook\nYour choice: ')

    if variant_start == '1':
        executor.start_polling(dp, on_shutdown=on_shutdown, skip_updates=True)

    elif variant_start == '2':
        main()

