import pygame
import random
from funcoes import calcula_tempo

class Telas:
    def __init__(self, cor):
        self.altura = 800
        self.largura = 1000
        self.cor = cor

    def desenha(self, window):
        window.fill(self.cor)


class Tela_Inicial(Telas):
    def __init__(self):
        super().__init__((36, 71, 107))

        self.titulo = pygame.font.Font('assets/font/PressStart2P.ttf', 40)

    def desenha_inicio (self, window):
        self.desenha(window)

        titulo = self.titulo.render("Jogo da Navinha", True, (164, 106, 69))
        posicao = titulo.get_rect(center=(self.largura // 2, self.altura // 2))
        window.blit(titulo, posicao)
        pygame.display.update()


class Tela_GameOver(Telas):
    def __init__(self):
        super().__init__((36, 71, 107))

        self.titulo = pygame.font.Font('assets/font/PressStart2P.ttf', 40)
    
    def desenha_game_over (self, window):
        self.desenha(window)

        titulo = self.titulo.render("Game Over", True, (134, 43, 53))
        posicao = titulo.get_rect(center=(self.largura // 2, self.altura // 2))
        window.blit(titulo, posicao)
        pygame.display.update()


class Nave(pygame.sprite.Sprite):
    def __init__(self, velocidade_nave, posicao_nave):
        super().__init__()

        nave = pygame.image.load('assets/img/playerShip1_orange.png')
        self.image = pygame.transform.scale(nave, (50, 40))
        self.rect = self.image.get_rect()

        self.velocidade_nave = velocidade_nave
        self.rect.midbottom = posicao_nave

    def movimento_nave(self, delta_t):
        teclas = pygame.key.get_pressed()
                
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            y = self.rect.y + self.velocidade_nave[1]*delta_t
            if y + 40 >= 800:
                y = 760
            self.rect.y = y
    
        elif teclas[pygame.K_UP] or teclas[pygame.K_w]:
            y = self.rect.y - self.velocidade_nave[1]*delta_t
            if y < 0:
                y = 760
            self.rect.y = y
    
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            x = self.rect.x + self.velocidade_nave[0]*delta_t
            if x + 50 >= 1000:
                x = 950
            self.rect.x = x
        
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            x = self.rect.x - self.velocidade_nave[0]*delta_t
            if x < 0:
                x = 0
            self.rect.x = x


class Meteoro(pygame.sprite.Sprite):
    def __init__(self, velocidade_meteoro, posicao_meteoro):
        super().__init__()

        self.image = pygame.image.load('assets/img/meteorBrown_med1.png')
        self.rect = self.image.get_rect()

        self.velocidade_meteoro = velocidade_meteoro
        self.rect.topleft = posicao_meteoro

    def movimento_meteoro(self, delta_t):
        ym = self.rect.y + delta_t * self.velocidade_meteoro

        if ym >= 800:
            ym = random.randint(-500, -50)
            self.rect.x = random.randint(0, 1000 - self.rect.width) 
        
        self.rect.y = ym


class Tiro(pygame.sprite.Sprite):
    def __init__(self, velocidade_tiro, posicao_tiro):
        super().__init__()

        tiro = pygame.image.load('assets/img/laserRed16.png')
        self.image = pygame.transform.scale(tiro, (10, 10))
        self.rect = self.image.get_rect()

        self.velocidade_tiro = velocidade_tiro
        self.rect.midbottom = posicao_tiro

    def movimento_tiro(self, delta_t):
        self.rect.y = self.rect.y - delta_t * self.velocidade_tiro

class Explosao(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()

        self.imagens = []
        for i in range(9):
            self.imagens.append(pygame.image.load(f'assets/img/regularExplosion{i:02d}.png'))

        self.indice = 0
        self.tempo = 0
        self.duracao = 0.06
        self.image = self.imagens[0]
        self.rect = self.image.get_rect(center=posicao)

    def atualiza_explosao(self, delta_t):
        self.tempo += delta_t

        while self.tempo >= self.duracao:
            self.tempo -= self.duracao
            self.indice += 1

            if self.indice >= len(self.imagens):
                self.kill()
                return

            self.image = self.imagens[self.indice]
            
        
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

        self.coracoes = pygame.font.Font('assets/font/PressStart2P.ttf', 20)
        self.fonte_fps = pygame.font.Font('assets/font/PressStart2P.ttf', 10)

        self.nave = Nave([200, 155], (500, 800))

        self.tiros = pygame.sprite.Group()

        self.explosao = pygame.sprite.Group()

        self.meteoros = pygame.sprite.Group()
        for i in range(qtd_meteoros):
            x = random.randint(0, 1000)
            y = random.randint(0, 800)
            meteoro = Meteoro(200, [x, y])
            self.meteoros.add(meteoro)

    def desenha_jogo(self, window, fps):
        self.desenha(window)
        window.blit(self.fundo, (0, 0))

        for estrela in self.estrelas:
            pygame.draw.circle(window, (255, 255, 255), (estrela[0], estrela[1]), estrela[2])

        self.meteoros.draw(window)

        window.blit(self.nave.image, self.nave.rect)

        self.tiros.draw(window)

        self.explosao.draw(window)

        coracoes_vidas = self.coracoes.render(chr(9829) * self.vidas, True, (255, 0, 0))
        window.blit(coracoes_vidas, (0, 0))

        coracoes_perdas = self.coracoes.render(chr(9829) * (self.vidas_max - self.vidas), True, (255, 255, 255))
        window.blit(coracoes_perdas, (coracoes_vidas.get_width(), 0))

        texto_fps = self.fonte_fps.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
        x_fps = window.get_width() - texto_fps.get_width()
        window.blit(texto_fps, (x_fps, 0))


class Jogo:
    def __init__(self):
        pygame.init()

        self.altura = 800
        self.largura = 1000
        self.window = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Jogo da Julia')

        pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg')
        self.musica = False

        self.som_tiro = pygame.mixer.Sound('assets/snd/pew.wav')

        self.t0 = pygame.time.get_ticks()
        self.fps = 0

        self.tela_jogo = Tela_Jogo(3, 3, 18)
        self.tela_inicial = Tela_Inicial()
        self.tela_game_over = Tela_GameOver()
        self.tela_atual = "inicio"

        self.nave = self.tela_jogo.nave
        self.grupo_nave = pygame.sprite.Group(self.nave)

        self.meteoros = self.tela_jogo.meteoros

        self.grupo_tiro = self.tela_jogo.tiros

        self.explosoes = self.tela_jogo.explosao

    def verifica_colisoes(self):
        colisoes_nave = pygame.sprite.groupcollide(self.meteoros, self.grupo_nave, False, False)
        colisoes_tiro = pygame.sprite.groupcollide(self.meteoros, self.grupo_tiro, True, True)

        if colisoes_nave:
            self.tela_jogo.vidas -= 1
            if self.tela_jogo.vidas <= 0:
                self.tela_atual = "game_over"
            
            for meteoro in colisoes_nave:
                meteoro.rect.x = random.randint(0, 1000 - meteoro.rect.width)
                meteoro.rect.y = random.randint(-500, -50)

        if colisoes_tiro:
            for meteoro in colisoes_tiro:
                self.explosoes.add(Explosao(meteoro.rect.center))

                x = random.randint(0, 1000 - meteoro.rect.width)
                y = random.randint(-500, -50)
                self.meteoros.add(Meteoro(200, [x, y]))

    def atualiza_estado(self):
        self.t0, delta_t, self.fps = calcula_tempo(self.t0)

        if not self.musica:
            pygame.mixer.music.play()
            self.musica = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False 

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tiro = Tiro(200, self.nave.rect.midtop)
                    self.grupo_tiro.add(tiro)
                    self.som_tiro.play()

        self.nave.movimento_nave(delta_t)

        for meteoro in self.meteoros:
            meteoro.movimento_meteoro(delta_t)
        
        for tiro in self.grupo_tiro:
            tiro.movimento_tiro(delta_t)

        for explosao in self.explosoes:
            explosao.atualiza_explosao(delta_t)

        self.verifica_colisoes()
        
        return True

    def game_loop(self):
        rodando = True

        while rodando:
            if self.tela_atual == "inicio":
                self.tela_inicial.desenha_inicio(self.window)

            elif self.tela_atual == "jogando":
                self.tela_jogo.desenha_jogo(self.window, self.fps)
                pygame.display.update()
                rodando = self.atualiza_estado()

            elif self.tela_atual == "game_over":
                self.tela_game_over.desenha_game_over(self.window)

            if self.tela_atual != "jogando":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        rodando = False

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if self.tela_atual == "inicio":
                            self.t0 = pygame.time.get_ticks()
                            self.tela_atual = "jogando"

                        elif self.tela_atual == "game_over":
                            self.tela_jogo = Tela_Jogo(3, 3, 18)
                            self.nave = self.tela_jogo.nave
                            self.meteoros = self.tela_jogo.meteoros
                            self.grupo_tiro = self.tela_jogo.tiros
                            self.explosoes = self.tela_jogo.explosao
                            self.grupo_nave = pygame.sprite.Group(self.nave)
                            self.tela_atual = "inicio"

        pygame.quit()








