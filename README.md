# id-bot

![repo-size badge](https://img.shields.io/github/repo-size/lvt87kr/id-bot)
![license badge](https://img.shields.io/github/license/lvt87kr/id-bot)

```
11:35:07: [id-bot: INFO]:
11:35:07: [id-bot: INFO]:  _|        _|              _|                    _|
11:35:07: [id-bot: INFO]:        _|_|_|              _|_|_|      _|_|    _|_|_|_|
11:35:07: [id-bot: INFO]:  _|  _|    _|  _|_|_|_|_|  _|    _|  _|    _|    _|
11:35:07: [id-bot: INFO]:  _|  _|    _|              _|    _|  _|    _|    _|
11:35:07: [id-bot: INFO]:  _|    _|_|_|              _|_|_|      _|_|        _|_|
11:35:07: [id-bot: INFO]:
11:35:07: [id-bot: INFO]: 현재 버전: v1.0.0
11:35:08: [id-bot: INFO]: 디스코드 서버와 연결되었습니다.
11:35:10: [id-bot: INFO]: 추가 기능 `default`을/를 로드 중입니다...
11:35:10: [id-bot: INFO]: 추가 기능 `roles`을/를 로드 중입니다...
11:35:10: [id-bot: INFO]: ID 봇 가동 준비가 완료되었습니다. (종료하시려면 CTRL+C를 입력해주세요.)
...

11:35:52: [id-bot: INFO]: 디스코드 서버와의 연결이 해제되었습니다.
```

[discord.py](https://github.com/Rapptz/discord.py)를 사용하여 다시 만든 ID 봇.

## 프로젝트 구조

어때요? 참 쉽죠?  

```
id_bot/ -> ID 봇의 프로젝트 폴더.
├── cog/ -> 추가 기능 (명령어) 모듈이 들어있는 폴더.
│   ├── default.py -> 기본적인 명령어 (clear, help, reload 등...)
│   └── roles.py -> 역할 관리 명령어 (role add, role remove, role list 등...)
│
├── __init__.py -> 버전 정보 등의 전역 상수가 정의되어 있는 파일.
├── __main__.py -> ID 봇의 최상위 코드가 실행되는 시작점.
├── bot.py -> ID 봇 클래스가 정의되어 있는 파일.
└── data.py -> 역할 관리에 필요한 데이터베이스를 관리하는 클래스가 정의되어 있는 파일.
```

## 설치 방법

```console
$ git clone https://github.com/lvt87kr/id-bot && cd id-bot
$ mv config_default.json config.json && vim config.json
$ python3 -m pip install -r requirements.txt
$ python3 id_bot
```