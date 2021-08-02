import discord, wikipedia
from discord_components import DiscordComponents, Button
from discord.ext import commands

bot = commands.Bot(command_prefix = "w!")
DiscordComponents(bot)

@bot.event
async def on_ready():
    print("Wikipedia Search Ready.")

@bot.command(
    name = "wikipedia",
    aliases = ["wiki"]
)
async def wiki(ctx, *, term = None):
    emojis = ["1", "2", "3", "4", "5"]
    if term == None:
        return await ctx.reply(
            "No search term provided! Please enter a search term this time around.",
            mention_author = False
        )
    results = wikipedia.search(term, results = 6)
    results.remove(results[0])

    embed_homepage = discord.Embed(
        colour = discord.Colour.blurple(),
        title = "Wikipedia Search",
        description = f"You searched for *{term}*"
    )
    send_components = []
    for i in range(len(results)):
        embed_homepage.add_field(
            name = results[i],
            value = f"Click the button **{emojis[i]}** to learn more",
            inline = False
        )
        send_components.append(
            Button(
                label = emojis[i],
                style = 1
            )
        )

    send_homepage = await ctx.reply(
        embed = embed_homepage,
        components = [send_components],
        mention_author = False
    )

    interaction = await bot.wait_for("button_click", check = lambda res: res.user.id == ctx.author.id and res.message.id == send_homepage.id)
    await interaction.respond(type = 6)

    index = int(interaction.component.label) - 1

    page = wikipedia.page(results[index])
    summary = wikipedia.summary(results[index], sentences = 5)
    sum_embed = discord.Embed(
        colour = discord.Colour.blurple(),
        title = f"{page.title}",
        description = f"{summary}"
    )

    await ctx.send(
        embed = sum_embed
    )

bot.run("ODIxNTgwODc1Nzc0MTY1MDMy.YFFy0Q.UCVR7FUtKt9YbR6qPHQm0tJswvQ")
