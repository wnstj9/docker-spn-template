import asyncio
import ctypes
import datetime
import io
import itertools
import json
import os
import platform
import random
import string
import time

import discord
import pyfiglet
import qrcode
import requests
from colorama import Fore
from discord.ext import commands
from gtts import gTTS

y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX

__version__ = "0.1.1"

start_time = datetime.datetime.now(datetime.timezone.utc)

with open("config/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
    token = config.get("token")
    prefix = config.get("prefix")
    message_generator = itertools.cycle(config["autoreply"]["messages"])


def save_config(config):
    with open("config/config.json", "w") as file:
        json.dump(config, file, indent=4)


def selfbot_menu(bot):
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    print(
        f"""\n{Fore.RESET}
                     
        \n""".replace("█", f"{b}█{y}"),
    )
    print(f"""{y}
{y}------------------------------------------------------------------------------------------------------------------------\n""")
    print(f"""{y}[{b}+{y}]{w} SelfBot Information:\n
\t{y}[{w}#{y}]{w} Version: v{__version__}
\t{y}[{w}#{y}]{w} Logged in as: {bot.user} ({bot.user.id})
\t{y}[{w}#{y}]{w} Cached Users: {len(bot.users)}
\t{y}[{w}#{y}]{w} Guilds Connected: {len(bot.guilds)}\n\n
{y}[{b}+{y}]{w} Settings Overview:\n
\t{y}[{w}#{y}]{w} SelfBot Prefix: {prefix}
\t{y}[{w}#{y}]{w} Remote Users Configured:""")
    if config["remote-users"]:
        for i, user_id in enumerate(config["remote-users"], start=1):
            print(f"\t\t{y}[{w}{i}{y}]{w} User ID: {user_id}")
    else:
        print(f"\t\t{y}[{w}-{y}]{w} No remote users configured.")
    print(f"""
\t{y}[{w}#{y}]{w} Active Autoreply Channels: {len(config["autoreply"]["channels"])}
\t{y}[{w}#{y}]{w} Active Autoreply Users: {len(config["autoreply"]["users"])}\n
\t{y}[{w}#{y}]{w} AFK Status: {"Enabled" if config["afk"]["enabled"] else "Disabled"}
\t{y}[{w}#{y}]{w} AFK Message: "{config["afk"]["message"]}"\n
\t{y}[{w}#{y}]{w} Total Commands Loaded: 41\n\n
{y}[{Fore.GREEN}!{y}]{w} SelfBot is now online and ready!""")


bot = commands.Bot(
    command_prefix=prefix,
    description="not a selfbot",
    self_bot=True,
    help_command=None,
)


@bot.event
async def on_ready():
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"SelfBot v{__version__} - Made By 준서",
        )
        os.system("cls")
    else:
        os.system("clear")
    selfbot_menu(bot)


@bot.event
async def on_message(message):
    if message.author.id in config["copycat"]["users"]:
        if message.content.startswith(config["prefix"]):
            response_message = message.content[len(config["prefix"]) :]
            await message.reply(response_message)
        else:
            await message.reply(message.content)

    if config["afk"]["enabled"]:
        if (bot.user in message.mentions and message.author != bot.user) or (
            isinstance(message.channel, discord.DMChannel)
            and message.author != bot.user
        ):
            await message.reply(config["afk"]["message"])
            return

    if message.author != bot.user:
        if (
            str(message.author.id) in config["autoreply"]["users"]
            or str(message.channel.id) in config["autoreply"]["channels"]
        ):
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return

    if (
        message.guild
        and message.guild.id == 1279905004181917808
        and message.content.startswith(config["prefix"])
    ):
        await message.delete()
        await message.channel.send(
            "> SelfBot commands are not allowed here. Thanks.",
            delete_after=5,
        )
        return

    if (
        message.author != bot.user
        and str(message.author.id) not in config["remote-users"]
    ):
        return

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


