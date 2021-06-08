from wordcloud import WordCloud

text = ' computadores' \
' telemóveis' \
' rede' \
' drones'\
' telemóveis'\
' chip'\
' Imagem'\
' telefilme'\
' redes sociais'\
' internet'\
' ensino à distância'\
' stayway covid'\
' aula à distância'\
' plataforma'\
' ensino à distância'\
' web summit'\
' redes sociais'\
' redes sociais'\
' web summit'\
' web summit'\
' web summit'\
' aula online'\
' web summit'\
' compras online'\
' propaganda online'\
' web summit'\
' e-mails'\
' web summit'\
' web summit'\
' jogo online'\
' redes sociais'\
' redes sociais'\
' teletrabalho'\
' teletrabalho'\
' psicologia online'\
' whatsapp'\
' uber'\
' football leaks'\
' site'\
' web summit'\
' web summit'\
' web summit'\
' fake news'\
' web summit'\
' rui pinto'\
' rui pinto'\
' hacker'\
' rui pinto'\
' hacker'\
' edward snowden'\
' hackers'\
' influencers'\
' influencer'\
' zuckerberg'\
' trolls'\
' startup'\
' hacker'\
' google'\
' hacker'

wc = WordCloud(width=1980,  min_word_length=2, height=720, max_words=1000,  background_color='white').generate(text)
wc.to_file("words_cloud.png")