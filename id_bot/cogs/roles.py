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

from discord.ext import commands


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
             "`role set`과 `role unset`은 특정 사람에게 역할을 부여하거나, 특정 사람의 "
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

    @role.command(name="add")
    @commands.check_any(
        commands.is_owner(),
        commands.has_permissions(manage_roles=True)
    )
    async def role_add(self, ctx):
        pass

    @role.command(name="list")
    @commands.check_any(
        commands.is_owner(),
        commands.has_permissions(manage_roles=True)
    )
    async def role_list(self, ctx):
        pass

    @role.command(name="remove")
    @commands.check_any(
        commands.is_owner(),
        commands.has_permissions(manage_roles=True)
    )
    async def role_remove(self, ctx):
        pass

    @role.command(name="set")
    @commands.check_any(
        commands.is_owner(),
        commands.has_permissions(manage_roles=True)
    )
    async def role_set(self, ctx):
        pass

    @role.command(name="unset")
    @commands.check_any(
        commands.is_owner(),
        commands.has_permissions(manage_roles=True)
    )
    async def role_unset(self, ctx):
        pass