@bot.command(aliases=["h"])
async def help(ctx):
    await ctx.message.delete()

    help_text = f"""
**SelfBot | Prefix: `{prefix}`**\n
**명령어:**\n
>>> :wrench: `{prefix}changeprefix <prefix>` - 봇의 접두사를 변경합니다.  
:x: `{prefix}shutdown` - 셀프봇을 종료합니다.  
:notepad_spiral: `{prefix}uptime` - 셀프봇이 실행된 시간을 표시합니다.  
:closed_lock_with_key: `{prefix}remoteuser <@user>` - 특정 사용자가 원격으로 명령을 실행하도록 승인합니다.  
:robot: `{prefix}copycat ON|OFF <@user>` - 지정한 사용자가 말할 때 자동으로 같은 메시지를 답장합니다.  
:pushpin: `{prefix}ping` - 봇의 응답 속도를 확인합니다.  
:pushpin: `{prefix}pingweb <url>` - 웹사이트의 HTTP 상태 코드를 확인합니다 (예: 200이면 온라인).  
:gear: `{prefix}geoip <ip>` - 입력한 IP 주소의 위치를 조회합니다.  
:microphone: `{prefix}tts <text>` - 입력한 텍스트를 음성 파일(.wav)로 변환하여 보냅니다.  
:hash: `{prefix}qr <text>` - 입력한 텍스트를 QR 코드로 생성하여 이미지로 보냅니다.  
:detective: `{prefix}hidemention <display_part> <hidden_part>` - 메시지 안에 다른 메시지를 숨깁니다.  
:wrench: `{prefix}edit <message>` - (수정됨) 태그의 위치를 변경합니다.  
:arrows_counterclockwise: `{prefix}reverse <message>` - 입력한 문장을 거꾸로 변환합니다.  
:notepad_spiral: `{prefix}gentoken` - 올바른 패턴을 가진 가짜 토큰을 생성합니다.  
:woozy_face: `{prefix}hypesquad <house>` - HypeSquad 배지를 변경합니다.  
:dart: `{prefix}nitro` - 가짜 Nitro 코드를 생성합니다.  
:hammer: `{prefix}whremove <webhook_url>` - 웹훅을 삭제합니다.  
:broom: `{prefix}purge <amount>` - 입력한 개수만큼 메시지를 삭제합니다.  
:broom: `{prefix}clear` - 채널의 메시지를 삭제합니다.  
:broom: `{prefix}cleardm <amount>` - 특정 사용자와의 DM을 삭제합니다.  
>>> :writing_hand: `{prefix}spam <amount> <message>` - 입력한 메시지를 지정한 횟수만큼 반복 전송합니다.  
:tools: `{prefix}quickdelete <message>` - 메시지를 전송한 후 2초 뒤에 자동 삭제합니다.  
:tools: `{prefix}autoreply <ON|OFF>` - 자동 응답 기능을 활성화하거나 비활성화합니다.  
:zzz: `{prefix}afk <ON/OFF>` - AFK(자리 비움) 모드를 켜거나 끕니다. DM을 받거나 멘션될 때 자동으로 메시지를 보냅니다.  
:busts_in_silhouette: `{prefix}fetchmembers` - 현재 서버의 모든 멤버 목록을 가져옵니다.  
:scroll: `{prefix}firstmessage` - 현재 채널에서 처음으로 전송된 메시지의 링크를 가져옵니다.  
:mega: `{prefix}dmall <message>` - 서버 내 모든 멤버에게 메시지를 보냅니다.  
:mega: `{prefix}sendall <message>` - 서버 내 모든 채널에 메시지를 보냅니다.  
:busts_in_silhouette: `{prefix}guildicon` - 현재 서버의 아이콘을 가져옵니다.  
:space_invader: `{prefix}usericon <@user>` - 지정한 사용자의 프로필 사진을 가져옵니다.  
:star: `{prefix}guildbanner` - 현재 서버의 배너를 가져옵니다.  
:page_facing_up: `{prefix}tokeninfo <token>` - 입력한 토큰을 이용해 정보를 가져옵니다.  
:pager: `{prefix}guildinfo` - 현재 서버의 정보를 가져옵니다.  
:memo: `{prefix}guildrename <new_name>` - 서버의 이름을 변경합니다.  
:video_game: `{prefix}playing <status>` - 봇의 상태를 "게임 중"으로 설정합니다.  
:x: `{prefix}stopactivity` - 봇의 현재 활동 상태를 초기화합니다.  
:art: `{prefix}ascii <message>` - 입력한 메시지를 ASCII 아트로 변환합니다.  
:x: `{prefix}minesweeper <width> <height>` - 지정한 크기의 지뢰찾기 게임을 시작합니다.  
:robot: `{prefix}leetspeak <message>` - 특정 문자들을 해커 스타일의 문자로 변환합니다.
:woozy_face: `{prefix}copy` - 사용자 메세지 복사 (답장툴)
:woozy_face: `{prefix}servername` - 1~10000 랜덤숫자 채팅방 닉네임 변경 (그룹방) (매크로)
"""

    await ctx.send(help_text)


@bot.command()
async def uptime(ctx):
    await ctx.message.delete()

    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if days:
        time_format = (
            "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
        )
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."

    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

    await ctx.send(uptime_stamp)


@bot.command()
async def ping(ctx):
    await ctx.message.delete()

    before = time.monotonic()
    message_to_send = await ctx.send("Pinging...")

    await message_to_send.edit(
        content=f"`{int((time.monotonic() - before) * 1000)} ms`",
    )


@bot.command()
async def geoip(ctx, ip: str = None):
    await ctx.message.delete()

    if not ip:
        await ctx.send(
            "> **[ERROR]**: Invalid command.\n> __Command__: `geoip <ip>`",
            delete_after=5,
        )
        return

    try:
        r = requests.get(f"http://ip-api.com/json/{ip}")
        geo = r.json()
        embed = f"""**GEOLOCATE IP | Prefix: `{prefix}`**\n
        > :pushpin: `IP`\n*{geo["query"]}*
        > :globe_with_meridians: `Country-Region`\n*{geo["country"]} - {geo["regionName"]}*
        > :department_store: `City`\n*{geo["city"]} ({geo["zip"]})*
        > :map: `Latitute-Longitude`\n*{geo["lat"]} - {geo["lon"]}*
        > :satellite: `ISP`\n*{geo["isp"]}*
        > :robot: `Org`\n*{geo["org"]}*
        > :alarm_clock: `Timezone`\n*{geo["timezone"]}*
        > :electric_plug: `As`\n*{geo["as"]}*"""
        await ctx.send(embed, file=discord.File("img/astraa.gif"))
    except Exception as e:
        await ctx.send(
            f"> **[**ERROR**]**: Unable to geolocate ip\n> __Error__: `{e!s}`",
            delete_after=5,
        )


