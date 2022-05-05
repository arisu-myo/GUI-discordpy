
import discord
from discord.ext import commands
import asyncio
token = "NzcwMDY2MTY5NzkzMDg1NDcw.X5YKAg.IMn3xg-NLWxF9htDIssAlMSTAtk"


"""
クラスとか構成が根本的に改造したいといけない？？
Discordpyのclient.run(token)の場合は起動、コマンド動作が行える
（一部client系の操作が効かないけど・・・）

Discordpyのclient.start(*args, **kwargs)をasyncio（非同期系の処理）
のself.loop.run_forever()で飛ばすと起動はするが、コマンド操作当を一切
受け付けないこれを解決しないとどうしようもない

最悪プロセスを作って強制終了させるっていう手も・・・・？

"""


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
        print("logout")

        # await client.close()
        return


class BOT():
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True

        self.client = commands.Bot(command_prefix="$",
                                   intents=intents)

    def start(self, *args, **kwargs):

        self.client.add_cog(RootUserSystem(self.client))
        self.client.add_cog(VioceBot(self.client))

        try:
            self.loop = asyncio.new_event_loop()
            # task =
            self.loop.create_task(
                self.client.start(*args, **kwargs))
            self.loop.run_forever()

            # self.client.run(token)

            # self.loop.run_until_complete(self.client.start(token,))
        except KeyboardInterrupt:
            return

    def end(self, *args, **kwargs):
        self.loop.stop()

    async def on_ready():
        print("起動")
