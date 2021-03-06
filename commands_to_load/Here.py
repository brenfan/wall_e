# Commands for finding who has access to certain channels.
# Useful since the server size does not allow offline users to be listed
#     in the sidebar

from discord.ext import commands
import discord
import logging
logger = logging.getLogger('wall_e')


class Here():

    def __init__(self, bot):
        self.bot = bot

    def build_embed(members, channel):
        # build response

        title = "Users in **#" + channel.name + "**"

        logger.info("[Here here()] creating an embed with title \"" + title + "\"")
        embed = discord.Embed(type = "rich")
        embed.title = title
        embed.color = discord.Color.blurple()
        embed.set_footer(text="brenfan", icon_url="https://i.imgur.com/vlpCuu2.jpg")
        if len(members) == 0:
            string = "I couldnt find anyone.\n"
        elif len(members) > 50:
            string = "There's a lot of people here.\n"
        else:
            string =  "The following users have permission for this channel.\n"
            nicks = ""
            names = ""
            for member in members:
                nicks += member.display_name + "\n"
                names += str(member) + "\n"

            embed.add_field(name = "Name", value = nicks, inline = True)
            embed.add_field(name = "Account", value = names, inline = True)

        roles = ""
        for role in channel.changed_roles:
            if roles == "":
                roles += "@" + role.name
            else:
                roles += ", @" + role.name
        if roles == "":
            roles = "@everyone"
        roles += "\n*This message will self-destruct in 5 minutes*\n"
        embed.add_field(name = "Channel Roles", value = roles, inline = False)
        embed.description = string
        return embed

    @commands.command()
    async def here(self, ctx, *search):
        logger.info("[Here here()] "
            + str(ctx.message.author) + " called here with {} arguments: {}".format(len(search), ', '.join(search)))

        # find people in the channel
        channel = ctx.channel
        members = channel.members

        # optional filtering
        if len(search) > 0:
            # don't ask
            allowed = [m for m in members
                if len([query for query in search
                if query.lower() in m.display_name.lower() or query.lower() in str(m).lower()])
                > 0]
            members = allowed

        logger.info("[Here here()] found " + str(len(members)) + " users in " + channel.name)

        embed = Here.build_embed(members, channel)

        await ctx.send(embed = embed, delete_after=300)



def setup(bot):
    bot.add_cog(Here(bot))
