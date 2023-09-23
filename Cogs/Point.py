# discord.py import
import discord
from discord.ext import commands
from discord import app_commands

# My program import
from Cogs.CommandPrograms.point_list import list
from Cogs.CommandPrograms.point_plus import plus
from Cogs.CommandPrograms.point_minus import minus
from Cogs.CommandPrograms.point_delete import delete
from Cogs.CommandPrograms.point_view import view

#@discord.app_commands.guilds(your_guild_id)
class point(app_commands.Group):
    def __init__(self, bot: commands.Bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    # /point *
    # /point plus
    @app_commands.command(name="plus",description="指定されたユーザーのポイントを加算します。また、初めてのユーザーの場合はそのユーザーに0から指定された数字を加算します。")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def point_plus(self, interaction: discord.Interaction,plus_point:int,user:discord.Member):

        await plus().plus_info(interaction, plus_point, user)

    # /point minus
    @app_commands.command(name="minus",description="指定されたユーザーのポイントを減算します。また、初めてのユーザーの場合はそのユーザーに0から指定された数字を減算します。")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def point_minus(self, interaction: discord.Interaction,minus_point:int,user:discord.Member):

        await minus().minus_info(interaction, minus_point, user)

    # /point delete
    @app_commands.command(name="delete",description="指定されたユーザーのポイント情報をリセットし、削除します。")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def point_delte(self, interaction: discord.Interaction,user:discord.Member):

        await delete().delete_info(interaction, user)
    
    # /point view
    @app_commands.command(name="view",description="現在のポイントを表示します。")
    @app_commands.guild_only()
    async def point_view(self, interaction: discord.Interaction):

        await view().view_info(interaction)

    # /point list
    @app_commands.command(name="list",description="サーバー全員のポイント一覧を表示します。")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def point_list(self, interaction: discord.Interaction):

        await list().list_info(interaction)

async def setup(bot: commands.Bot):
    bot.tree.add_command(point(bot, name="point"))