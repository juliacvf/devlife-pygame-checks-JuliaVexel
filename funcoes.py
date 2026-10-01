import pygame
import random 

def inicializa():
    pygame.init()
    
    janela = pygame.display.set_mode((320, 240))
    pygame.display.set_caption("Jogo da Julia")
    
    assets = {}
    assets['fundo'] = pygame.image.load('assets/img/starfield.png')
    nave = pygame.image.load('assets/img/playerShip1_orange.png')
    assets['nave'] = pygame.transform.scale(nave, (50, 40))

    assets['estrelas'] = []
    for i in range(16):
        x = random.randint(0,320)
        y = random.randint(0, 240)
        r = random.randint(1, 5)
        assets['estrelas'].append((x, y, r))

    return janela, assets

def recebe_eventos():
    game = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False 
            break

    return game 

def desenha(janela, assets):
    janela.fill((0, 0, 0))

    janela.blit(assets['fundo'], (0, 0))
    janela.blit(assets['nave'], (135, 200))

    branco = (255, 255, 255)
    for estrela in assets['estrelas']:
        pygame.draw.circle(janela, branco, (estrela[0], estrela[1]), estrela[2])
    
    pygame.display.update()

    return janela

def game_loop(janela, assets):
    while recebe_eventos():
        desenha(janela, assets)

if __name__ == '__main__':
    janela, assets = inicializa()
    game_loop(janela, assets)
    pygame.quit()