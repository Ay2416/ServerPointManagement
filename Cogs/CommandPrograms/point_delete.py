# Discord bot import
import discord
import os
import glob
import ndjson

# My program import
# none

data_location = "./data"

class delete:
    async def delete_info(self, interaction, user):
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
            embed=discord.Embed(title="エラー!", description="このサーバーにはポイントデータがありません。", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return

        # ユーザーのポイントデータがあるかどうかを確認
        with open(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson') as f:
            read_data = ndjson.load(f)
            
        judge = 0
        location = 0
        for i in range(0, len(read_data)):
                if read_data[i]["user"] == user.id:
                    judge = 1
                    location = i
                    break
        
        if judge != 1:
            embed=discord.Embed(title="エラー!", description="そのユーザーのポイントデータがありません。", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return

        # もしサーバーのデータの個数が1つしかなければ、ファイルごと削除する ※その場合は、ここで処理を終了させる
        if len(read_data) == 1:
            os.remove(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson')
            embed=discord.Embed(title="成功しました！", description="<@" + str(user.id) + ">さんのポイントデータを削除しました。", color=0x00ff7f)
            await interaction.followup.send(embed=embed)
            return

        # そのユーザーのデータを削除
        os.remove(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson')

        for i in range(0, len(read_data)):
            if i != location:
                with open(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson', 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(read_data[i])

        # 結果をDiscordに表示
        embed=discord.Embed(title="成功しました！", description="<@" + str(user.id) + ">さんのポイントデータを削除しました。", color=0x00ff7f)
        await interaction.followup.send(embed=embed)