@bot.command()
async def tts(ctx, *, content: str = None):
    await ctx.message.delete()

    if not content:
        await ctx.send(
            "> **[ERROR]**: Invalid command.\n> __Command__: `tts <message>`",
            delete_after=5,
        )
        return

    content = content.strip()

    tts = gTTS(text=content, lang="en")

    f = io.BytesIO()
    tts.write_to_fp(f)
    f.seek(0)

    await ctx.send(file=discord.File(f, f"{content[:10]}.wav"))


@bot.command(aliases=["qrcode"])
async def qr(ctx, *, text: str = "https://discord.gg/PKR7nM9j9U"):
    qr = qrcode.make(text)

    img_byte_arr = io.BytesIO()
    qr.save(img_byte_arr)
    img_byte_arr.seek(0)

    await ctx.send(file=discord.File(img_byte_arr, "qr_code.png"))


@bot.command()
async def pingweb(ctx, website_url: str = None):
    await ctx.message.delete()

    if not website_url:
        await ctx.send(
            "> **[ERROR]**: Invalid command.\n> __Command__: `pingweb <url>`",
            delete_after=5,
        )
        return

    try:
        r = requests.get(website_url).status_code
        if r == 404:
            await ctx.send(f"> Website **down** *({r})*")
        else:
            await ctx.send(f"> Website **operational** *({r})*")
    except Exception as e:
        await ctx.send(
            f"> **[**ERROR**]**: Unable to ping website\n> __Error__: `{e!s}`",
            delete_after=5,
        )


@bot.command()
async def gentoken(ctx, user: str = None):
    await ctx.message.delete()

    code = (
        "ODA"
        + random.choice(string.ascii_letters)
        + "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(20)
        )
        + "."
        + random.choice(string.ascii_letters).upper()
        + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        + "."
        + "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(27)
        )
    )

    if not user:
        await ctx.send("".join(code))
    else:
        await ctx.send(f"> {user}'s token is: ||{''.join(code)}||")


@bot.command()
async def quickdelete(ctx, *, message: str = None):
    await ctx.message.delete()

    if not message:
        await ctx.send(
            "> **[**ERROR**]**: Invalid input\n> __Command__: `quickdelete <message>`",
            delete_after=2,
        )
        return

    await ctx.send(message, delete_after=2)


@bot.command(aliases=["uicon"])
async def usericon(ctx, user: discord.User = None):
    await ctx.message.delete()

    if not user:
        await ctx.send(
            "> **[**ERROR**]**: Invalid input\n> __Command__: `usericon <@user>`",
            delete_after=5,
        )
        return

    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    await ctx.send(f"> {user.mention}'s avatar:\n{avatar_url}")


