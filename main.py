import discord, os, time
from discord.ext import commands
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Functions:
async def download_visual_map():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://coinank.com/indexdata/VisualMap")
        time.sleep(3)
        element = page.locator("canvas")
        await element.screenshot(path="visual-map.png")

        await browser.close()

async def download_liq_heatmap():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://coinank.com/liqHeatMapChart")
        time.sleep(5)
        element = page.locator("canvas")
        await element.screenshot(path="liq-heatmap.png")

        await browser.close()

# Events:
@bot.event
async def on_ready():
    print(f"🟢 | Bot Running As: {bot.user.name}")

# Commands:
@bot.command()
async def visual_map(ctx):
    async def callback(interaction: discord.Interaction):
        await interaction.response.send_message("Downloading visual map...", ephemeral=True)
        await download_visual_map()
        await interaction.followup.send(content="✅ Here is the visual map:", file=discord.File("visual-map.png"), ephemeral=True)

    button = discord.ui.Button(label="Visual Map", style=discord.ButtonStyle.blurple)
    button.callback = callback

    view = discord.ui.View(timeout=None)
    view.add_item(button)

    await ctx.send("Click the button to view visual map.", view=view)

@bot.command()
async def liq_heatmap(ctx):
    async def callback(interaction: discord.Interaction):
        await interaction.response.send_message("Downloading liquidation heatmap...", ephemeral=True)
        await download_liq_heatmap()
        await interaction.followup.send(content="✅ Here is the liquidation heatmap:", file=discord.File("liq-heatmap.png"), ephemeral=True)

    button = discord.ui.Button(label="Liquidation Heatmap", style=discord.ButtonStyle.blurple)
    button.callback = callback

    view = discord.ui.View(timeout=None)
    view.add_item(button)

    await ctx.send("Click the button to view liquidation heatmap.", view=view)

bot.run(BOT_TOKEN)
