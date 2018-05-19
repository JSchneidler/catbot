from Bot import Bot
from time import sleep

bot = Bot();

'''
bot.updateBot(100, 90);
sleep(3);
bot.stop();
'''

bot.updateBot(100, 0);
sleep(3);
bot.updateBot(100, 45);
sleep(3);
bot.updateBot(100, 90);
sleep(3);
bot.updateBot(100, 135);
sleep(3);
bot.updateBot(100, 180);
sleep(3);
bot.updateBot(100, -135);
sleep(3);
bot.updateBot(100, -90);
sleep(3);
bot.updateBot(100, -45);
sleep(3);
bot.stop();