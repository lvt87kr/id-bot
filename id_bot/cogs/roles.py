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

import logging
import random

import discord

from discord import Color, Permissions
from discord.ext import commands

logger = logging.getLogger('id-bot.cogs.roles')


def setup(bot):
    """
    `discord.commands.Bot.load_extension()`에서 사용되는 함수.
    """

    bot.add_cog(Roles(bot))


class Roles(commands.Cog):
    """
    ID 봇의 추가 기능 `roles`를 나타내는 클래스.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        brief="서버 역할을 관리합니다.",
        help="서버 역할을 관리합니다.\n\n"
             "총 5개의 역할 관리 명령어를 사용할 수 있습니다. `role add`는 새로운 역할을 "
             "생성하고 ID 봇의 데이터베이스에 저장하는 명령어, `role list`는 데이터베이스에 "
             "저장된 역할을 보여주는 명령어, `role remove`는 서버 역할을 삭제하는 명령어이고, "
             "`role set`과 `role unset`은 사용한 사람에게 역할을 부여하거나, 사용한 사람의 "
             "역할을 제거하는 명령어입니다.",
        invoke_without_command=True,
        usage="<command> [...]"
    )
    @commands.check_any(
        commands.is_owner(),
        commands.has_permissions(manage_roles=True)
    )
    async def role(self, ctx):
        # 존재하지 않는 명령어일 경우, 도움말 메시지를 보여준다.
        await ctx.invoke(self.bot.get_command("help"), "role")

    @role.command(
        name="add",
        usage="<role>"
    )
    @commands.check_any(
        commands.is_owner(),
        commands.has_permissions(manage_roles=True)
    )
    async def role_add(self, ctx, name=None):
        if name is None:
            # TODO: 도움말 메시지 추가
            pass
        else:
            logger.info(f"새로운 역할 `{name}`을 생성하는 중입니다...")

            try:
                permissions = Permissions(
                    add_reactions=True,
                    stream=True,
                    read_messages=True,
                    send_messages=True,
                    send_tts_messages=True,
                    attach_files=True,
                    read_message_history=True,
                    connect=True,
                    speak=True,
                    change_nickname=True
                )

                new_role = await ctx.guild.create_role(
                    name=name,
                    permissions=permissions,
                    color=Color.from_hsv(random.random(), 1, 1),
                    reason=f"`{ctx.author}`이/가 역할 생성"
                )

                self.bot.role_manager.add_role_to_db(ctx.guild.id, new_role.id)

                await self.bot.send_embed(
                    ctx,
                    self.bot.colors["ok"],
                    "역할을 생성하였습니다.",
                    f"역할 `{name}`을/를 생성하였습니다."
                )
            except Exception:
                await self.bot.send_embed(
                    ctx,
                    self.bot.colors["error"],
                    "역할을 생성할 수 없습니다.",
                    "역할 생성 중에 오류가 발생하였습니다."
                    "봇 관리자님께 오류 신고를 해주세요."
                )

    @role.command(name="list")
    async def role_list(self, ctx):
        try:
            id_tuples = self.bot.role_manager.get_roles_db(ctx.guild.id)

            roles_str = ",".join(
                "`{}`".format(
                    ctx.guild.get_role(id_tuple[0]).name
                ) for id_tuple in id_tuples
            )

            if not roles_str:
                roles_str = "`없음`"

            await self.bot.send_embed(
                ctx,
                self.bot.colors["ok"],
                "역할 목록",
                roles_str
            )
        except Exception:
            await self.bot.send_embed(
                ctx,
                self.bot.colors["error"],
                "역할 목록을 불러올 수 없습니다.",
                "역할 목록을 불러오는 중에 오류가 발생하였습니다. "
                "봇 관리자님께 오류 신고를 해주세요."
            )

    @role.command(
        name="remove",
        usage="<role>"
    )
    @commands.check_any(
        commands.is_owner(),
        commands.has_permissions(manage_roles=True)
    )
    async def role_remove(self, ctx, name=None):
        if name is None:
            # TODO: 도움말 메시지 추가
            pass
        else:
            role = discord.utils.get(ctx.guild.roles, name=name)

            # 주어진 이름을 가진 역할이 존재하지 않는 경우?
            if not isinstance(role, discord.Role):
                await self.bot.send_embed(
                    ctx,
                    self.bot.colors["error"],
                    "존재하지 않는 역할입니다.",
                    "주어진 이름을 가진 역할이 존재하지 않습니다."
                )
            else:
                try:
                    self.bot.role_manager.remove_role_from_db(
                        ctx.guild.id,
                        role.id
                    )

                    await role.delete(reason="`{ctx.author}`이/가 역할 삭제")

                    await self.bot.send_embed(
                        ctx,
                        self.bot.colors["ok"],
                        "역할을 삭제하였습니다.",
                        f"역할 `{name}`을/를 삭제하였습니다."
                    )
                except Exception:
                    await self.bot.send_embed(
                        ctx,
                        self.bot.colors["error"],
                        "역할을 삭제할 수 없습니다.",
                        "역할 삭제 중에 오류가 발생하였습니다. "
                        "봇 관리자님께 오류 신고를 해주세요."
                    )

    @role.command(
        name="set",
        usage="<role>"
    )
    async def role_set(self, ctx, name=None):
        if name is None:
            # TODO: 도움말 메시지 추가
            pass
        else:
            role = discord.utils.get(ctx.guild.roles, name=name)

            if not isinstance(role, discord.Role):
                await self.bot.send_embed(
                    ctx,
                    self.bot.colors["error"],
                    "존재하지 않는 역할입니다.",
                    "주어진 이름을 가진 역할이 존재하지 않습니다."
                )
            else:
                await ctx.author.add_roles(
                    role,
                    reason="`{ctx.author}`이/가 자신에게 역할 부여"
                )

    @role.command(
        name="unset",
        usage="<role>"
    )
    async def role_unset(self, ctx, name=None):
        if name is None:
            # TODO: 도움말 메시지 추가
            pass
        else:
            role = discord.utils.get(ctx.guild.roles, name=name)

            if not isinstance(role, discord.Role):
                await self.bot.send_embed(
                    ctx,
                    self.bot.colors["error"],
                    "존재하지 않는 역할입니다.",
                    "주어진 이름을 가진 역할이 존재하지 않습니다."
                )
            else:
                await ctx.author.remove_roles(
                    role,
                    reason="`{ctx.author}`이/가 자신의 역할 제거"
                )
