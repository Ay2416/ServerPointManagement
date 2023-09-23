# Discord bot import
import discord
import os
import glob
import ndjson

# My program import
# none

data_location = "./data"

class view:
    async def view_info(self, interaction):
        await interaction.response.defer(ephemeral=False)

        # このサーバーのデータがあるかどうかの確認
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

        # ユーザーのポイントデータがあるかどうかを確認
        with open(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson') as f:
            read_data = ndjson.load(f)
            
        judge = 0
        location = 0
        for i in range(0, len(read_data)):
                if read_data[i]["user"] == interaction.user.id:
                    judge = 1
                    location = i
                    break
        
        if judge != 1:
            embed=discord.Embed(title="エラー!", description="あなたのポイントデータがありません。\n詳しくはサーバー管理者へご連絡ください。", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return

        # 結果をDiscordに表示
        embed=discord.Embed(title="あなたの現在のポイント", color=0x00ff7f)
        embed.add_field(name="現在のポイント", value=str(read_data[location]["point"]), inline=False)
        await interaction.followup.send(embed=embed)