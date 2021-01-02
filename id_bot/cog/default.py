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

from collections import defaultdict

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
    ID 봇의 추가 기능 `default`를 나타내는 클래스.
    """

    def __init__(self, bot):
        self.bot = bot

        # `dict` 타입이랑 비슷하지만 키에 배열을 저장할 수 있음!
        self.help_dict = defaultdict(list)

    @commands.command(
        aliases=["cl", "purge"],
        brief="메시지를 일정 개수만큼 삭제합니다.",
        help="메시지를 일정 개수만큼 삭제합니다.\n\n"
             "`count`는 삭제할 메시지의 개수를 나타내며, 0보다 크고 100보다 작은 정수입니다. "
             "`silent_mode`는 명령어의 실행 결과를 보여줄 것인지를 나타내며, 따로 입력하지 않거나 "
             "0일 경우 실행 결과를 보여주고, 값이 1일 경우 실행 결과를 보여주지 않습니다.\n",
        usage="<count> [silent_mode]"
    )
    async def clear(self, ctx, count=3, silent_mode=False):
        if count < 1 or count > 99:
            await self.bot.send_embed(
                ctx,
                self.bot.colors["error"],
                "오류",
                "`count`는 0보다 크고 100보다 작은 정수여야 합니다."
            )
        else:
            try:
                result = await ctx.channel.purge(limit=count)

                if not silent_mode:
                    await self.bot.send_embed(
                        ctx,
                        self.bot.colors["ok"],
                        "실행 결과",
                        "총 {}개의 메시지가 삭제되었습니다.".format(len(result))
                    )
            except Exception as error:
                await self.bot.handle_error(ctx, error)

    @commands.command(
        aliases=["hl"],
        brief="등록된 명령어의 목록을 보여주거나, 특정 명령어의 도움말을 보여줍니다.",
        help="등록된 명령어의 목록을 보여주거나, 특정 명령어의 도움말을 보여줍니다. "
             "`command`는 도움말을 확인할 명령어를 나타내며, 따로 입력하지 않을 경우 "
             "ID 봇에 등록되어 있는 모든 명령어의 목록을 보여줍니다.",
        usage="[command]"
    )
    async def help(self, ctx, cmd_name=None):
        if cmd_name is None:
            if not self.help_dict:
                # 각 명령어의 이름과 설명을 찾고 분류하여, `self.help_dict`에 추가한다.
                for cmd in self.bot.walk_commands():
                    cog_name = cmd.cog.qualified_name
                    self.help_dict[cog_name].append(
                        f"`{cmd.name}`: {cmd.brief}\n"
                    )

            cmd_list = ""

            # 명령어의 이름과 설명을 내림차순으로 정렬한다.
            for cog_name in self.help_dict:
                cmd_list += "\n"

                for text in sorted(self.help_dict[cog_name]):
                    cmd_list += text

            await self.bot.send_embed(
                ctx,
                self.bot.colors["ok"],
                "도움말 📖",
                cmd_list,
            )
        else:
            found = False

            for cmd in self.bot.walk_commands():
                if cmd.name == cmd_name:
                    found = True

                    aliases = ", ".join(f"`{alias}`" for alias in cmd.aliases)
                    usage = f" {cmd.usage}" if cmd.usage is not None else ""

                    await self.bot.send_embed(
                        ctx,
                        self.bot.colors["ok"],
                        f"도움말 📖: `{cmd.name}`",
                        f"단축 명령어: {aliases}\n"
                        f"사용법: `{cmd.name}{usage}`\n\n"
                        f"```{cmd.help}```\n"
                    )

            if not found:
                raise commands.errors.CommandNotFound()

    @commands.command(
        aliases=["rl"],
        brief="모든 추가 기능을 다시 로드합니다.",
        help="모든 추가 기능을 다시 로드합니다. 추가 기능 로드 중에 오류가 발생할 경우 "
             "봇 로그를 확인해주세요."
    )
    async def reload(self, ctx):
        try:
            self.bot.reload_cogs()

            await self.bot.send_embed(
                ctx,
                self.bot.colors["ok"],
                "추가 기능을 다시 로드했습니다.",
                "총 {}개의 추가 기능을 다시 로드했습니다. "
                "({})".format(
                    len(self.bot.loaded_cogs),
                    ", ".join(f"`{cog}`" for cog in self.bot.loaded_cogs)
                )
            )
        except Exception:
            await self.bot.send_embed(
                ctx,
                self.bot.colors["error"],
                "추가 기능을 로드할 수 없습니다.",
                "오류가 발생했습니다. 봇 로그를 확인해주세요.",
            )

    @commands.command(
        aliases=["sinfo", "si"],
        brief="서버 정보를 보여줍니다.",
        help="서버 정보를 보여줍니다. 이 명령어를 사용하면 서버 소유자, 서버의 "
             "멤버 수, 역할 개수 등의 서버 정보를 확인할 수 있습니다."
    )
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            color=self.bot.colors["ok"]
        ).set_author(
            name=ctx.guild.name,
            icon_url=ctx.guild.icon_url
        ).add_field(
            name="서버 소유자",
            value="알 수 없음" if ctx.guild.owner is None
                  else f"{ctx.guild.owner}",
            inline=False
        ).add_field(
            name="서버 인원 수",
            value=ctx.guild.member_count,
            inline=False
        )

        await ctx.send(embed=embed.set_footer(
            text=f"id-bot v{__version__}",
            icon_url=self.bot.user.avatar_url
        ))
