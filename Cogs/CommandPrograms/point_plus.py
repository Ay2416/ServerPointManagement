# Discord bot import
import discord
import os
import glob
import ndjson

# My program import
# none

data_location = "./data"

class plus:
    async def plus_info(self, interaction, plus_point, user):
        await interaction.response.defer(ephemeral=False)

        # 指定された加算するポイントがプラスの値であるかどうか
        if plus_point < 0:
            embed=discord.Embed(title="エラー!", description="入力された加算値がプラスではありません！\n入力した内容を確認してください。", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return

        # もしギルドのndjsonファイルがなければ作成
        files = glob.glob(data_location + '/guild_json/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                judge = 1
                break

        if judge != 1:
            # 0から追加
            point = 0 + plus_point

            content = {
                "user": user.id,
                "point" : point
            }

            with open(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson', 'a') as f:
                writer = ndjson.writer(f)
                writer.writerow(content)
                
        else:
            # ndjsonのデータに既にそのユーザーがいるかを確認
            with open(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson') as f:
                    read_data = ndjson.load(f)
            
            judge = 0
            location = 9
            for i in range(0, len(read_data)):
                 if read_data[i]["user"] == user.id:
                     judge = 1
                     location = i
                     break
 
            # なければ0から追加
            if judge != 1:
                point = 0 + plus_point

                content = {
                    "user": user.id,
                    "point" : point
                }
            
                with open(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson', 'a') as f:
                    writer = ndjson.writer(f)
                    writer.writerow(content)
            
            # あればそれに加算
            else:
                point = read_data[location]["point"] + plus_point
                read_data[location]["point"] = point
                
                os.remove(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson')

                for i in range(0, len(read_data)):
                    with open(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson', 'a') as f:
                        writer = ndjson.writer(f)
                        writer.writerow(read_data[i])
            
        # 結果をDiscordに表示
        embed=discord.Embed(title="成功！", description="<@" + str(user.id) + ">さんのポイントを" + str(plus_point) + "ポイント加算しました！", color=0x00ff7f)
        embed.add_field(name="現在のポイント", value=str(point) + "ポイント", inline=False)
        await interaction.followup.send(embed=embed)

