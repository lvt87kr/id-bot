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

from discord.ext import commands


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

        self.help_dict = defaultdict(list)

    @staticmethod
    def is_int(self, num_str):
        """
        주어진 문자열 `num_str`를 숫자로 변환할 수 있는지 확인한다.
        """

        return num_str.lstrip("-+").isdigit()

    @commands.command(
        aliases=["purge"],
        brief="메시지를 일정 개수만큼 삭제합니다.",
        help="메시지를 일정 개수만큼 삭제합니다.\n\n"
             "`count`는 삭제할 메시지의 개수를 나타내며, 0보다 크고 100보다 작은 정수입니다. "
             "`silent_mode`는 명령어의 실행 결과를 보여줄 것인지를 나타내며, 값을 따로 입력하지 "
             "않거나 0일 경우 실행 결과를 보여주고, 값이 1일 경우 실행 결과를 보여주지 않습니다.\n",
        usage="<count> [silent_mode]"
    )
    async def clear(self, ctx, count=5, silent_mode=False):
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
        brief="등록된 명령어의 목록을 보여주거나, 특정 명령어의 도움말을 보여줍니다.",
        help="등록된 명령어의 목록을 보여주거나, 특정 명령어의 도움말을 보여줍니다."
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

                    await self.bot.send_embed(
                        ctx,
                        self.bot.colors["ok"],
                        f"도움말 📖: `{cmd.name}`",
                        f"사용법: `{cmd.name} {cmd.usage}`\n\n"
                        f"```{cmd.help}```\n"
                    )

            if not found:
                raise commands.errors.CommandNotFound()
