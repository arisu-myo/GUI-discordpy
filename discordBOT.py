
# import asyncio
import discord
from discord.ext import commands  # , tasks
import datetime
import tracemalloc

tracemalloc.start()


def event_time():
    now = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%m:%S : "))
    return now


class VioceBot(commands.Cog, name="ボイスボッド"):
    @commands.command()
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
            await ctx.send("OK")
            return
        except Exception as e:
            print(e)
            await ctx.message.guild.voice_client.disconnect()
            await ctx.author.voice.channel.connect()

            await ctx.send("すでにボイスチャンネルに入ってため再度接続しました。")
            return

    @commands.command()
    async def unjoin(self, ctx):
        """ボイスチャンネルの接続を"""
        try:
            await ctx.message.guild.voice_client.disconnect()
            await ctx.send("ボイスチャンネルへの接続解除しました")
        except Exception as e:
            print(str(e))

            await ctx.send("ボイスチャンネルへの接続を正常解除できません。")


class RootUserSystem(commands.Cog, name="開発者向け機能"):
    """開発者向けのシステムです
    この以下のコマンド郡は、システム管理者に許可を得てください
    """

    @commands.command()
    async def logout(self, ctx):
        await ctx.message.delete()
        await client.close()
        print("logout")
        return


def create_client():
    intents = discord.Intents.default()
    intents.members = True

    client_reb = commands.Bot(command_prefix="$",
                              intents=intents)
    return client_reb


client = create_client()
client.add_cog(RootUserSystem(client))
client.add_cog(VioceBot(client))


@client.event
async def on_ready():
    print(f"{event_time()}BOT起動しました...")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if "$" in message.content:
        pass
        # elif "<@" in message.content:
        #    pass
    elif message.guild.voice_client:
        # inputtext = creat_audio(message.content)

        print(f"voice_play>>{message.content}")
        return
    else:
        pass
    await client.process_commands(message)


@ client.event
async def on_command_error(ctx, error):
    await ctx.send("エラーコマンド実行者:{}\n エラー詳細:{}"
                   .format(ctx.message.author.name, error))


def start(token):

    client.loop.create_task(client.start(token))

    try:
        client.loop.run_forever()
    finally:
        client.loop.close()
        print(f"{event_time()}終了が実行されました!")


def end():
    client.loop.stop()
