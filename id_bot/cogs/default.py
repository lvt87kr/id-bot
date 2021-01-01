#
# MIT License
#
# Copyright (c) 2020 dennis0324, lvt87kr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import discord
from discord.ext import commands

from id_bot import __version__


def setup(bot):
    """
    `discord.commands.Bot.load_extension()`에서 사용되는 함수.
    """

    bot.add_cog(Default(bot))


class Default(commands.Cog):
    """
    ID 봇의 추가 기능 `roles`를 나타내는 클래스.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """
        ID 봇의 `help` 명령어.
        """

        color_ok = self.bot.colors["ok"]

        if not color_ok:
            color_ok = discord.Color.teal()

        await ctx.send(
            embed=discord.Embed(
                title="도움말",
                description="...",
                color=color_ok
            ).set_footer(
                text=f"id-bot v{__version__}",
                icon_url=self.bot.user.avatar_url
            )
        )
