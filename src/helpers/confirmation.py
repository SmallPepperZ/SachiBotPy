
import discord

async def confirm(self:discord.ext.commands.Cog, ctx:discord.ext.commands.Context, msg:discord.Message, *, timeout:int=20, silent:bool=False) -> "bool|None":
    """Waits for confirmation via reaction from the user before continuing

    Parameters
    ----------
    self : discord.ext.commands.Cog
        Cog the command is invoked in

    ctx : discord.ext.commands.Context
        Command invocation context

    msg : discord.Message
        The message to prompt for confirmation on

    timeout = timeout : int, optional
        How long to wait before timing out (seconds), by default 20

    silent = silent : bool, optional
        Whether to avoid sending ephemeral feedback to the user

    Returns
    -------
    output : bool or None
        True if user confirms action, False if user does not confirm action, None if confirmation times out
    """
    view = Confirm(invoker=ctx.author, silent=silent, timeout=timeout)
    await msg.edit(view=view)
    # Wait for the View to stop listening for input...
    await view.wait()
    return view.value

class Confirm(discord.ui.View):
    def __init__(self, invoker:"discord.User|discord.Member",silent:bool=False, *, timeout:float=None):
        if timeout is not None:
            super().__init__(timeout=timeout)
        else:
            super().__init__()
        self.value = None
        self.invoker = invoker
        self.silent = silent

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.confirmation(interaction, True)

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.gray)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.confirmation(interaction, False)

    async def confirmation(self, interaction:discord.Interaction, confirm:bool):
        if not interaction.user.id == self.invoker.id:
            await interaction.response.send_message('You do not have permissions to do this', ephemeral=True)
            return
        if confirm and not self.silent:
            await interaction.response.send_message('Confirming', ephemeral=True)
        elif not confirm and not self.silent:
            await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = confirm
        self.stop()