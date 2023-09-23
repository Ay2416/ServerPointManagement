# Discord bot import
import discord
import os
import glob
import ndjson
import asyncio

# My program import
# none

data_location = "./data"

class list:
    async def list_info(self, interaction):
        await interaction.response.defer(ephemeral=False)

        # このサーバーのデータがあるのかの確認
        files = glob.glob(data_location + '/guild_json/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                judge = 1
                break
        
        if judge != 1:
            embed=discord.Embed(title="エラー!", description="このサーバーにはポイントデータがありません。\n詳しくはサーバー管理者へご連絡ください。", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return

        # あればDiscord上に表示する
        with open(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson') as f:
            read_data = ndjson.load(f)

        embed=discord.Embed(title="全プレイヤーポイント一覧")

        cut = 25
        for i in range(0, len(read_data)):
            embed.add_field(name="",
                            value="**" + str(i+1) + ".<@" + str(read_data[i]["user"]) + ">**\n" + str(read_data[i]["point"]) + " ポイント", inline=False)
            if i == len(read_data) - 1:
                #表示させる
                await interaction.followup.send(embed=embed)
                return
            
            if i + 1 == cut:
                cut = cut + 25
                #表示させる
                await interaction.followup.send(embed=embed)
                embed=discord.Embed(title="")
                
                # DiscordのWebhook送信制限に引っかからないための対策　※効果があるかは不明
                await asyncio.sleep(2)
