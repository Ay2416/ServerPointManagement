# discord.py import
import discord
from discord import app_commands
from discord.ext import commands
import os
import glob

# My program import
# none

data_location = "./data"
# guild_id = your_guild_id

class other(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # /help
    @app_commands.command(name="help",description="コマンドについての簡単な使い方を出します。")
    #@discord.app_commands.guilds(guild_id)
    @app_commands.guild_only()
    async def help_command(self, interaction: discord.Interaction):

        #Discord上にヘルプを表示
        embed=discord.Embed(title="コマンドリスト")
        embed.add_field(name="/point view", value="自分のポイント数を確認します。", inline=False)
        embed.add_field(name="/help", value="このBotのコマンドの一覧を表示します。", inline=False)
        embed.add_field(name="・その他補足事項",
                        value="* このBotに保存されているポイントデータはサーバーごとにユーザー単位で管理されています。\n* ユーザーが退会した場合、そのユーザーのポイントデータは自動的に削除されます。", inline=False)

        '''
        if interaction.guild.id == your_guild_id: # もしサーバー限定コマンドの実装があった場合の表記をした場合はここに書く
            embed.add_field(name="", value="", inline=False)
        '''
        await interaction.response.send_message(embed=embed,ephemeral=False)
    
    # /help_admin
    @app_commands.command(name="help_admin",description="管理者用コマンドについての簡単な使い方を出します。")
    #@discord.app_commands.guilds(guild_id)
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def help_admin_command(self, interaction: discord.Interaction):

        #Discord上にヘルプを表示
        embed=discord.Embed(title="管理者用コマンドリスト")
        embed.add_field(name="/point plus [加算したい1以上のポイント数] [対象ユーザー]", value="※管理者用コマンド\n指定したユーザーのポイント数を加算します。", inline=False)
        embed.add_field(name="/point minus [減算したい-1以下のポイント数 [対象ユーザー]]", value="※管理者用コマンド\n指定したユーザーのポイント数を減算します。", inline=False)
        embed.add_field(name="/point list", value="※管理者用コマンド\nこのサーバーにいる全員分のポイント数を見ることができます。", inline=False)
        embed.add_field(name="/point delete [ポイント数を削除・リセットしたいユーザー]", value="※管理者用コマンド\n指定したユーザーのポイント数をリセットし、削除します。", inline=False)
        embed.add_field(name="/backup", value="※管理者用コマンド\nこのサーバーのポイントデータをバックアップします。", inline=False)
        embed.add_field(name="/restore [復元するためのファイル]", value="※管理者用コマンド\nこのサーバーのポイントデータを復元します。", inline=False)
        embed.add_field(name="・その他補足事項",
                        value="* ここにあるコマンドはサーバーの管理者権限を持っているユーザーのみが実行することができます。", inline=False)

        '''
        if interaction.guild.id == your_guild_id: # もしサーバー限定コマンドの実装があった場合の表記をした場合はここに書く
            embed.add_field(name="", value="", inline=False)
        '''
        await interaction.response.send_message(embed=embed,ephemeral=False)
    
    # /backup
    @app_commands.command(name="backup",description="このサーバーのポイントデータをバックアップします。")
    #@discord.app_commands.guilds(guild_id)
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def backup_command(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

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


        #Discord上に送信
        embed=discord.Embed(title="バックアップに成功しました！", 
                            description="ダウンロードを行ってください。\n復元を行う場合はこのファイルをそのまま\n/restoreコマンドを利用して復元を行ってください。", color=0x00ff7f)
        await interaction.followup.send(embed=embed, file=discord.File(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson'))

    # /restore
    @app_commands.command(name="restore",description="このサーバーのポイントデータを復元・過去のデータに戻します。")
    #@discord.app_commands.guilds(guild_id)
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def restore_command(self, interaction: discord.Interaction, restore_file: discord.Attachment):

        await interaction.response.defer(ephemeral=True)

        # 簡易的なバックアップデータかを確認する処理
        #print(restore_file.filename)
        if str(interaction.guild.id) + ".ndjson" != restore_file.filename:
            embed=discord.Embed(title="エラー!", description="データが異なります。\n添付したファイルを確認してください。", color=0xff0000)
            await interaction.followup.send(embed=embed)
            return 

        # データを置き換える
        # データが存在しているかの確認
        files = glob.glob(data_location + '/guild_json/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                judge = 1
                break
        
        if judge == 1:
            os.remove(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson')

        await restore_file.save(data_location + '/guild_json/' + str(interaction.guild.id) + '.ndjson')

        #Discord上に送信
        embed=discord.Embed(title="復元を行いました！", 
                            description="データを確認してください。", color=0x00ff7f)
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(other(bot))