import nextcord
import json
import os
import asyncio
from nextcord import slash_command
from nextcord.ext import commands




class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_count = 0
        self.roles = {"Support": 123456789} # Replace with the names and IDs of the roles in your server
        self.settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.json')

    @slash_command(name="newticket", description="Make a new Ticket")
    async def newticket(self, ctx):
        self.ticket_count += 1
        channel_name = f"ticket-{self.ticket_count}"
        category = self.bot.get_channel(ctx.channel.id)
        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            ctx.user: nextcord.PermissionOverwrite(read_messages=True),
            self.roles["Support"]: nextcord.PermissionOverwrite(read_messages=True)
        }
        ticket_channel = await category.create_text_channel(channel_name, overwrites=overwrites)
        await ticket_channel.send(f"{ctx.user.mention} created a new ticket!")

    @slash_command(name="closeticket", description="Close the Ticket")
    async def closeticket(self, ctx):
        if ctx.channel.category_id == ctx.channel.id:
            await ctx.channel.delete()
        else:
            await ctx.send("You cannot use this command outside of a ticket channel!")

    @slash_command(name="ticketsettings", description="Configure ticket settings.")
    async def ticketsettings(self, ctx):
        if not ctx.user.guild_permissions.administrator:
            await ctx.send("You do not have the required permissions to use this command.")
            return

        # Get a list of channels in the server
        channels = ctx.guild.channels
        channel_options = []
        for channel in channels:
            if channel.type == nextcord.ChannelType.text:
                channel_options.append(nextcord.SelectOption(label=channel.name, value=str(channel.id)))

        # Define the dropdown object
        select_menu = nextcord.ui.Select(
            placeholder="Select the ticket channel.",
            options=channel_options
        )

        # Define the embed
        embed = nextcord.Embed(title="Select a channel", description="Please select a channel from the dropdown below")

        # Add the select menu to the message
        message = await ctx.send(embed=embed, components=[select_menu])

        # Define the check for the wait_for event
        def check(interaction):
            return interaction.user.id == ctx.user_id and interaction.message == message

        # Wait for the user to select an option
        try:
            interaction = await self.bot.wait_for("select_option", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await message.edit(content="No option selected in time.", components=[])
            return

        # Get the selected option
        selected_option = interaction.values[0]

        # Handle the selected option
        selected_option = await self.bot.fetch_channel(selected_option)
        # Here you can do whatever you want with the selected channel

        # Send confirmation message
        await interaction.response.send_message(f"You selected {interaction.selected_options[0].label}")







    @newticket.error
    async def newticket_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You can create a new ticket in {error.retry_after:.0f} seconds!")

    @closeticket.error
    async def closeticket_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You cannot use this command outside of a ticket channel!")

def setup(bot):
    bot.add_cog(TicketSystem(bot))



