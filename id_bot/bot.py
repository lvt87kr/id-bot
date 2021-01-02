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

from datetime import datetime
import logging
import os
import sys

import discord
from discord.ext import commands

from id_bot import __version__


logger = logging.getLogger('id-bot')


class IDBot(commands.Bot):
    """
    ID 봇을 나타내는 클래스.
    """

    def __init__(self, colors=None, prefix=None, token=None):
        self._cog_list = []
        self._init_time = datetime.utcnow()

        self.colors = {}
        self.loaded_cogs = []
        self.register_colors(colors)

        self.prefix = prefix
        self.token = token

        super().__init__(
            command_prefix=self.prefix,
            description=f"ID 봇: v{__version__}",
            help_command=None,
            intents=discord.Intents.all()
        )

    async def on_command_error(self, ctx, error):
        await self.handle_error(ctx, error)

    async def on_connect(self):
        logger.info("디스코드 서버와 연결되었습니다.")

    async def on_disconnect(self):
        logger.info("디스코드 서버와의 연결이 해제되었습니다.")

    async def on_ready(self):
        self.load_cogs()

        logger.info("ID 봇 가동 준비가 완료되었습니다. (종료하시려면 CTRL+C를 입력해주세요.)")

    def get_uptime(self):
        return datetime.utcnow() - self._init_time

    def get_version(self):
        return __version__

    async def handle_error(self, ctx, error):
        """
        봇 가동 중에 발생하는 오류를 처리한다.
        """

        if isinstance(error, commands.errors.BadArgument):
            logger.info(
                f"사용자 `{ctx.author}`이/가 명령어 `{ctx.message.content}`에"
                "잘못된 인수를 사용하였습니다."
            )

            await self.send_embed(
                ctx,
                self.colors["error"],
                "명령어 형식이 올바르지 않습니다.",
                "명령어를 실행할 때 형식에 맞는 값을 입력해주세요."
            )
        elif isinstance(error, commands.errors.CheckFailure):
            pass
        elif isinstance(error, commands.errors.CommandNotFound):
            logger.info(
                f"사용자 `{ctx.author}`이/가 존재하지 않는 명령어"
                f"`{ctx.message.content}`을/를 사용하였습니다."
            )

            await self.send_embed(
                ctx,
                self.colors["error"],
                "존재하지 않는 명령어입니다.",
                "명령어를 정확하게 입력했는지 확인해보세요."
            )
        elif isinstance(error, commands.errors.CommandOnCooldown):
            pass
        elif isinstance(error, commands.errors.DisabledCommand):
            pass
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            pass
        elif isinstance(error, discord.Forbidden):
            logger.error(
                f"ID 봇이 명령어 `{ctx.message.content}`을/를 실행하려고 했으나 "
                f"권한이 없어 실패했습니다."
            )

            await self.send_embed(
                ctx,
                self.colors["error"],
                "권한이 없습니다.",
                "ID 봇이 이 명령어를 실행하기 위한 권한을 가지고 있지 않습니다."
            )
        else:
            pass

    def load_cogs(self):
        """
        추가 기능을 로드한다.
        """

        self.loaded_cogs = []

        if not self._cog_list:
            self._cog_list = [os.path.splitext(cog)[0]
                              for cog in os.listdir("id_bot/cog")
                              if os.path.isfile(f"id_bot/cog/{cog}")]

        # 추가 기능을 로드한다.
        for cog in self._cog_list:
            try:
                logger.info(f"추가 기능 `{cog}`을/를 로드 중입니다...")

                self.load_extension(f"cog.{cog}")
                self.loaded_cogs.append(cog)
            except Exception as error:
                logger.warning(
                    f"추가 기능 `{cog}`을/를 로드할 수 없습니다: \"{error}\""
                )

    def register_colors(self, colors):
        """
        설정 데이터에 저장된 색상 정보를 등록한다.
        """

        for key, value in colors.items():
            self.colors[key] = discord.Color(int(value, 16))

    def reload_cogs(self):
        """
        추가 기능을 다시 로드한다.
        """

        self.loaded_cogs = []

        if self._cog_list:
            for cog in self._cog_list:
                try:
                    logger.info(f"추가 기능 `{cog}`을/를 다시 로드 중입니다...")

                    self.reload_extension(f"cog.{cog}")
                    self.loaded_cogs.append(cog)
                except Exception as error:
                    logger.warning(
                        f"추가 기능 `{cog}`을/를 다시 로드할 수 없습니다: \"{error}\""
                    )

    def run(self, *args, **kwargs):
        """
        `discord.Client`의 `run` 함수의 오버라이드이다.
        """

        try:
            self.loop.run_until_complete(self.start(self.token))
        except discord.LoginFailure:
            logger.error(
                "올바르지 않은 봇 토큰입니다. "
                "봇 토큰을 다시 설정해주세요."
            )

            sys.exit(1)
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())
        finally:
            self.loop.close()

    async def send_embed(self, ctx, color, title, description):
        """
        `discord.Embed` 형식의 메시지를 채널로 보낸다.
        """

        await ctx.send(
                embed=discord.Embed(
                    title=title,
                    description=description,
                    color=color
                ).set_footer(
                    text=f"id-bot v{__version__}",
                    icon_url=self.user.avatar_url
                )
            )
