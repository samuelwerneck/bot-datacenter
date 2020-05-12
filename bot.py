from environs import Env
import discord

# Importa o TOKEN de autenticação do arquivo de variáveis
# Arquivo .env que deve estar no mesmo diretório
env = Env()
env.read_env()
TOKEN = env.str("TOKEN")


client = discord.Client()

# Define o ID do canal monitoramento
async def getCanal():
    canal = client.get_channel(691685353769140254)
    return canal


# Encontra as mensagens marcadas como "RESOLVIDAS:"
async def encontra_mensagens(canal):
    cn = canal
    lista = []
    async for message in cn.history(limit=500):

        if len(message.embeds) == 0:
            pass

        if len(message.embeds) != 0:
            if 'RESOLVIDO:' in message.embeds[0].title:
                lista.append(message.embeds[0].footer.text)
    return lista


# Deleta as mensagens selecionadas
async def deleta_mensagens(lista, autor):
    canal = await getCanal()
    deletar = lista
    usuario = autor
    await canal.send(f'Lista de mensagens a deletar solicitada por: {usuario}\n{deletar}')



    async for message in canal.history(limit=500):

        # if len(message.embeds) == 0:
        #     pass

        if len(message.embeds) != 0:
            print(message.embeds[0].footer.text)
            if message.embeds[0].footer.text in deletar:
                print(f'Deletando {message.embeds[0].footer.text}')
                await message.delete()


@client.event
async def on_ready():
    print(f'{client.user.name} conectado')


@client.event
async def on_message(msg):
    canal = await getCanal()
    # Verifica se o autor da mensagem é o próprio bot e se a mensagem foi
    # enviada em outro canal que não o #monitoramento.
    if (msg.author == client.user) or (str(msg.channel) != "monitoramento"):
        return

    if msg.content == 'teste':
        autor = msg.author.name
        lista = await encontra_mensagens(canal)
        await deleta_mensagens(lista, autor)


client.run(TOKEN)