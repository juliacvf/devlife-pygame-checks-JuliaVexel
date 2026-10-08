import pygame
import random
from funcoes import calcula_tempo

# determina padronização de tamanho p/ altura e largura de tds as janelas do jogo e necessidade de preenchimento de cor 
class Telas:
    def __init__(self, cor):
        self.cor = cor
        self.altura = 800
        self.largura = 1000

    def desenha(self, window):
        window.fill(self.cor) 
        # n tem display.uptade() pq é só o preenchimento inicial das telas


# classe filha da Tela 
class Tela_Inicial(Telas):
    def __init__(self):
        super().__init__((36, 71, 107)) # determina cor de preenchimento da tela

        self.titulo = pygame.font.Font('assets/font/PressStart2P.ttf', 40) # pygame.font.Font('link', tam.) --> carrega texto

    def desenha_inicio (self, window):
        self.desenha(window)

        titulo = self.titulo.render("Jogo da Navinha", True, (164, 106, 69)) # texto.render --> permite a disposição do texto como 'imagem'
        posicao = titulo.get_rect(center=(self.largura // 2, self.altura // 2))
        window.blit(titulo, posicao) # window.blit('img', pos) --> dispõe imagem na janela 
        pygame.display.update() # carega mudanças feitas no desenho da tela


# classe filha da Tela
class Tela_GameOver(Telas):
    def __init__(self):
        super().__init__((36, 71, 107))

        self.titulo = pygame.font.Font('assets/font/PressStart2P.ttf', 40)

        self.record = 0 
        self.texto_record = pygame.font.Font('assets/font/PressStart2P.ttf', 20)
    
    def desenha_game_over (self, window):
        self.desenha(window)

        titulo = self.titulo.render("Game Over", True, (134, 43, 53))
        posicao = titulo.get_rect(center=(self.largura // 2, self.altura // 2))
        window.blit(titulo, posicao)

        record = self.texto_record.render(f"Recorde: {self.record}", True, (164, 106, 69))
        posicao_record = record.get_rect(center=(self.largura // 2, self.altura // 2 + 75))
        window.blit(record, posicao_record)
        pygame.display.update()


# determina características inerentes ao elemento nave
# classe filha da classe Sprite do pygame --> atributos image e rect
class Nave(pygame.sprite.Sprite):
    def __init__(self, velocidade_nave, posicao_nave):
        super().__init__()

        nave = pygame.image.load('assets/img/playerShip1_orange.png') # pygame.image.load('link') --> carrega imagem
        self.image = pygame.transform.scale(nave, (50, 40)) # self.image --> atributo image | pygame.transform.scale --> ajustar tamanho
        self.rect = self.image.get_rect() # self.rect --> atributo rect | .get_rect() --> criar um retangulo que 'envolve' imagem

        # atributos de velocidade e posicao
        self.velocidade_nave = velocidade_nave
        self.rect.midbottom = posicao_nave # self.rect.midbottom --> pega o atributo rect e estabelece sua posicao no centro inferior da tela

    def desenha_nave(self, window):
        window.blit(self.image, self.rect)


    def movimento_nave(self, delta_t):
        teclas = pygame.key.get_pressed()
                
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            y = self.rect.y + self.velocidade_nave[1]*delta_t # coordenadas x e y são inerentes à atributo rect 
            if y + self.rect.height >= 800:
                y = 800 - self.rect.height # atribuições height e width são inerentes à atributo rect
            self.rect.y = y
    
        elif teclas[pygame.K_UP] or teclas[pygame.K_w]:
            y = self.rect.y - self.velocidade_nave[1]*delta_t
            if y < 0:
                y = 800 - self.rect.height # nave volta para o início da tela quando atinge seu limite superior
            self.rect.y = y
    
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            x = self.rect.x + self.velocidade_nave[0]*delta_t
            if x + self.rect.width >= 1000:
                x = 1000 - self.rect.width
            self.rect.x = x
        
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            x = self.rect.x - self.velocidade_nave[0]*delta_t
            if x < 0:
                x = 0
            self.rect.x = x


# determina características inerentes ao elemento meteoro
# classe filha da classe Sprite do pygame --> atributos image e rect
class Meteoro(pygame.sprite.Sprite):
    def __init__(self, velocidade_meteoro, posicao_meteoro):
        super().__init__()

        self.image = pygame.image.load('assets/img/meteorBrown_med1.png')
        self.rect = self.image.get_rect()

        self.velocidade_meteoro = velocidade_meteoro
        self.rect.topleft = posicao_meteoro

    def movimento_meteoro(self, delta_t):
        y = self.rect.y + delta_t*self.velocidade_meteoro

        if y >= 800:
            y = random.randint(-500, -50)
            self.rect.x = random.randint(0, 1000 - self.rect.width) 
        
        self.rect.y = y


# determina características inerentes ao elemento tiro
# classe filha da classe Sprite do pygame --> atributos image e rect
class Tiro(pygame.sprite.Sprite):
    def __init__(self, velocidade_tiro, posicao_tiro):
        super().__init__()

        tiro = pygame.image.load('assets/img/laserRed16.png')
        self.image = pygame.transform.scale(tiro, (10, 10))
        self.rect = self.image.get_rect()

        self.velocidade_tiro = velocidade_tiro
        self.rect.midbottom = posicao_tiro

    def desenha_tiro(self, window):
        window.blit(self.image, self.rect)

    def movimento_tiro(self, delta_t):
        self.rect.y = self.rect.y - delta_t*self.velocidade_tiro


# determina características inerentes à animação de explosão
# classe filha da classe Sprite do pygame --> atributos image e rect
class Explosao(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()

        self.imagens = [] # cria lista com todas as imagens necessárias para reprdução da animação de explosão
        for i in range(9):
            self.imagens.append(pygame.image.load(f'assets/img/regularExplosion{i:02d}.png'))

        self.indice = 0
        self.tempo = 0
        self.duracao = 0.05 # duração de cada frame da explosão
        self.image = self.imagens[0] # determina a imagem mostrada no momento
        self.rect = self.image.get_rect(center=posicao)

    def atualiza_explosao(self, delta_t):
        self.tempo += delta_t 

        while self.tempo >= self.duracao: # analisa o tempo decorrido a cada loop do jogo e encaixa a explosão no tempo que a cabe
            self.tempo -= self.duracao
            self.indice += 1

            if self.indice >= len(self.imagens):
                self.kill() # remove a explosão do sprite.Group() que a contiver, impeindo a continuidade da animação, uma vez terminada 
                return

            self.image = self.imagens[self.indice] 


# determina características inerentes ao sistema de pontuação
# classe filha da classe Sprite do pygame --> atributos image e rect
class Pontuacao(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.pontuacao = 0
        self.tempo = 0

    def atualiza_pontuacao_tempo(self, delta_t):
        self.tempo += delta_t 

        while self.tempo >= 1:
            self.tempo -= 1
            self.pontuacao += 1 # jogador ganha 1 ponto a cada segundo mque sobrevive

    def atualiza_pontuacao_meteoro(self):
        self.pontuacao += 3 # jogador ganha 3 pontos por meteoro que destroi


# classe filha da Tela
class Tela_Jogo(Telas):
    def __init__(self, vidas_max, vidas, qtd_meteoros):
        super().__init__((0, 0, 0))

        self.vidas_max = vidas_max
        self.vidas = vidas

        fundo = pygame.image.load('assets/img/starfield.png')
        self.fundo = pygame.transform.scale(fundo, (1000, 800))

        self.estrelas = []
        for i in range(41):
            x = random.randint(0, 1000)
            y = random.randint(0, 800)
            r = random.randint(1, 5)
            self.estrelas.append((x, y, r))

        self.nave = Nave([200, 155], (500, 800))

        self.coracoes = pygame.font.Font('assets/font/PressStart2P.ttf', 20)

        self.fonte_fps = pygame.font.Font('assets/font/PressStart2P.ttf', 10)

        self.tiros = pygame.sprite.Group() # criação de sprite.Group() p/ tiros p/ que sejam desenhados apenas a partir do momento em que existam

        self.explosao = pygame.sprite.Group() 

        self.placar = Pontuacao()
        self.fonte_pontuacao = pygame.font.Font('assets/font/PressStart2P.ttf', 10)

        self.meteoros = pygame.sprite.Group() # criação de sprite.Group() p/ meteoros p/ favcilitar armanezamento de características e desenho 
        for i in range(qtd_meteoros):
            x = random.randint(0, 1000)
            y = random.randint(0, 800)
            meteoro = Meteoro(200, [x, y])
            self.meteoros.add(meteoro)

    def desenha_jogo(self, window, fps):
        self.desenha(window)
        window.blit(self.fundo, (0, 0))

        for estrela in self.estrelas:
            pygame.draw.circle(window, (255, 255, 255), (estrela[0], estrela[1]), estrela[2]) # .draw.circle --> recebe window, cor, coordenadas do centro e raio

        self.meteoros.draw(window)

        self.nave.desenha_nave(window)

        for tiro in self.tiros:
            tiro.desenha_tiro(window)

        self.explosao.draw(window)

        coracoes_vidas = self.coracoes.render(chr(9829) * self.vidas, True, (255, 0, 0)) # chr(9829) * self.vidas --> carrega corções em qtd definida
        window.blit(coracoes_vidas, (0, 0))

        coracoes_perdas = self.coracoes.render(chr(9829) * (self.vidas_max - self.vidas), True, (255, 255, 255))
        window.blit(coracoes_perdas, (coracoes_vidas.get_width(), 0))

        texto_fps = self.fonte_fps.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
        x_fps = window.get_width() - texto_fps.get_width()
        window.blit(texto_fps, (x_fps, 0))

        pontuacao = self.fonte_pontuacao.render(f'Pontuação: {self.placar.pontuacao} ', True, (255, 255, 255)) # self.placar.pontuacao --> pega pontuacao atualizada
        window.blit(pontuacao, (0, 30))

        pygame.display.update()


class Jogo:
    def __init__(self):
        pygame.init()

        self.altura = 800
        self.largura = 1000
        self.window = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Jogo da Julia')
        
        self.tela_jogo = Tela_Jogo(3, 3, 18)
        self.tela_inicial = Tela_Inicial()
        self.tela_game_over = Tela_GameOver()
        self.tela_atual = "inicio"

        pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg') # .mixer.music.load('link') --> carrega musica
        self.musica = False

        self.som_tiro = pygame.mixer.Sound('assets/snd/pew.wav') #.mixer.Sound('link') --> carrega sons

        self.t0 = pygame.time.get_ticks() # .time.get.ticks() pega tempo entre frames
        self.fps = 0 # fps inicial

        self.nave = self.tela_jogo.nave
        self.grupo_nave = pygame.sprite.Group(self.nave) # cria sprite.Group p/ a nave para verificação de colisões

        self.meteoros = self.tela_jogo.meteoros # pega os parametros definidos na tela_jogo p/ n criar outros elementos aleatórios

        self.grupo_tiro = self.tela_jogo.tiros

        self.explosoes = self.tela_jogo.explosao


    def verifica_colisoes(self):
        colisoes_nave = pygame.sprite.groupcollide(self.meteoros, self.grupo_nave, False, False) # .sprite.groupcollide verifica colisão entre sprite.Group's; boleanos recebidos determinam se é para apagar ou não os elementos que colidiram
        colisoes_tiro = pygame.sprite.groupcollide(self.meteoros, self.grupo_tiro, True, True)

        if colisoes_nave:
            self.tela_jogo.vidas -= 1
            if self.tela_jogo.vidas <= 0:
                if self.tela_jogo.placar.pontuacao > self.tela_game_over.record: # verifica se pontuação final da partida é meior do que record estabelecido na tela de game-over
                    self.tela_game_over.record = self.tela_jogo.placar.pontuacao
                self.tela_atual = "game_over"
            
            for meteoro in colisoes_nave: # determina qual meteoro do sprite.Group colidiu com a nave
                meteoro.rect.x = random.randint(0, 1000 - meteoro.rect.width)
                meteoro.rect.y = random.randint(-500, -50)

        if colisoes_tiro:
            for meteoro in colisoes_tiro:
                self.tela_jogo.placar.atualiza_pontuacao_meteoro() # determina aumento de pontuação em caso de colisão do tiro com meteoro
                self.explosoes.add(Explosao(meteoro.rect.center)) #adiciona explosão ao sprite.Group e permite seu desenho

                x = random.randint(0, 1000 - meteoro.rect.width)
                y = random.randint(-500, -50)
                self.meteoros.add(Meteoro(200, [x, y])) # cria novo meteoro p/ suprir ausência do anterior

    def atualiza_estado(self):
        self.t0, delta_t, self.fps = calcula_tempo(self.t0) # calcula fps eretorna novo t0, delta_t e fps

        if not self.musica:
            pygame.mixer.music.play() # toca música
            self.musica = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False 

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tiro = Tiro(200, self.nave.rect.midtop)
                    self.grupo_tiro.add(tiro) #adiciona tiro ao seu sprite.Group, permitindo seu desenho
                    self.som_tiro.play() # toca som do tiro

        # pega o delta_t determinado pela função de cálculo de tempo e aplica como parâmetro p/ atualização do estado dos componentes do jogo necessários
        self.nave.movimento_nave(delta_t)

        for meteoro in self.meteoros:
            meteoro.movimento_meteoro(delta_t)
        
        for tiro in self.grupo_tiro:
            tiro.movimento_tiro(delta_t)

        for explosao in self.explosoes:
            explosao.atualiza_explosao(delta_t)

        self.tela_jogo.placar.atualiza_pontuacao_tempo(delta_t)

        self.verifica_colisoes()
        
        return True

    def game_loop(self):
        rodando = True

        while rodando:
            if self.tela_atual == "inicio":
                self.tela_inicial.desenha_inicio(self.window)

            elif self.tela_atual == "jogando":
                self.tela_jogo.desenha_jogo(self.window, self.fps)
                rodando = self.atualiza_estado()

            elif self.tela_atual == "game_over":
                self.tela_game_over.desenha_game_over(self.window)

            if self.tela_atual != "jogando":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        rodando = False

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if self.tela_atual == "inicio":
                            self.t0 = pygame.time.get_ticks() # reinicia o t0 a cada rodagem do jogo
                            self.tela_atual = "jogando"

                        elif self.tela_atual == "game_over":
                            self.tela_jogo = Tela_Jogo(3, 3, 18) # reinicia elementos da tela inicial
                            self.nave = self.tela_jogo.nave # reinicia estados dos elemntos que fazem parte do jogo
                            self.meteoros = self.tela_jogo.meteoros
                            self.grupo_tiro = self.tela_jogo.tiros
                            self.explosoes = self.tela_jogo.explosao
                            self.grupo_nave = pygame.sprite.Group(self.nave) # recria sprite.Group da nave
                            self.tela_atual = "inicio"

        pygame.quit()








