# discord.py import
import discord
from discord.ext import commands

# other import
import os
from dotenv import load_dotenv
import glob
import ndjson

# my program import
# none

# Bot Programs

# load dotenv
load_dotenv()

# 変数
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

data_location = "./data"

# Bot起動時に行う処理
@bot.event
async def on_ready():
    print("接続しました！")

    await bot.change_presence(activity=discord.Game(name="PointManagement"))

    # スラッシュコマンドを同期
    await bot.load_extension("Cogs.Point")
    await bot.load_extension("Cogs.Other")

    await bot.tree.sync()
    print("グローバルコマンド同期完了！")

    #await bot.tree.sync(guild=discord.Object(your_guild_id))
    #print("ギルドコマンド同期完了！")
    
    # dataフォルダがあるかの確認
    files = glob.glob(data_location)
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "data"):
            print("dataファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir(data_location)
        print("dataファイルがなかったため作成しました！")

    # guild_jsonフォルダがあるかの確認
    files = glob.glob(data_location + '/*')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if(os.path.split(files[i])[1] == "guild_json"):
            print("guild_jsonファイルを確認しました！")
            judge = 1
            break

    if judge != 1:
        os.mkdir(data_location + '/guild_json')
        print("guild_jsonファイルがなかったため作成しました！")

# サーバーからキック、BANされた場合に特定の処理をする
@bot.event
async def on_guild_remove(guild):
    files = glob.glob(data_location + '/guild_json/*.ndjson')
    judge = 0

    for i in range(0, len(files)):
        #print(os.path.split(files[i])[1])
        if os.path.split(files[i])[1] == str(guild.id) + ".ndjson":
            judge = 1
            break
    
    if judge == 1:
        os.remove(data_location + "/guild_json/" + str(guild.id))
        print("キックまたはBANされたため、" + str(guild.id) + "のguild jsonを削除しました。")

# サーバーからユーザーが脱退した場合に、そのユーザーのポイントデータを削除する処理
@bot.event
async def on_member_remove(member):
        # このサーバーのデータがあるかどうかの確認
        files = glob.glob(data_location + '/guild_json/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(member.guild.id) + ".ndjson"):
                judge = 1
                break
        
        if judge != 1:
            print("エラー!：このサーバーにはポイントデータがありません。")
            return

        # ユーザーのポイントデータがあるかどうかを確認
        with open(data_location + '/guild_json/' + str(member.guild.id) + '.ndjson') as f:
            read_data = ndjson.load(f)
        
        judge = 0
        location = 0
        for i in range(0, len(read_data)):
                if read_data[i]["user"] == member.id:
                    judge = 1
                    location = i
                    break
        
        if judge != 1:
            print("エラー!：そのユーザーのポイントデータがありません。")
            return

        # もしサーバーのデータの個数が1つしかなければ、ファイルごと削除する ※その場合は、ここで処理を終了させる
        if len(read_data) == 1:
            os.remove(data_location + '/guild_json/' + str(member.guild.id) + '.ndjson')
            print("成功しました！：<@" + str(member.id) + ">さんのポイントデータを削除しました。")
            return

        # そのユーザーのデータを削除
        os.remove(data_location + '/guild_json/' + str(member.guild.id) + '.ndjson')

        for i in range(0, len(read_data)):
            if i != location:
                with open(data_location + '/guild_json/' + str(member.guild.id) + '.ndjson', 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(read_data[i])
        
        print("成功しました！：<@" + str(member.id) + ">さんのポイントデータを削除しました。")

bot.run(os.environ['token'])