@bot.command(aliases=["tinfo"])
async def tokeninfo(ctx, usertoken: str = None):
    await ctx.message.delete()

    if not usertoken:
        await ctx.send(
            "> **[**ERROR**]**: Invalid input\n> __Command__: `tokeninfo <token>`",
            delete_after=5,
        )
        return

    headers = {"Authorization": usertoken, "Content-Type": "application/json"}
    languages = {
        "da": "Danish, Denmark",
        "de": "German, Germany",
        "en-GB": "English, United Kingdom",
        "en-US": "English, United States",
        "es-ES": "Spanish, Spain",
        "fr": "French, France",
        "hr": "Croatian, Croatia",
        "lt": "Lithuanian, Lithuania",
        "hu": "Hungarian, Hungary",
        "nl": "Dutch, Netherlands",
        "no": "Norwegian, Norway",
        "pl": "Polish, Poland",
        "pt-BR": "Portuguese, Brazilian, Brazil",
        "ro": "Romanian, Romania",
        "fi": "Finnish, Finland",
        "sv-SE": "Swedish, Sweden",
        "vi": "Vietnamese, Vietnam",
        "tr": "Turkish, Turkey",
        "cs": "Czech, Czechia, Czech Republic",
        "el": "Greek, Greece",
        "bg": "Bulgarian, Bulgaria",
        "ru": "Russian, Russia",
        "uk": "Ukrainian, Ukraine",
        "th": "Thai, Thailand",
        "zh-CN": "Chinese, China",
        "ja": "Japanese",
        "zh-TW": "Chinese, Taiwan",
        "ko": "Korean, Korea",
    }

    try:
        res = requests.get("https://discordapp.com/api/v6/users/@me", headers=headers)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(
            f"> **[**ERROR**]**: An error occurred while sending request\n> __Error__: `{e!s}`",
            delete_after=5,
        )
        return

    if res.status_code == 200:
        res_json = res.json()
        user_name = f"{res_json['username']}#{res_json['discriminator']}"
        user_id = res_json["id"]
        avatar_id = res_json["avatar"]
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif"
        phone_number = res_json["phone"]
        email = res_json["email"]
        mfa_enabled = res_json["mfa_enabled"]
        flags = res_json["flags"]
        locale = res_json["locale"]
        verified = res_json["verified"]
        days_left = ""
        language = languages.get(locale)
        creation_date = datetime.datetime.fromtimestamp(
            ((int(user_id) >> 22) + 1420070400000) / 1000,
        ).strftime("%d-%m-%Y %H:%M:%S UTC")
        has_nitro = False

        try:
            nitro_res = requests.get(
                "https://discordapp.com/api/v6/users/@me/billing/subscriptions",
                headers=headers,
            )
            nitro_res.raise_for_status()
            nitro_data = nitro_res.json()
            has_nitro = bool(len(nitro_data) > 0)
            if has_nitro:
                d1 = datetime.datetime.strptime(
                    nitro_data[0]["current_period_end"].split(".")[0],
                    "%Y-%m-%dT%H:%M:%S",
                )
                d2 = datetime.datetime.strptime(
                    nitro_data[0]["current_period_start"].split(".")[0],
                    "%Y-%m-%dT%H:%M:%S",
                )
                days_left = abs((d2 - d1).days)
        except requests.exceptions.RequestException:
            pass

        try:
            embed = f"""**TOKEN INFORMATIONS | Prefix: `{prefix}`**\n
        > :dividers: __Basic Information__\n\tUsername: `{user_name}`\n\tUser ID: `{user_id}`\n\tCreation Date: `{creation_date}`\n\tAvatar URL: `{avatar_url if avatar_id else "None"}`
        > :crystal_ball: __Nitro Information__\n\tNitro Status: `{has_nitro}`\n\tExpires in: `{days_left if days_left else "None"} day(s)`
        > :incoming_envelope: __Contact Information__\n\tPhone Number: `{phone_number if phone_number else "None"}`\n\tEmail: `{email if email else "None"}`
        > :shield: __Account Security__\n\t2FA/MFA Enabled: `{mfa_enabled}`\n\tFlags: `{flags}`
        > :paperclip: __Other__\n\tLocale: `{locale} ({language})`\n\tEmail Verified: `{verified}`"""

        except Exception as e:
            await ctx.send(
                f"> **[**ERROR**]**: Unable to recover token infos\n> __Error__: `{e!s}`",
                delete_after=5,
            )
    else:
        await ctx.send(
            "> **[**ERROR**]**: Unable to recover token infos\n> __Error__: Invalid token",
            delete_after=5,
        )


@bot.command()
async def cleardm(ctx, amount: str = "1"):
    await ctx.message.delete()

    if not amount.isdigit():
        await ctx.send(
            f"> **[**ERROR**]**: Invalid amount specified. It must be a number.\n> __Command__: `{config['prefix']}cleardm <amount>`",
            delete_after=5,
        )
        return

    amount = int(amount)

    if amount <= 0 or amount > 100:
        await ctx.send(
            "> **[**ERROR**]**: Amount must be between 1 and 100.",
            delete_after=5,
        )
        return

    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(
            "> **[**ERROR**]**: This command can only be used in DMs.",
            delete_after=5,
        )
        return

    deleted_count = 0
    async for message in ctx.channel.history(limit=amount):
        if message.author == bot.user:
            try:
                await message.delete()
                deleted_count += 1
            except discord.Forbidden:
                await ctx.send(
                    "> **[**ERROR**]**: Missing permissions to delete messages.",
                    delete_after=5,
                )
                return
            except discord.HTTPException as e:
                await ctx.send(
                    f"> **[**ERROR**]**: An error occurred while deleting messages: {e!s}",
                    delete_after=5,
                )
                return

    await ctx.send(f"> **Cleared {deleted_count} messages in DMs.**", delete_after=5)


@bot.command(aliases=["hs"])
async def hypesquad(ctx, house: str = None):
    await ctx.message.delete()

    if not house:
        await ctx.send(
            "> **[**ERROR**]**: Invalid input\n> __Command__: `hypesquad <house>`",
            delete_after=5,
        )
        return

    headers = {"Authorization": token, "Content-Type": "application/json"}

    try:
        r = requests.get("https://discord.com/api/v8/users/@me", headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(
            f"> **[**ERROR**]**: Invalid status code\n> __Error__: `{e!s}`",
            delete_after=5,
        )
        return

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36",
    }
    payload = {}
    if house == "bravery":
        payload = {"house_id": 1}
    elif house == "brilliance":
        payload = {"house_id": 2}
    elif house == "balance":
        payload = {"house_id": 3}
    else:
        await ctx.send(
            "> **[**ERROR**]**: Invalid input\n> __Error__: Hypesquad house must be one of the following: `bravery`, `brilliance`, `balance`",
            delete_after=5,
        )
        return

    try:
        r = requests.post(
            "https://discordapp.com/api/v6/hypesquad/online",
            headers=headers,
            json=payload,
            timeout=10,
        )
        r.raise_for_status()

        if r.status_code == 204:
            await ctx.send(f"> Hypesquad House changed to `{house}`!")

    except requests.exceptions.RequestException as e:
        await ctx.send(
            f"> **[**ERROR**]**: Unable to change Hypesquad house\n> __Error__: `{e!s}`",
            delete_after=5,
        )


