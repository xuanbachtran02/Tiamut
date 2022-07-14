import hikari
import lightbulb
import os
from lib.model import bonfire
from datetime import datetime as dt
from apscheduler.triggers.cron import CronTrigger

"""
Schedule daily task 

Contain functions for daily reminder or updates from APIs

:doc: https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html
"""

daily_plugin = lightbulb.Plugin("Daily")

CHANNEL = int(os.environ["STDOUT_CHANNEL_ID"])


async def msg() -> None:
    await daily_plugin.app.rest.create_message(CHANNEL, "Morning Message\n Here is our today tasks:")


# @daily_plugin.listener(hikari.StartedEvent)
# async def on_started(_: hikari.StartedEvent) -> None:
#     # This event fires once, when the BotApp is fully started.
#     daily_plugin.app.d.sched.add_job(
#         msg, CronTrigger(second=10))


@daily_plugin.command
@lightbulb.option(
    "content", "Reminder content", str, required=True
)
@lightbulb.option(
    "date", "Date of event", str, required=True
)
@lightbulb.command(
    "task", "Add task"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def task(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.user)

    content = ctx.options.content
    date = ctx.options.date

    bonfire.execute("INSERT INTO task VALUES (?, ?, ?)",
                    target.id, content, date)
    bonfire.commit()

    await ctx.respond(f"{target.mention} task is added")


@daily_plugin.command
@lightbulb.command(
    "mytask", "Show member task"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def task(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.user)

    resp = bonfire.records(
        f"SELECT * FROM task WHERE task_memid = {target.id}")

    # [(815706256463364116, 'Wake me up', '3:00 8 July 2022')]

    # embed = (
    #     hikari.Embed(
    #         title=f"Task - {target.display_name}",
    #         description=f"ID: {target.id}",
    #         colour=0x181818,
    #         timestamp=dt.now().astimezone(),
    #     )
    #     .set_footer(
    #         text=f"Requested by {ctx.member.display_name}",
    #         icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
    #     )
    #     .set_thumbnail(target.avatar_url or target.default_avatar_url)
    # )

    # for task in resp:
    #     embed.add_field(
    #         task[2],
    #         f"`{task[1]}`",
    #         inline=False
    #     )

    embed = (
        hikari.Embed(
            title=f"Task - {target.display_name}",
            description=f"ID: {target.id}",
            colour=0x181818,
            timestamp=dt.now().astimezone()
        )
        .add_field(
            "cjoejcoecje",
            "cneocnoeceneoc",
            inline=True
        )
        .add_field(
            "cjoejcoecje",
            "cneocnoeceneoc",
            inline=True
        )
        .add_field(
            "cjoejcoecje",
            "cneocnoeceneoc",
            inline=True
        )
        .add_field(
            "----------------------",
            "----------------------",
            inline=False
        )
        .add_field(
            "cjoejcoecje",
            "cneocnoeceneoc",
            inline=True
        )
        .add_field(
            "cjoejcoecje",
            "cneocnoeceneoc",
            inline=True
        )
        .add_field(
            "cjoejcoecje",
            "cneocnoeceneoc",
            inline=True
        )
    )

    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(daily_plugin)
