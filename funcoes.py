import pygame

def inicializa():
    pygame.init()
    janela = pygame.display.set_mode((320, 240))
    pygame.display.set_caption("Jogo da Julia")

    return janela 

def recebe_eventos():
    game = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False 
            break

    return game 

def desenha(janela):
    janela.fill((0, 0, 0))
    pygame.display.update()

    return janela

def game_loop(janela):
    while recebe_eventos():
        desenha(janela)