@bot.command(aliases=["ginfo"])
async def guildinfo(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(
            "> **[**ERROR**]**: This command can only be used in a server",
            delete_after=5,
        )
        return

    date_format = "%a, %d %b %Y %I:%M %p"
    embed = f"""> **GUILD INFORMATIONS | Prefix: `{prefix}`**
:dividers: __Basic Information__
Server Name: `{ctx.guild.name}`\nServer ID: `{ctx.guild.id}`\nCreation Date: `{ctx.guild.created_at.strftime(date_format)}`\nServer Icon: `{ctx.guild.icon.url if ctx.guild.icon.url else "None"}`\nServer Owner: `{ctx.guild.owner}`
:page_facing_up: __Other Information__
`{len(ctx.guild.members)}` Members\n`{len(ctx.guild.roles)}` Roles\n`{len(ctx.guild.text_channels) if ctx.guild.text_channels else "None"}` Text-Channels\n`{len(ctx.guild.voice_channels) if ctx.guild.voice_channels else "None"}` Voice-Channels\n`{len(ctx.guild.categories) if ctx.guild.categories else "None"}` Categories"""

    await ctx.send(embed)


@bot.command()
async def nitro(ctx):
    await ctx.message.delete()

    await ctx.send(
        f"https://discord.gift/{''.join(random.choices(string.ascii_letters + string.digits, k=16))}",
    )


@bot.command()
async def whremove(ctx, webhook: str = None):
    await ctx.message.delete()

    if not webhook:
        await ctx.send(
            f"> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}whremove <webhook>`",
            delete_after=5,
        )
        return

    try:
        requests.delete(webhook.rstrip())
    except Exception as e:
        await ctx.send(
            f"> **[**ERROR**]**: Unable to delete webhook\n> __Error__: `{e!s}`",
            delete_after=5,
        )
        return

    await ctx.send("> Webhook has been deleted!")


@bot.command(aliases=["hide"])
async def hidemention(ctx, *, content: str = None):
    await ctx.message.delete()

    if not content:
        await ctx.send(
            f"> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}hidemention <message>`",
            delete_after=5,
        )
        return

    await ctx.send(content + ("||\u200b||" * 200) + "@everyone")


@bot.command()
async def edit(ctx, *, content: str = None):
    await ctx.message.delete()

    if not content:
        await ctx.send(
            f"> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}edit <message>`",
            delete_after=5,
        )
        return

    text = await ctx.send(content)

    await text.edit(content=f"\u202b{content}")


@bot.command(aliases=["911"])
async def airplane(ctx):
    await ctx.message.delete()

    frames = [
        """:man_wearing_turban::airplane:\t\t\t\t:office:""",
        """:man_wearing_turban:\t:airplane:\t\t\t:office:""",
        """:man_wearing_turban:\t\t::airplane:\t\t:office:""",
        """:man_wearing_turban:\t\t\t:airplane:\t:office:""",
        """:man_wearing_turban:\t\t\t\t:airplane::office:""",
        """:boom::boom::boom:""",
    ]

    sent_message = await ctx.send(frames[0])

    for frame in frames[1:]:
        await asyncio.sleep(0.5)
        await sent_message.edit(content=frame)


@bot.command(aliases=["mine"])
async def minesweeper(ctx, size: int = 5):
    await ctx.message.delete()

    size = max(min(size, 8), 2)
    bombs = [
        [random.randint(0, size - 1), random.randint(0, size - 1)]
        for _ in range(size - 1)
    ]
    is_on_board = lambda x, y: 0 <= x < size and 0 <= y < size
    has_bomb = lambda x, y: [i for i in bombs if i[0] == x and i[1] == y]
    m_numbers = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
    m_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    message_to_send = "**Click to play**:\n"

    for y in range(size):
        for x in range(size):
            tile = f"||{chr(11036)}||"
            if has_bomb(x, y):
                tile = f"||{chr(128163)}||"
            else:
                count = 0
                for xmod, ymod in m_offsets:
                    if is_on_board(x + xmod, y + ymod) and has_bomb(x + xmod, y + ymod):
                        count += 1
                if count != 0:
                    tile = f"||{m_numbers[count - 1]}||"
            message_to_send += tile
        message_to_send += "\n"

    await ctx.send(message_to_send)


@bot.command(aliases=["leet"])
async def leetspeak(ctx, *, content: str):
    await ctx.message.delete()

    if not content:
        await ctx.send(
            "> **[ERROR]**: Invalid command.\n> __Command__: `leetspeak <message>`",
            delete_after=5,
        )
        return

    content = (
        content.replace("a", "4")
        .replace("A", "4")
        .replace("e", "3")
        .replace("E", "3")
        .replace("i", "1")
        .replace("I", "1")
        .replace("o", "0")
        .replace("O", "0")
        .replace("t", "7")
        .replace("T", "7")
        .replace("b", "8")
        .replace("B", "8")
    )
    await ctx.send(content)


@bot.command()
async def dick(ctx, user: str = None):
    await ctx.message.delete()

    if not user:
        user = ctx.author.display_name

    size = random.randint(1, 15)
    dong = "=" * size

    await ctx.send(f"> **{user}**'s Dick size\n8{dong}D")


@bot.command()
async def reverse(ctx, *, content: str = None):
    await ctx.message.delete()

    if not content:
        await ctx.send(
            "> **[ERROR]**: Invalid command.\n> __Command__: `reverse <message>`",
            delete_after=5,
        )
        return

    content = content[::-1]
    await ctx.send(content)


@bot.command(aliases=["fetch"])
async def fetchmembers(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(
            "> **[**ERROR**]**: This command can only be used in a server.",
            delete_after=5,
        )
        return

    members = ctx.guild.members
    member_data = []

    for member in members:
        member_info = {
            "name": member.name,
            "id": str(member.id),
            "avatar_url": str(member.avatar.url)
            if member.avatar
            else str(member.default_avatar.url),
            "discriminator": member.discriminator,
            "status": str(member.status),
            "joined_at": str(member.joined_at),
        }
        member_data.append(member_info)

    with open("members_list.json", "w", encoding="utf-8") as f:
        json.dump(member_data, f, indent=4)

    await ctx.send("> List of members:", file=discord.File("members_list.json"))

    os.remove("members_list.json")


@bot.command()
async def spam(
    ctx,
    amount: int = 1,
    *,
    message_to_send: str = "https://discord.gg/PKR7nM9j9U",
):
    await ctx.message.delete()

    try:
        if amount <= 0 or amount > 9:
            await ctx.send(
                "> **[**ERROR**]**: Amount must be between 1 and 9",
                delete_after=5,
            )
            return
        for _ in range(amount):
            await ctx.send(message_to_send)
    except ValueError:
        await ctx.send(
            "> **[**ERROR**]**: Invalid input\n> __Command__: `spam <amount> <message>`",
            delete_after=5,
        )


@bot.command(aliases=["gicon"])
async def guildicon(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(
            "> **[**ERROR**]**: This command can only be used in a server",
            delete_after=5,
        )
        return

    await ctx.send(
        f"> **{ctx.guild.name} icon :**\n{ctx.guild.icon.url if ctx.guild.icon else '*NO ICON*'}",
    )


@bot.command(aliases=["gbanner"])
async def guildbanner(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(
            "> **[**ERROR**]**: This command can only be used in a server",
            delete_after=5,
        )
        return

    await ctx.send(
        f"> **{ctx.guild.name} banner :**\n{ctx.guild.banner.url if ctx.guild.banner else '*NO BANNER*'}",
    )


@bot.command(aliases=["grename"])
async def guildrename(ctx, *, name: str = None):
    await ctx.message.delete()

    if not name:
        await ctx.send(
            "> **[ERROR]**: Invalid command.\n> __Command__: `guildrename <name>`",
            delete_after=5,
        )
        return

    if not ctx.guild:
        await ctx.send(
            "> **[**ERROR**]**: This command can only be used in a server",
            delete_after=5,
        )
        return

    if not ctx.guild.me.guild_permissions.manage_guild:
        await ctx.send("> **[**ERROR**]**: Missing permissions", delete_after=5)
        return

    try:
        await ctx.guild.edit(name=name)
        await ctx.send(f"> Server renamed to '{name}'")
    except Exception as e:
        await ctx.send(
            f"> **[**ERROR**]**: Unable to rename the server\n> __Error__: `{e!s}`, delete_after=5",
        )


@bot.command()
async def purge(ctx, num_messages: int = 1):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(
            "> **[**ERROR**]**: This command can only be used in a server",
            delete_after=5,
        )
        return

    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send(
            "> **[**ERROR**]**: You do not have permission to delete messages",
            delete_after=5,
        )
        return

    if 1 <= num_messages <= 100:
        deleted_messages = await ctx.channel.purge(limit=num_messages)
        await ctx.send(
            f"> **{len(deleted_messages)}** messages have been deleted",
            delete_after=5,
        )
    else:
        await ctx.send(
            "> **[**ERROR**]**: The number must be between 1 and 100",
            delete_after=5,
        )


@bot.command(aliases=["autor"])
async def autoreply(ctx, command: str, user: discord.User = None):
    await ctx.message.delete()

    if command not in ["ON", "OFF"]:
        await ctx.send(
            "> **[**ERROR**]**: Invalid input. Use `ON` or `OFF`.\n> __Command__: `autoreply ON|OFF [@user]`",
            delete_after=5,
        )
        return

    if command.upper() == "ON":
        if user:
            if str(user.id) not in config["autoreply"]["users"]:
                config["autoreply"]["users"].append(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(
                f"> **Autoreply enabled for user {user.mention}.**",
                delete_after=5,
            )
        else:
            if str(ctx.channel.id) not in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].append(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(
                "> **Autoreply has been enabled in this channel**",
                delete_after=5,
            )
    elif command.upper() == "OFF":
        if user:
            if str(user.id) in config["autoreply"]["users"]:
                config["autoreply"]["users"].remove(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(
                f"> **Autoreply disabled for user {user.mention}**",
                delete_after=5,
            )
        else:
            if str(ctx.channel.id) in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].remove(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(
                "> **Autoreply has been disabled in this channel**",
                delete_after=5,
            )


@bot.command(aliases=["remote"])
async def remoteuser(ctx, action: str, users: discord.User = None):
    await ctx.message.delete()

    if not users:
        await ctx.send(
            "> **[ERROR]**: Invalid command.\n> __Command__: `remoteuser ADD|REMOVE <@user(s)>`",
            delete_after=5,
        )
        return

    if action not in ["ADD", "REMOVE"]:
        await ctx.send(
            "> **[**ERROR**]**: Invalid action. Use `ADD` or `REMOVE`.\n> __Command__: `remoteuser ADD|REMOVE <@user(s)>`",
            delete_after=5,
        )
        return

    if action.upper() == "ADD":
        for user in users:
            if str(user.id) not in config["remote-users"]:
                config["remote-users"].append(str(user.id))

        save_config(config)
        selfbot_menu(bot)

        await ctx.send(
            f"> **Success**: {len(users)} user(s) added to remote-users",
            delete_after=5,
        )
    elif action.upper() == "REMOVE":
        for user in users:
            if str(user.id) in config["remote-users"]:
                config["remote-users"].remove(str(user.id))

        save_config(config)
        selfbot_menu(bot)

        await ctx.send(
            f"> **Success**: {len(users)} user(s) removed from remote-users",
            delete_after=5,
        )


@bot.command()
async def afk(ctx, status: str, *, message: str = None):
    await ctx.message.delete()

    if status not in ["ON", "OFF"]:
        await ctx.send(
            "> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `afk ON|OFF <message>`",
            delete_after=5,
        )
        return

    if status.upper() == "ON":
        if not config["afk"]["enabled"]:
            config["afk"]["enabled"] = True
            if message:
                config["afk"]["message"] = message
            save_config(config)
            selfbot_menu(bot)
            await ctx.send(
                f"> **AFK mode enabled.** Message: `{config['afk']['message']}`",
                delete_after=5,
            )
        else:
            await ctx.send(
                "> **[**ERROR**]**: AFK mode is already enabled",
                delete_after=5,
            )
    elif status.upper() == "OFF":
        if config["afk"]["enabled"]:
            config["afk"]["enabled"] = False
            save_config(config)
            selfbot_menu(bot)
            await ctx.send("> **AFK mode disabled.** Welcome back!", delete_after=5)
        else:
            await ctx.send(
                "> **[**ERROR**]**: AFK mode is not currently enabled",
                delete_after=5,
            )


@bot.command(aliases=["prefix"])
async def changeprefix(ctx, *, new_prefix: str = None):
    await ctx.message.delete()

    if not new_prefix:
        await ctx.send(
            "> **[**ERROR**]**: Invalid command.\n> __Command__: `changeprefix <prefix>`",
            delete_after=5,
        )
        return

    config["prefix"] = new_prefix
    save_config(config)
    selfbot_menu(bot)

    bot.command_prefix = new_prefix

    await ctx.send(f"> Prefix updated to `{new_prefix}`", delete_after=5)


@bot.command(aliases=["logout"])
async def shutdown(ctx):
    await ctx.message.delete()

    msg = await ctx.send("> Shutting down...")
    await asyncio.sleep(2)

    await msg.delete()
    await bot.close()


@bot.command()
async def clear(ctx):
    await ctx.message.delete()

    await ctx.send("ﾠﾠ" + "\n" * 200 + "ﾠﾠ")


@bot.command()
async def sendall(ctx, *, message="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(
            "> **[**ERROR**]**: This command can only be used in a server",
            delete_after=5,
        )
        return

    channels = ctx.guild.text_channels
    success_count = 0
    failure_count = 0

    try:
        for channel in channels:
            try:
                await channel.send(message)
                success_count += 1
            except Exception:
                failure_count += 1
        await ctx.send(
            f"> {success_count} message(s) sent successfully, {failure_count} failed to send",
            delete_after=5,
        )
    except Exception as e:
        await ctx.send(f"> **[**ERROR**]**: An error occurred: `{e}`", delete_after=5)


@bot.command(aliases=["copycatuser", "copyuser"])
async def copycat(ctx, action: str = None, user: discord.User = None):
    await ctx.message.delete()

    if action not in ["ON", "OFF"]:
        await ctx.send(
            "> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `copycat ON|OFF <@user>`",
            delete_after=5,
        )
        return

    if not user:
        await ctx.send(
            "> **[**ERROR**]**: Please specify a user to copy.\n> __Command__: `copycat ON|OFF <@user>`",
            delete_after=5,
        )
        return

    if action == "ON":
        if user.id not in config["copycat"]["users"]:
            config["copycat"]["users"].append(user.id)
            save_config(config)
            await ctx.send(f"> Now copying `{user!s}`", delete_after=5)
        else:
            await ctx.send(f"> `{user!s}` is already being copied.", delete_after=5)

    elif action == "OFF":
        if user.id in config["copycat"]["users"]:
            config["copycat"]["users"].remove(user.id)
            save_config(config)
            await ctx.send(f"> Stopped copying `{user!s}`", delete_after=5)
        else:
            await ctx.send(f"> `{user!s}` was not being copied.", delete_after=5)


@bot.command()
async def firstmessage(ctx):
    await ctx.message.delete()

    try:
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            link = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id}"
            await ctx.send(
                f"> Here is the link to the first message: {link}",
                delete_after=5,
            )
            break
        else:
            await ctx.send(
                "> **[ERROR]**: No messages found in this channel.",
                delete_after=5,
            )

    except Exception as e:
        await ctx.send(
            f"> **[ERROR]**: An error occurred while fetching the first message. `{e}`",
            delete_after=5,
        )


@bot.command()
async def ascii(ctx, *, message=None):
    await ctx.message.delete()

    if not message:
        await ctx.send(
            "> **[**ERROR**]**: Invalid command.\n> __Command__: `ascii <message>`",
            delete_after=5,
        )
        return

    try:
        ascii_art = pyfiglet.figlet_format(message)
        await ctx.send(f"```\n{ascii_art}\n```", delete_after=5)
    except Exception as e:
        await ctx.send(
            f"> **[ERROR]**: An error occurred while generating the ASCII art. `{e}`",
            delete_after=5,
        )


@bot.command()
async def playing(ctx, *, status: str = None):
    await ctx.message.delete()

    if not status:
        await ctx.send(
            "> **[**ERROR**]**: Invalid command.\n> __Command__: `playing <status>`",
            delete_after=5,
        )
        return

    await bot.change_presence(activity=discord.Game(name=status))
    await ctx.send(f"> Successfully set the game status to `{status}`", delete_after=5)


@bot.command()
async def streaming(ctx, *, status: str = None):
    await ctx.message.delete()

    if not status:
        await ctx.send(
            "> **[**ERROR**]**: Invalid command.\n> __Command__: `streaming <status>`",
            delete_after=5,
        )
        return

    await bot.change_presence(
        activity=discord.Streaming(name=status, url=f"https://www.twitch.tv/{status}"),
    )
    await ctx.send(
        f"> Successfully set the streaming status to `{status}`",
        delete_after=5,
    )


@bot.command(
    aliases=[
        "stopstreaming",
        "stopstatus",
        "stoplistening",
        "stopplaying",
        "stopwatching",
    ],
)
async def stopactivity(ctx):
    await ctx.message.delete()

    await bot.change_presence(activity=None, status=discord.Status.dnd)


@bot.command()
async def dmall(ctx, *, message: str = "https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(
            "> **[**ERROR**]**: This command can only be used in a server",
            delete_after=5,
        )
        return

    members = [m for m in ctx.guild.members if not m.bot]
    total_members = len(members)
    estimated_time = round(total_members * 4.5)

    await ctx.send(
        f">Starting DM process for `{total_members}` members.\n> Estimated time: `{estimated_time} seconds` (~{round(estimated_time / 60, 2)} minutes)",
        delete_after=10,
    )

    success_count = 0
    fail_count = 0

    for member in members:
        try:
            await member.send(message)
            success_count += 1
        except Exception:
            fail_count += 1

        await asyncio.sleep(random.uniform(3, 6))

    await ctx.send(
        f"> **[**INFO**]**: DM process completed.\n> Successfully sent: `{success_count}`\n> Failed: `{fail_count}`",
        delete_after=10,
    )


copy_users = {}


@bot.command()
async def copy(ctx, mode=None, member: discord.Member = None):
    await ctx.message.delete()  # 명령어 메시지 삭제

    if mode not in ["ON", "OFF"] or member is None:
        await ctx.send("사용법: `.copy ON|OFF @user`")
        return

    if mode == "ON":
        copy_users[member.id] = True
        await ctx.send(f"{member.display_name} 유저의 메시지를 복사하도록 설정했어요.")
    else:
        copy_users.pop(member.id, None)
        await ctx.send(f"{member.display_name} 유저 복사를 중지했어요.")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.id in copy_users and not message.author.bot:
        await message.channel.send(message.content)


import discord
from discord.ext import commands


@bot.command()
async def servername(ctx):
    await ctx.message.delete()

    # DM 그룹 채팅방에서만 작동
    if ctx.channel.type != discord.ChannelType.group:
        await ctx.send("❌ 이 명령어는 DM 그룹 채팅방에서만 사용할 수 있어요.")
        return

    await ctx.send("✅ 이름 변경을 시작합니다! (중단하려면 수동으로 멈춰야 해요)")

    while True:
        try:
            number = random.randint(1, 10000)
            new_name = f"쉬지마라 - {number}"
            await ctx.channel.edit(name=new_name)
            await asyncio.sleep(1)  # 1초 대기
        except Exception as e:
            await ctx.send(f"⚠️ 오류 발생: {e}")
            break

if __name__ == "__main__":
 bot.run(token)