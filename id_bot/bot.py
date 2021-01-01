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

    def __init__(self, prefix=None, token=None):
        self._cog_list = []
        self._init_time = datetime.utcnow()

        self.prefix = prefix
        self.token = token

        super().__init__(
            command_prefix=self.prefix,
            description=f"ID 봇: v{__version__}",
            help_command=None
        )

    async def on_connect(self):
        logger.info("디스코드 서버와 연결되었습니다.")

    async def on_disconnect(self):
        logger.info("디스코드 서버와의 연결이 해제되었습니다.")

    async def on_ready(self):
        if not self._cog_list:
            self._cog_list = [os.path.splitext(cog)[0]
                              for cog in os.listdir("id_bot/cogs")
                              if os.path.isfile(f"id_bot/cogs/{cog}")]

        for cog in self._cog_list:
            try:
                logger.info(f"추가 기능 `{cog}`을/를 로드 중입니다...")

                self.load_extension(f"cogs.{cog}")
            except Exception as error:
                logger.warning(
                    f"추가 기능 `{cog}`을/를 로드할 수 없습니다: \"{error}\""
                )

        logger.info("ID 봇 가동 준비가 완료되었습니다.")

    def run(self, *args, **kwargs):
        """
        `discord.Client`의 `run` 함수.
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
