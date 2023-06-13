import discord
from discord.ext import commands
import blockcypher

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
stock_count = 100
API_TOKEN = "TOKEN"

# A dictionary to store payment addresses and their associated payments
payment_addresses = {}

@client.command()
async def commander(ctx, *, arg):
    global stock_count  # Access the global stock_count variable
    if stock_count > 0:
        arg = int(arg)
        stock_count -= arg  # Deduct 1 from the stock count

        payment_address = get_payment_address()
        payment_addresses[payment_address] = arg  # Store the payment address and corresponding command quantity

        embed = discord.Embed(title="Dofus_GEN",
                              description=f"Votre commande de : {arg}",
                              color=discord.Color.blue())
        embed.add_field(name="Adresse BTC", value=payment_address, inline=False)
        embed.add_field(name="Prix", value="1€", inline=True)
        embed.add_field(name="Prix en BTC", value="$1", inline=True)
        embed.add_field(name="Description", value="Test", inline=False)

        await ctx.send(embed=embed)

        embed2 = discord.Embed(title="Dofus_GEN",
                               description=f"Votre commande de : {arg}",
                               color=discord.Color.blue())
        embed2.add_field(name="Adresse BTC", value=payment_address, inline=False)
        embed2.add_field(name="Prix    ", value="1€    ", inline=True)
        embed2.add_field(name="Prix en BTC  ", value="$1    ", inline=True)
        embed2.add_field(
            name="Description",
            value="Veuillez envoyer à cette adresse le montant mentionné",
            inline=False)
        await ctx.author.send(embed=embed2)
    else:
        await ctx.send("Stock is empty.")

def get_payment_address():
    address = blockcypher.generate_new_address(coin_symbol='btc', api_key=API_TOKEN)['address']
    if address:
        return address
    else:
        return "Error generating payment address."

@client.command()
async def stock(ctx):
    global stock_count  # Access the global stock_count variable
    await ctx.send(f">>> Il y a {stock_count} comptes disponibles")

# Override the on_message event to handle webhook notifications
@client.event
async def on_message(message):
    if message.content.startswith('Payment confirmed for address'):
        print(message.content)  # Print the confirmation message
        address = message.content.split(':')[1].strip()
        if address in payment_addresses:
            quantity = payment_addresses[address]
            print(f"Payment confirmed for {quantity} items.")
            # Perform any additional actions or updates based on the payment confirmation
            # For example, you can update the stock count or mark the order as paid.
    await client.process_commands(message)  # Process other commands

client.run('TOKEN')
