import hikari
import lightbulb
from admin.model.__main__ import pipeline
from admin.utils.scrap import playlist
from datetime import datetime

"""
Spotify plugins

"""

spotify_plugin = lightbulb.Plugin("Spotify", "🎵 Spotify utilities")


@spotify_plugin.command
@lightbulb.option(
    "url", "Your Spotify playlist url", str, required=True
)
@lightbulb.command(
    "suggest", "Recommend songs for your playlist"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def suggest(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.target or ctx.user)

    if not target:
        await ctx.respond("That user is not in the server.")
        return

    await ctx.respond(f"Extracting songs from playlist, estimated time: 10s")

    url = ctx.options.url
    suggestion = pipeline(url)
    coverimg, playlistname = playlist(url)

    embed = (
        hikari.Embed(
            title=f"Recommendation - `{playlistname}`",
            description=f"`Suggested tracks` for your playlist",
            colour=0x181818,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
        .set_thumbnail(coverimg)
    )

    artists = list(suggestion['artist_name'])
    tracks = list(suggestion['track_name'])

    for i in range(0, len(tracks), 2):
        embed.add_field(
            artists[i],
            tracks[i],
            inline=True
        ).add_field(
            artists[i+1],
            tracks[i+1],
            inline=True
        )

    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(spotify_plugin)
