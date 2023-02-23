@bot.command()
async def info(ctx: commands.Context):
    message = "test_command"
    await ctx.send(content=message, ephemeral=True)


