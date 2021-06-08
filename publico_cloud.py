from wordcloud import WordCloud, STOPWORDS
from tika import parser # pip install tika


raw = parser.from_file("PublicoPDF/2017/P_2017_10_15.pdf")
text = raw['content']
stopwords = set(STOPWORDS)
stopwords.update(
    [
        "o", "os", "ou", 
        "a", "à", "ao", "aos", "as", "ás", "á", "às",
        "que", 
        "de", "da", "das", "do", "dos",
        "na", "nas", "ma", "num","numa",
        "em", 
        "e", "é", "ser", "estar", "ter",
        "uma", "um", 
        "para", "por", "pela", "pelo", "pela", "pelas",
        "se", "só",
        "sim", "não",
        "seu", "sua", "seus", "suas",
        "foi", "fi",
        "mais", "menos",
        "como",
        "todo", 'todos',
        "já", "até",
        "mas",
        "esta", "está","estas", "este", "estes", "isto", "desta", "isso", "isto", "esse", "esses",
        "sem", "com",
        "há", "será",
        "nos", "nós","num", 
        "são", "sem",
        "tem", "têm",
        "lhe", "lhes", "lho",
        "porque", "porquê", "por que", "por quê",
        "agora", "hoje", "ontem", "dia", "dias", "ano", "anos", "mes", "mês", "meses","tempo", "tempos", "desde", "amanhã", "sempre", 
        "hora", "horas", "minutos", "segundos", "minuto", "segundo",
        "quando", "onde", "ainda", "também", "depois", "quem", "que",
        "entre", "sobre", 
        "muito", "pouco", "bem", "mal", "mesmo",
        "pode", "podem"

    ]
)
wc = WordCloud(stopwords=stopwords, min_word_length=5, width=1980, height=720).generate(text)
wc.to_file("apagar_cloud.png")