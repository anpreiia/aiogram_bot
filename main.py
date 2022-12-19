import aiogram as iog
import time as time

import game as game
import DB as gdb

API_TOKEN = 'Bot token here!'

HELP_MESSAGE = "You can plant tulips (🌷) which take 30 seconds to grow.\n" \
                "The seeds cost 15💵.\n" \
                "Tulips can be sold for 20💵.\n" \
                "\n" \
                "/info - shows farm\n" \
                "/buy <number from 1 to 10> or all - Buy seeds(🌱) and plant in place(🕳)\n" \
                "/sell - sell all grown tulips(🌷)\n"

bot = iog.Bot(token=API_TOKEN)
dp = iog.Dispatcher(bot)


def log_message(message: iog.types.Message):
    print(f"{time.strftime('[%H:%M:%S][%d/%m/%Y]', time.gmtime())} {message.from_user.id}: {message.text}")


def keyboard():
    kb = [
        [
            iog.types.KeyboardButton(text="/info"),
            iog.types.KeyboardButton(text="/sell"),
            iog.types.KeyboardButton(text="/buy all")
        ],
    ]
    return iog.types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Choose an action"
    )


@dp.message_handler(commands=['sell'])
async def command_sell(message: iog.types.Message):
    log_message(message)
    pdata = gdb.player_get(message.from_user.id)
    if not pdata:
        await message.answer("Enter /start",
                             reply_markup=keyboard())
    else:
        sell_result = game.sell_all(pdata[1])
        pdata[0] += sell_result[0]
        pdata[1] = sell_result[1]
        gdb.player_update(message.from_user.id, pdata[0], pdata[1])
        await message.answer(game.draw_garden(pdata[1]) + "\n\n you have: " + str(pdata[0]) + "💵",
                             reply_markup=keyboard())


@dp.message_handler(commands=['buy'])
async def command_buy(message: iog.types.Message):
    log_message(message)
    args = message.text.split()
    pdata = gdb.player_get(message.from_user.id)
    if not pdata:
        await message.answer("Enter /start",
                             reply_markup=keyboard())
    else:
        if len(args) < 2:
            await message.answer("Enter /buy <number from 1 to 10> or /buy all",
                                 reply_markup=keyboard())
        elif str.isdigit(args[1]) is False and args[1] != "all":
            await message.answer("Enter /buy <number from 1 to 10> or /buy all",
                                 reply_markup=keyboard())
        else:
            if args[1] == "all":
                buy_result = game.buy_in_renge([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], pdata[0], pdata[1], "TULP")
            else:
                buy_result = game.buy_in_renge([int(args[1]) - 1], pdata[0], pdata[1], "TULP")

            if buy_result:
                pdata[0] = buy_result[0]
                pdata[1] = buy_result[1]
                gdb.player_update(message.from_user.id, pdata[0], pdata[1])
                await message.answer(game.draw_garden(pdata[1]) + "\n\n you have: " + str(pdata[0]) + "💵",
                                     reply_markup=keyboard())
            else:
                await message.answer("Enter /buy <number from 1 to 10> or /buy all",
                                     reply_markup=keyboard())


@dp.message_handler(commands=['info'])
async def command_info(message: iog.types.Message):
    log_message(message)
    pdata = gdb.player_get(message.from_user.id)
    if not pdata:
        await message.answer("Enter /start")
    else:
        await message.answer(game.draw_garden(pdata[1]) + "\n\n you have: " + str(pdata[0]) + "💵",
                             reply_markup=keyboard())


@dp.message_handler(commands=['start'])
async def command_start(message: iog.types.Message):
    log_message(message)
    pdata = gdb.player_get(message.from_user.id)
    if not pdata:
        gdb.player_create(message.from_user.id)
        await message.answer(HELP_MESSAGE + "\n" + game.draw_garden(pdata[1]) + "\n\n you have: " + str(pdata[0]) + "💵",
                             reply_markup=keyboard())
    else:
        await message.answer("Enter /help for a list of commands",
                             reply_markup=keyboard())


@dp.message_handler(commands=['help'])
async def command_help(message: iog.types.Message):
    log_message(message)
    await message.answer(HELP_MESSAGE,
                         reply_markup=keyboard())


if __name__ == '__main__':
    iog.executor.start_polling(dp, skip_updates=True)
