import discord
from discord import Embed
class DescriptionEmbed(Embed):
    def add_field(self, key, value):
        if self.description == Embed.Empty:
            self.description = f'**{key}:** {value}'
        else:
            self.description = f'{self.description}\n**{key}:** {value}'
        
        return self

    def add_spacer(self):
        if self.description != Embed.Empty:
            self.description = f'{self.description}\n'