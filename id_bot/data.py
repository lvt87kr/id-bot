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
from os import path
import sqlite3

logger = logging.getLogger('id-bot.data')


class RoleManager:
    """
    서버 역할을 관리하는 클래스.
    """

    def __init__(self):
        """
        `RoleManager` 클래스의 생성자이다.
        """

        # 데이터베이스 파일을 불러온다.
        self.db = sqlite3.connect(path.join("_ID_ROLES.db"))
        self.cur = self.db.cursor()

        self.init_db()

    def init_db(self):
        """
        데이터베이스를 초기화한다.
        """

        try:
            with self.db:
                self.cur.execute(
                    "CREATE TABLE IF NOT EXISTS guild_roles ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "guild_id INTEGER NOT NULL,"
                    "role_id INTEGER NOT NULL)"
                )
        except Exception as error:
            logger.error(
                f"데이터베이스 초기화 중에 오류가 발생했습니다: \"{error}\""
            )

    def get_all_db(self) -> [tuple(int, int, int)]:
        try:
            with self.db:
                self.cur.execute("SELECT * FROM GUILD_ROLES")

                result = self.cur.fetchall()
                print(result)
        except Exception as error:
            logger.error(
                f"데이터베이스 작업 처리 중에 오류가 발생했습니다: \"{error}\""
            )

    def get_roles_db(self, guild_id: int) -> [int]:
        """
        ID가 `guild_id`인 디스코드 서버의 역할을 데이터베이스에서 찾고,
        그 목록을 반환한다.
        """

        result = []

        try:
            with self.db:
                self.cur.execute(
                    "SELECT role_id FROM GUILD_ROLES WHERE guild_id = ?",
                    guild_id
                )

                result = self.cur.fetchall()
                print(result)
        except Exception as error:
            logger.error(
                f"데이터베이스 작업 처리 중에 오류가 발생했습니다: \"{error}\""
            )

        return result

    def add_role_to_db(self, guild_id: int, role_id: int):
        """
        데이터베이스에 새로운 역할을 추가한다.
        """

        try:
            with self.db:
                self.cur.execute(
                    "INSERT INTO GUILD_ROLES (guild_id, role_id)"
                    "VALUES (?, ?)",
                    guild_id,
                    role_id
                )

                # 변경 사항을 저장한다.
                self.db.commit()
        except Exception as error:
            logger.error(
                f"데이터베이스 작업 처리 중에 오류가 발생했습니다: \"{error}\""
            )

    def remove_role_from_db(self, guild_id: int, role_id: int):
        """
        데이터베이스에 존재하는 역할을 제거한다.
        """
        try:
            with self.db:
                self.cur.execute(
                    "DELETE FROM GUILD_ROLES "
                    "WHERE guild_id = ? AND role_id = ?",
                    guild_id,
                    role_id
                )

                # 변경 사항을 저장한다.
                self.db.commit()
        except Exception as error:
            logger.error(
                f"데이터베이스 작업 처리 중에 오류가 발생했습니다: \"{error}\""
            )

