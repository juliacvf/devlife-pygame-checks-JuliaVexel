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

    assets['coracoes'] = pygame.font.Font('assets/font/PressStart2P.ttf', 20)

    state = {
        'nave_pos': [135, 200],
        'nave_vel': [100, 100],
        't0': 0,
        'fps': 0
    }

    assets['fps'] = pygame.font.Font('assets/font/PressStart2P.ttf', 10)

    return janela, assets, state

def atualiza_estado(state):
    game = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False 
            break

    t0 = state['t0']
    t1 = pygame.time.get_ticks()
    if t1 - t0 > 0:
        fps = 1000/(t1-t0)
        state['fps'] = fps

    state['t0'] = t1
    return game 

def desenha(janela, assets, state):
    janela.fill((0, 0, 0))

    janela.blit(assets['fundo'], (0, 0))
    janela.blit(assets['nave'], state['nave_pos'])

    branco = (255, 255, 255)
    for estrela in assets['estrelas']:
        pygame.draw.circle(janela, branco, (estrela[0], estrela[1]), estrela[2])

    coracoes = assets['coracoes'].render(chr(9829) * 3, True, (255, 0, 0))
    janela.blit(coracoes, (0,0))

    fps = assets['fps'].render(f"FPS: {state['fps']:.2f}", True, (255,255,255))
    x_fps = janela.get_width() - fps.get_width()
    janela.blit(fps, (x_fps,0))

    
    pygame.display.update()

    return janela

def game_loop(janela, assets, state):
    while atualiza_estado(state):
        desenha(janela, assets, state)

if __name__ == '__main__':
    janela, assets, state = inicializa()
    game_loop(janela, assets, state)
    pygame.quit()