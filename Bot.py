import asyncio #libreria de asyncio

import discord #libreria de discord
import youtube_dl #necesitamos la libreria de youtube_dl instalar con pip como extra se necesita ytdl, instalar con apt-get

from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # dejar como esta
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            #
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class BotPrincipal:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Se une al canal de discord"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Para reproducir musica de manera local"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Ahora sonando: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Para reproducir por url youtube """

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Ahora sonando: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Para hacer un stremam por url url (casi igual que yt, pero este no descarga antes)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Ahora sonando: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Para Cambiar el volumen """

        if ctx.voice_client is None:
            return await ctx.send("No esta conectado a ningun canal de voz.")

        ctx.voice_client.source.volume = volume
        await ctx.send("Cambiar el volumen a {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Para desconectar al bot del canal de voz"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("No estas conectado a ningun canal de voz.")
                raise commands.CommandError("El usuario no esta conectado a ningun canal de voz.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            #Aqui iniciamos el diccionario
    @commands.command() #ejemplo con un gato
    async def cat(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")
        #Abajo de este iran los comandos

    @commands.command()
    async def algoritmo(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("conjunto de reglas bien definidas para la resolución de un problema. Un programa de software es la trascripción, en lenguaje de programación, de un algoritmo.")

    @commands.command()
    async def apache(self, ctx): #siempre hay que poner self y ctx
        await ctx.send(" servidor web de distribución libre. Fue desarrollado en 1995 y ha llegado a ser el más usado de Internet. ")

    @commands.command()
    async def bios(self, ctx): #siempre hay que poner self y ctx
        await ctx.send(" Basic Input/Output System: Sistema básico de ingreso/salida de datos. Conjunto de procedimientos que controla el flujo de datos entre el sistema operativo y dispositivos tales como el disco rígido, la placa de video, el teclado, el mouse y la impresora. ")

    @commands.command()
    async def bit(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("abreviatura de binary digit (dígito binario). El bit es la unidad más pequeña de almacenamiento en un sistema binario dentro de una computadora. ")

    @commands.command()
    async def cpu(self, ctx): #siempre hay que poner self y ctx
        await ctx.send(" Central Processing Unit. Unidad central de procesamiento. Es el procesador que contiene los circuitos lógicos que realizan las instrucciones de la computadora. ")

    @commands.command()
    async def database(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("En español Base de datos, es un “almacén” que nos permite guardar grandes cantidades de información de forma organizada para que luego podamos encontrar y utilizar fácilmente.")

    @commands.command()
    async def DNS(self, ctx): #siempre hay que poner self y ctx
        await ctx.send(" Domain Name System. Sistema de Nombres de Dominio. Método de identificación de una dirección de Internet. Según este método, cada computadora de la red se identifica con una dirección unívoca, la URL (Uniform Resource Locator), compuesta de grupos de letras separados por puntos.")

    @commands.command()
    async def encriptar(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("proteger archivos expresando su contenido en un lenguaje cifrado. Los lenguajes cifrados simples consisten, por ejemplo, en la sustitución de letras por números. ")

    @commands.command()
    async def ethernet(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("tecnología para red de área local. Fue desarrollada originalmente por Xerox y posteriormente por Xerox, DEC e Intel. Ha sido aceptada como estándar por la IEEE. ")

    @commands.command()
    async def extranet(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("parte de una intranet de acceso disponible a clientes y otros usuariosajenos a la compañía.")

    @commands.command()
    async def giga(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("prefijo que indica un múltiplo de 1.000 millones, o sea 10^9. Cuando se emplea el sistema binario, como ocurre en informática, significa un múltiplo de 2^30, o sea 1.073.741.824")

    @commands.command()
    async def gigabit(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("Aproximadamente 1.000 millones de bits (exactamente 1.073.741.824 bits). ")

    @commands.command()
    async def gigaflop(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("medida de velocidad de una computadora equivalente a 1.000 millones de operaciones de coma flotante por segundo. ")

    @commands.command()
    async def hosting(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("alojamiento. Servicio ofrecido por algunos proveedores, que brindan a sus clientes (individuos o empresas) un espacio en su servidor para alojar un sitio web. ")

    @commands.command()
    async def html(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("Hyper Text Mark-up Language. Lenguaje de programación para armar páginas web.")

    @commands.command()
    async def http(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("Hypertext Transfer Protocol. Protocolo de transferencia de hipertextos. Es un protocolo que permite transferir información en archivos de texto, gráficos, de video, de audio y otros recursos multimedia. ")

    @commands.command()
    async def informatica(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("es la rama de la Ingeniería que estudia el hardware, las redes de datos y el software necesarios para tratar información de forma automática.")

    @commands.command()
    async def internet(self, ctx): #siempre hay que poner self y ctx
        await ctx.send(" red de redes. Sistema mundial de redes de computadoras interconectadas.")

    @commands.command()
    async def intranet(self, ctx): #siempre hay que poner self y ctx
        await ctx.send(" red de redes de una empresa. Su aspecto es similar al de las páginas de Internet. ")

    @commands.command()
    async def ip(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("Protocolo de Internet")

    @commands.command()
    async def iso(self, ctx): #siempre hay que poner self y ctx
        await ctx.send(" International Organization for Standardization. Fundada en 1946, es una federación internacional que unifica normas en unos cien países. Una de ellas es la norma OSI, modelo de referencia universal para protocolos de comunicación. ")

    @commands.command()
    async def isp(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("Internet Service Provider. Proveedor de servicios de Internet.")

    @commands.command()
    async def kernel(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("núcleo o parte esencial de un sistema operativo. Provee los servicios básicos del resto del sistema.")

    @commands.command()
    async def kilobit(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("1.024 bits.")

    @commands.command()
    async def kilobyte(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("unidad de medida de una memoria. l kilobyte = 1024 bytes.")

    @commands.command()
    async def lan(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("Local Area Network: Red de Área Local. Red de computadoras interconectadas en un área reducida, por ejemplo, una empresa.")

    @commands.command()
    async def linux(self, ctx): #siempre hay que poner self y ctx
        await ctx.send(" sistema operativo gratuito para computadoras personales derivado de Unix.")

    @commands.command()
    async def login(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("conexión. Entrada en una red.")

    @commands.command()
    async def megabit(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("Aproximadamente 1 millón de bits. (1.048.576 bits).")

    @commands.command()
    async def megabyte(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("unidad de medida de una memoria. 1 megabyte = 1024 kilobytes = 1.048.576 bytes. ")

    @commands.command()
    async def megahertz(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("Un millón de hertz o hercios.")

    @commands.command()
    async def motherboard(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("placa madre. Placa que contiene los circuitos impresos básicos de la computadora, la CPU, la memoria RAM y slots en los que se puede insertar otras placas (de red, de audio, etc.). ")

    @commands.command()
    async def nano(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("prefijo que significa una milmillonésima parte.")

    @commands.command()
    async def net(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("WorldWideWeb")

    @commands.command()
    async def query(self, ctx): #siempre hay que poner self y ctx
        await ctx.send("consulta. Búsqueda en una base de datos.")

    @commands.command()
    async def ram(self, ctx):
        await ctx.send("Random Acces Memory: Memoria de acceso aleatorio. Memoria donde la computadora almacena datos que le permiten al procesador acceder rápidamente al sistema operativo, las aplicaciones y los datos en uso.")

    @commands.command()
    async def rom(self, ctx):
        await ctx.send(" Read Only Memory: Memoria de sólo lectura. Memoria incorporada que contiene datos que no pueden ser modificados. Permite a la computadora arrancar.")

    @commands.command()
	async def abstracion(self, ctx):
		await ctx.send(" Proceso de análisis del mundo real con el propósito de interpretar los aspectos esenciales de un problema y expresarlo en términos precisos.")
#2
	@commands.command()
	async def arbol(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Estructura de datos en la cual los registros son almacenados de manera jerárquica. ")
#3
	@commands.command()
	async def ASCII(self, ctx): #siempre hay que poner self y ctx
		await ctx.send("  American Standard Code of Information Interchange(por sus siglas en inglés: Código normalizado estadounidense para el intercambio de la información. Código que permite definir caracteres alfanuméricos; se lo usa para lograr compatibilidad entre diversos procesadores de texto.")
#4
	@commands.command()
	async def buffer(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Conjunto de datos organizados de modo tal que resulte fácil acceder a ellos, gestionarlos y actualizarlos. ")
#6
	@commands.command()
	async def bug(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Bicho, insecto. Error de programación que genera problemas en las operaciones de una computadora.")
#7
	@commands.command()
	async def cache(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" En un navegador, el caché guarda copias de documentos de acceso frecuente, para que en el futuro aparezcan más rápidamente. \n  En un disco: pequeña porción de memoria RAM que almacena datos recientemente leídos, con lo cual agiliza el acceso futuro a los mismos datos. ")
#8
	@commands.command()
	async def cookie(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Pequeño archivo de texto que un sitio web coloca en el disco rígido de una computadora que lo visita. Al mismo tiempo, recoge información sobre el usuario. Agiliza la navegación en el sitio. Su uso es controvertido, porque pone en riesgo la privacidad de los usuarios. ")
#9
	@commands.command()
	async def computadora(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Máquina electrónica, analógica o digital, dotada de una memoria de gran capacidad y de métodos de tratamiento de la información, capaz de resolver problemas matemáticos y lógicos mediante la ejecución de programas informáticos")
#10
	@commands.command()
	async def BFS(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" es un algoritmo de búsqueda sin información, que expande y examina todos los nodos de un árbol sistemáticamente para buscar una solución.")
#11
	@commands.command()
	async def compilador(self, ctx): #siempre hay que poner self y ctx
		await ctx.send("  Programa informático que transforma código fuente escrito en un lenguaje de programación o lenguaje informático (el lenguaje fuente), en otro lenguaje informático (el lenguaje objetivo, estando a menudo en formato binario conocido como código objeto).")
#12
	@commands.command()
	async def chat(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Servicio de internet que permite conversar en tiempo real a dos o más personas geográficamente distantes. Para hacer uso de este servicio es necesario contar con una cuenta de correo electrónico y un software llamado cliente de chat.")
#13
	@commands.command()
	async def ADSL(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Tipo de línea telefónica que permite trasmitir información a gran velocidad. Simultanea el flujo de datos y de voz, por lo que permite hablar por teléfono al tiempo que se usa cualquier servicio de internet. \n Las siglas corresponden a las palabras en inglés: Asymmetric Digital Subscriber Line (línea de usuario asimétrica digital). Se dice que es asimétrica porque la velocidad de descarga de datos es mayor (no igual) a la de envío de datos.")
#14
	@commands.command()
	async def CSS(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" es un lenguaje de hojas de estilos creado para controlar el aspecto o presentación de los documentos electrónicos definidos con HTML y XHTML. CSS es la mejor forma de separar los contenidos y su presentación y es imprescindible para crear páginas web complejas.")
#15
	@commands.command()
	async def enlace(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Elemento de una página web que da acceso a otro documento (o a otra parte del mismo documento) al hacer clic sobre él con el botón izquierdo del ratón. Es la base del acceso a la información en la World Wide Web. Un enlace puede estar sobre texto o sobre una imagen. Se reconocen porque el puntero del ratón se convierte en una mano al pasar sobre un enlace.")
#16
	@commands.command()
	async def foro(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Servicio ofrecido por internet que permite emitir opiniones por escrito sobre temas de discusión. Se pueden abrir temas de trabajo y hacer comentarios a las opiniones de otros, de forma que los artículos pueden aparecer anidados. Suele ser necesario darse de alta para hacer uso de este servicio, indicando una dirección de e-mail personal, y hay un moderador o administrador que se encarga de que no aparezcan opiniones ofensivas o que no traten del tema al que está dedicado el foro. Los temas son muy variados: educación, informática, ocio, amigos, lecturas...")
#17
	@commands.command()
	async def gif(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Formato de imágenes y animaciones muy utilizado para transmitir imágenes en internet. Las siglas provienen de Graphics Interchange Format. Optimiza el tamaño de los dibujos (no tanto de las fotografías, para las que es más conveniente el formato .jpg). Admite la transparencia de un color y permite la construcción de animaciones.")
#18
	@commands.command()
	async def periferico(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Se llama así a cualquier aparato que se conecta a la CPU, como el monitor, el ratón o el escaner. Son necesarios para intercambiar información con ella. Pueden ser de tres tipos: \n DE ENTRADA: cuando sirven para introducir datos en el ordenador. Por ejemplo el teclado, el ratón, el escaner. \n DE SALIDA: cuando sirven para extraer datos del ordenador. Por ejemplo el monitor, la impresora... \n DE ENTRADA Y SALIDA: cuando tienen ambas funciones. Por ejemplo: el módem, la tarjeta de red...")
#19
	@commands.command()
	async def procesador(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Circuitos electrónicos incluidos en una pastilla que ejecutan las instrucciones básicas de un ordenador. Es el núcleo que le permite realizar todas las operaciones que nosotros utilizamos. También se le llama microprocesador, debido a su pequeño tamaño. Cuando un procesador opera, su temperatura se eleva y pierde efectividad. Por eso es necesario un sistema de ventilación (normalmente un simple ventilador de aspas) que aseguren la temperatura adecuada.")
#20
	@commands.command()
	async def red(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Conjunto e dos o más ordenadores conectados entre sí, que son capaces de intercambiar datos e información. Según la distancia existente entre los ordenadores conectados, podemos hablar de una LAN (Local Area Network, o Red de Área local) si los ordenadores conectados están físicamente próximos. Un ejemplo de LAN sería la red de cualquier empresa localizada en un edificio. En el caso de que los ordenadores conectados estén lejos se habla de WAN (Wide Area Network, o Red de Área Extensa). La red Internet es un caso de WAN. Para que los ordenadores conectados puedan entenderse, deben "hablar" el mismo idioma, es decir, deben utilizar el mismo código. El código empleado por Internet es el llamado TCP-IP (Protocolo de Control de la Transmisión - Protocolo de Internet)")
#21
	@commands.command()
	async def router(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Se podría traducir por /Encaminador/, pero se usa siempre la palabra inglesa router. Es un aparato dotados de cierta programación, que permite comunicar un ordenador o una red de ordenadores con la red Internet. La vía usada para esta conexión es una línea telefónica del tipo ADSL.")
#22
	@commands.command()
	async def servidor(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Se llama así a un ordenador central de un sistema de red que proporciona servicios y programas a otros ordenadores conectados. En el caso de estar trabajando con servicios de internet, se habla de /servidor de correo/ si ofrece cuentas de correo electrónico, /servidor web/ si almacena y ofrece acceso a páginas con hipertexto, /servidor de FTP/ si proporciona acceso a archivos, etc.")
#23
	@commands.command()
	async def slot(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Ranura de la placa base del ordenador que permite insertar una nueva tarjeta que amplía las funcionalidades de la máquina.")
#24
	@commands.command()
	async def software(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Parte lógica del ordenador. Se trata de un conjunto de órdenes lógicas cuya ejecución permite al usuario realizar un trabajo con el ordenador. Son los llamados /programas/. Se almacenan en la memoria y pueden se muy variados: de tratamiento de texto, de tratamiento de imágenes, de control numérico, de reproducción multimedia... El propio sistema operativo del ordenador se considera software.")
#25
	@commands.command()
	async def hardware(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" La palabra hardware en informática se refiere a las partes físicas tangibles de un sistema informático; sus componentes eléctricos, electrónicos, electromecánicos y mecánicos.")
#26
	@commands.command()
	async def spam(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Recibe este nombre el correo electrónico que se recibe sin ser solicitado. Se considera poco ético, y en ocasiones, puede se portador de virus. Normalmente su fin es el de la publicidad.")
#27
	@commands.command()
	async def tcp_ip(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Son las  siglas en inglés de Protocolo de Control de la Transemisión / Protocolo de Internet. Es el código que emplean los ordenadores que están conectados por la red Internet para comunicarse entre sí. Sin este código común, sería imposible el intercambio de datos.")
#28
	@commands.command()
	async def url(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Siglas de la expresión en inglés Uniform Resource Locator (Localizador Uniforme de Recursos). Es la dirección de una página web en internet. Por ejemplo: https://uls.edu.sv/sitioweb/ \n La URL está formada por \na) El protocolo de servicio (http://). Si no se escribe, el navegador lo añade por defecto. \n b) El nombre de dominio del ordenador en el que está almacenada la página (www.catedu.es). No todos los dominios llevan las www. \n c) La carpeta o carpetas en que se encuentra el archivo solicitado y el nombre de éste. Si el archivo es el principal de la carpeta, no es necesario indicarlo. Éste es el caso del ejemplo. \n Como separador de las distintas partes se utiliza la barra /")
#29
	@commands.command()
	async def virus(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Son programas capaces de autocopiarse en los medios de almacenamiento de los ordenadores (disco duro, pendrives...) Esta capacidad de copiarse en el nuevo medio es lo que les ha dado el nombre de virus, ya que se puede considerar que se multiplican y que infectan el ordenador en el que lo hacen. Una vez copiado, cuando se ejecute su código, realizará en el nievo ordenador todas las acciones que indiquen sus instrucciones. Pueden ser muy dañinos, ya que pueden destruir datos e incluso dañar la información necesaria para utilizar el ordenador. Los daños se producen a nivel de software.")
#30
	@commands.command()
	async def wireless(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Literalmente significa (sin cables). Normalmente se usa el término inalámbrico como traducción. Es aquella tecnología que no usa cables para transmitir datos.")
#31
	@commands.command()
	async def wifi(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Abreviatura de Wirless Fidelity, también llamada WLAN (Wireless LAN = red sin cables). Es una red inalámbrica para conectar ordenadores.")
#32
	@commands.command()
	async def wlan(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Wireless LAN, red sin cables: Una red de área local inalámbrica, también conocida como WLAN (del inglés wireless local area network), es un sistema de comunicación inalámbrico para minimizar las conexiones cableadas.")
#33
	@commands.command()
	async def lan(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Red de Área Local. Una red de área local, red local o LAN (del inglés local area network) es la interconexión de varias Computadoras y Periféricos. Su extensión está limitada físicamente a un edificio o a un entorno de 200 metros, o con Repetidores podría llegar a la distancia de un campo de 1 kilómetro.")
#34
	@commands.command()
	async def sintaxis(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Reglas que determinan cómo se pueden construir y secuenciar los elementos del lenguaje.")
#35
	@commands.command()
	async def semantica(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Significado de cada elemento del lenguaje. El término semántica se refiere a los aspectos del significado, sentido o interpretación de signos lingüísticos como símbolos, palabras, expresiones o representaciones formales.")
#36
	@commands.command()
	async def www(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Literalmente se podría traducir por /telaraña mundial/. Es un servicio de internet que ofrece la transmisión de datos en forma de hipertexto (en código HTML), o sea, páginas web y toda la información multimedia que normalmente va asociada a éstas. Este Sistema de información global fue desarrollado en 1990 por Robert Cailliau y Tim Berners-Lee en el CERN (Consejo Europeo para la Investigación Nuclear). Se suele abreviar como www.")
#37
	@commands.command()
	async def interprete(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" En ciencias de la computación, intérprete o interpretador es un programa informático capaz de analizar y ejecutar otros programas.")
#38
	@commands.command()
	async def tarea(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Un programa se vuelve tarea a partir del momento que se lo selecciona para su ejecución y hasta que esta termina.")
#39
	@commands.command()
	async def programar(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Dividir una tarea compleja en las pequeñas acciones necesarias para su ejecución y expresarla en comandos comprensibles para una máquina.")
#40
	@commands.command()
	async def programa(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Un programa informático o programa de computadora es una secuencia de instrucciones, escritas para realizar una tarea específica en una computadora.​ Este dispositivo requiere programas para funcionar, por lo general, ejecutando las instrucciones del programa en un procesador central.​")
#41
	@commands.command()
	async def variable(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" En programación, las variables son espacios reservados en la memoria que, como su nombre indica, pueden cambiar de contenido a lo largo de la ejecución de un programa. Una variable corresponde a un área reservada en la memoria principal del ordenador.")
#42
	@commands.command()
	async def poo(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" La programación orientada a objetos (POO, u OOP según sus siglas en inglés) es un paradigma de programación que viene a innovar la forma de obtener resultados. Los objetos manipulan los datos de entrada para la obtención de datos de salida específicos, donde cada objeto ofrece una funcionalidad especial.")
#43
	@commands.command()
	async def clases(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Dentro de la programación orientada a objetos, las clases son un pilar fundamental. Estas nos van a permitir abstraer los datos y sus operaciones asociadas como si tuviéramos en frente una caja negra. ")
#44
	@commands.command()
	async def tuplas(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" En matemáticas, una tupla es una lista ordenada de elementos. Una n-tupla es una secuencia (o lista ordenada) de n elementos, siendo n un número natural (entero no-negativo). La única 0-tupla es la secuencia vacía. Una n-tupla se define inductivamente desde la construcción de un par ordenado.")
#45
	@commands.command()
	async def listas(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Una lista es una estructura de datos que contiene una colección o secuencia de datos. Los datos o elementos de una lista deben ir separados con una coma y todo el conjunto entre corchetes. Se dice que una lista es una estructura mutable porque además de permitir el acceso a los elementos, pueden suprimirse o agregarse nuevos.")
#46
	@commands.command()
	async def diccionarios(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Los diccionarios son objetos que contienen una lista de parejas de elementos. De cada pareja un elemento es la clave, que no puede repetirse, y, el otro, un valor asociado. La clave que se utiliza para acceder al valor tiene que ser un dato inmutable como una cadena, mientras que el valor puede ser un número, una cadena, un valor lógico (True/False), una lista o una tupla.")
#47
	@commands.command()
	async def python(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Python es un lenguaje de programación interpretado cuya filosofía hace hincapié en una sintaxis que favorezca un código legible. Se trata de un lenguaje de programación multiparadigma, ya que soporta orientación a objetos, programación imperativa y, en menor medida, programación funcional.")
#48
	@commands.command()
	async def indentacion(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Indentación es un anglicismo de uso común en informática; no es un término reconocido por la Real Academia Española. La Real Academia recomienda utilizar «sangrado»")
#49
	@commands.command()
	async def bucle(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Un bucle o ciclo, en programación, es una sentencia que ejecuta repetidas veces un trozo de código, hasta que la condición asignada a dicho bucle deja de cumplirse. Los tres bucles más utilizados en programación son el bucle while, el bucle for y el bucle do-while.")
#50
	@commands.command()
	async def excepciones(self, ctx): #siempre hay que poner self y ctx
		await ctx.send(" Son comportamientos anómalos que se producen porque las cosas fallan. Así de simple: todo falla. Porque un fichero de texto está corrupto. Porque el disco duro tiene un sector defectuoso. Porque el usuario interrumpe de forma abrupta la ejecución del programa. Porque el usuario introduce una letra cuando tu programa está esperando un número. Porque hay un cable flojo en un prototipo electrónico. Tu programa puede estar perfectamente escrito, y que algo pase: porque las cosas pasan, y si algo puede pasar, en algún momento ten por seguro que pasará.")

        #Inicio de Arturo

    @commands.command() #comando de ayuda
    async def ayuda(self, ctx):
        embed = discord.Embed(title="Bot ULS", description="Lista de comandos del bot", color=0xeee657) #Con help tira una lista de cada comando para darle informacion y que hace cada cosa
        embed.add_field(name="$cat", value="ON", inline=False)
        embed.add_field(name="$rom", value="ON", inline=False)
        embed.add_field(name="$query", value="ON", inline=False)
        embed.add_field(name="$ram", value="ON", inline=False)
        embed.add_field(name="$net", value="ON", inline=False)
        embed.add_field(name="$net", value="ON", inline=False)
        embed.add_field(name="$nano", value="ON", inline=False)
        embed.add_field(name="$motherboard", value="ON", inline=False)
        embed.add_field(name="$megahertz", value="ON", inline=False)
        embed.add_field(name="$megabyte", value="ON", inline=False)
        embed.add_field(name="$megabit", value="ON", inline=False)
        embed.add_field(name="$login", value="ON", inline=False)
        embed.add_field(name="$lan", value="ON", inline=False)
        embed.add_field(name="$linux", value="ON", inline=False)
        embed.add_field(name="$ip", value="ON", inline=False)
        embed.add_field(name="$intranet", value="ON", inline=False)
        embed.add_field(name="$internet", value="ON", inline=False)
        embed.add_field(name="$informatica", value="ON", inline=False)
        embed.add_field(name="$http", value="ON", inline=False)
        embed.add_field(name="$html", value="ON", inline=False)
        embed.add_field(name="$hosting", value="ON", inline=False)
        embed.add_field(name="$gigaflop", value="ON", inline=False)
        embed.add_field(name="$gigabit", value="ON", inline=False)
        embed.add_field(name="$giga", value="ON", inline=False)
        embed.add_field(name="$extranet", value="ON", inline=False)
        embed.add_field(name="$ethernet", value="ON", inline=False)
        embed.add_field(name="$encriptar", value="ON", inline=False)
        embed.add_field(name="$DNS", value="ON", inline=False)
        embed.add_field(name="$database", value="ON", inline=False)
        embed.add_field(name="$cpu", value="ON", inline=False)
        embed.add_field(name="$bit", value="ON", inline=False)
        embed.add_field(name="$bios", value="ON", inline=False)
        embed.add_field(name="$apache", value="ON", inline=False)
        embed.add_field(name="$algoritmo", value="ON", inline=False)
        #Inicio de gloria
        embed.add_field(name="$abstracción", value="ON", inline=False)
        embed.add_field(name="$ADSL", value="ON", inline=False)
        embed.add_field(name="$arbol", value="ON", inline=False)
        embed.add_field(name="$ascii", value="ON", inline=False)
        embed.add_field(name="$BFS", value="ON", inline=False)
        embed.add_field(name="$buffer", value="ON", inline=False)
        embed.add_field(name="$bug", value="ON", inline=False)
        embed.add_field(name="$cache", value="ON", inline=False)
        embed.add_field(name="$chat", value="ON", inline=False)
        embed.add_field(name="$computadora", value="ON", inline=False)
        embed.add_field(name="$cookie", value="ON", inline=False)
        embed.add_field(name="$compilador", value="ON", inline=False)
        embed.add_field(name="$CSS", value="ON", inline=False)
        embed.add_field(name="$enlace", value="ON", inline=False)
        embed.add_field(name="$foro", value="ON", inline=False)
        embed.add_field(name="$gif", value="ON", inline=False)
        embed.add_field(name="$hardware", value="ON", inline=False)
        embed.add_field(name="$periferico", value="ON", inline=False)
        embed.add_field(name="$procesador", value="ON", inline=False)
        embed.add_field(name="$red", value="ON", inline=False)
        embed.add_field(name="$router", value="ON", inline=False)
        embed.add_field(name="$servidor", value="ON", inline=False)
        embed.add_field(name="$slot", value="ON", inline=False)
        embed.add_field(name="$software", value="ON", inline=False)
        embed.add_field(name="$spam", value="ON", inline=False)
        embed.add_field(name="$tcp/ip", value="ON", inline=False)
        embed.add_field(name="$url", value="ON", inline=False)
        embed.add_field(name="$virus", value="ON", inline=False)
        embed.add_field(name="$wireless", value="ON", inline=False)
        embed.add_field(name="$wifi", value="ON", inline=False)
        embed.add_field(name="$wlan", value="ON", inline=False)
        embed.add_field(name="$lan", value="ON", inline=False)
        embed.add_field(name="$www", value="ON", inline=False)
        embed.add_field(name="$interprete", value="ON", inline=False)
        embed.add_field(name="$semantica", value="ON", inline=False)
        embed.add_field(name="$tarea", value="ON", inline=False)
        embed.add_field(name="$programar", value="ON", inline=False)
        embed.add_field(name="$programa", value="ON", inline=False)
        embed.add_field(name="$variable", value="ON", inline=False)
        embed.add_field(name="$poo", value="ON", inline=False)
        embed.add_field(name="$clases", value="ON", inline=False)
        embed.add_field(name="$tuplas", value="ON", inline=False)
        embed.add_field(name="$diccionarios", value="ON", inline=False)
        embed.add_field(name="$listas", value="ON", inline=False)
        embed.add_field(name="$python", value="ON", inline=False)
        embed.add_field(name="$indentacion", value="ON", inline=False)
        embed.add_field(name="$bucle", value="ON", inline=False)
        embed.add_field(name="$excepciones", value="ON", inline=False)
        #Inicio de arturo
        await ctx.send(embed=embed)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"),
                   description='Bot')

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
print('------')

bot.add_cog(BotPrincipal(bot))
#Aca lleva el token
bot.run('')
