from datetime import datetime

import hikari
import lightbulb
# from lib.model import bonfire

"""
Handle member information

"""

info_plugin = lightbulb.Plugin("Info", "📝 Member information commands")


@info_plugin.command
@lightbulb.option(
    "target", "The member to get information about.", hikari.User, required=False
)
@lightbulb.command(
    "userinfo", "Get info on a server member."
)
@lightbulb.implements(lightbulb.SlashCommand)
async def userinfo(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.target or ctx.user)

    if not target:
        await ctx.respond("That user is not in the server.")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]  # All but @everyone

    embed = (
        hikari.Embed(
            title=f"User Info - {target.display_name}",
            description=f"ID: `{target.id}`",
            colour=0x181818,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
        .set_thumbnail(target.avatar_url or target.default_avatar_url)
        .add_field(
            "Bot?",
            str(target.is_bot),
            inline=True,
        )
        .add_field(
            "Created account on",
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
            inline=True,
        )
        .add_field(
            "Joined server on",
            f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
            inline=True,
        )
        .add_field(
            "Roles",
            ", ".join(r.mention for r in roles),
            inline=False,
        )
    )

    await ctx.respond(embed)


@info_plugin.command
@lightbulb.option(
    "target", "The member to get information about.", hikari.User, required=False
)
@lightbulb.command(
    "insert", "Insert member into database."
)
# @lightbulb.implements(lightbulb.SlashCommand)
# async def userinfo(ctx: lightbulb.Context) -> None:
#     """
#     ID, Name, Roles, Joindate, Isbot
#     """
#     target = ctx.get_guild().get_member(ctx.options.target or ctx.user)
#     members = ctx.get_guild().get_members()
#     print(members.items)
#
#     if not target:
#         await ctx.respond("That user is not in the server.")
#         return
#
#     user_id = target.id
#     name = target.username
#     joined_at = target.joined_at
#     is_bot = str(target.is_bot)
#
#     get_roles = (await target.fetch_roles())[1:]  # All but @everyone
#     roles = ', '.join([role.name for role in get_roles])
#
#     bonfire.execute("INSERT INTO MEMBER VALUES (?, ?, ?, ?, ?)",
#                     user_id, name, roles, joined_at, is_bot)
#     bonfire.commit()
#
#     await ctx.respond(f"Added {target.mention} into bonfire")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)
