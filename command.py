@bot.command()
async def subscribe(ctx: commands.Context):
    message = "Open the page below to pick your plan and subscribe!\nhttps://mee6.gg/m/thedream"
    await ctx.send(content=message, ephemeral=True)


