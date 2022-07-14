""" Tiamut main functionalities """

__last_modified__ = "14 July 2022"

import logging
import os

import tiamut
import hikari
import lightbulb

from pytz import utc
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from hikari.events.base_events import FailedEventT

log = logging.getLogger(__name__)

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    intents=hikari.Intents.ALL,
    case_insensitive_prefix_commands=True,
    default_enabled_guilds=int(os.environ["GUILD_ID"]),
    help_slash_command=True
)

bot.d.sched = AsyncIOScheduler()
bot.d.sched.configure(timezone=utc)

bot.load_extensions_from("./tiamut/extensions", must_exist=True)


@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.sched.start()
    bot.d.session = ClientSession(trust_env=True)
    log.info("AIOHTTP session started")

    # Database connection...


@bot.listen(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    await bot.rest.create_message(
        int(os.environ["STDOUT_CHANNEL_ID"]),
        f"Tiamut is now online! (Version {tiamut.__version__})",
    )


@bot.listen(hikari.StoppingEvent)
async def on_stopping(_: hikari.StoppingEvent) -> None:
    bot.d.sched.shutdown()
    await bot.d.session.close()
    log.info("AIOHTTP session closed")

    await bot.rest.create_message(
        int(os.environ["STDOUT_CHANNEL_ID"]),
        f"Tiamut is shutting down. (Version {tiamut.__version__})",
    )


@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent[FailedEventT]) -> None:
    raise event.exception


def run() -> None:
    bot.run(
        activity=hikari.Activity(
            name=f"/help • Version {tiamut.__version__}",
            type=hikari.ActivityType.WATCHING,
        )
    )
