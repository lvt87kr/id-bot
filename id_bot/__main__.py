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
import json
import sys

from id_bot.bot import IDBot

if __name__ == "__main__":
    # 로깅 모듈이 출력할 메시지의 최소 레벨을 설정한다.
    logger = logging.getLogger('id-bot')
    logger.setLevel(logging.INFO)

    # 로깅 모듈이 출력할 메시지의 형식을 지정한다.
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s: [%(name)s: %(levelname)s]: %(message)s",
            "%H:%M:%S"
        ),
    )
    logger.addHandler(handler)

    try:
        # config.json 설정 파일을 읽고, 메모리로 불러온다.
        conf_file = open("config.json")
        conf_data = json.load(conf_file)

        debug = conf_data["debug"]
        prefix = conf_data["prefix"]
        token = conf_data["token"]

        # `debug`의 값이 `true`일 경우, 디버깅 모드를 활성화한다.
        if debug.lower() == "true":
            logger = logging.getLogger('discord')
            logger.setLevel(logging.INFO)

            logger.addHandler(handler)

        bot = IDBot(prefix, token)
        bot.run()
    except FileNotFoundError:
        logger.error(
            "config.json 파일이 없습니다. "
            "config_default.json 파일을 복사한 다음, "
            "이름을 config.json으로 변경해주세요."
        )

        sys.exit(1)
    except (json.JSONDecodeError, KeyError):
        logger.error(
            "config.json 파일의 형식이 올바르지 않습니다. "
            "config.json 파일을 다시 생성해주세요."
        )

        sys.exit(1)
