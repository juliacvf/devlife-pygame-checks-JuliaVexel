import pygame
import random 

def inicializa():
    pygame.init()
    
    janela = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Jogo da Julia")
    
    assets = {}
    fundo = pygame.image.load('assets/img/starfield.png')
    assets['fundo'] = pygame.transform.scale(fundo, (1000, 800))
    nave = pygame.image.load('assets/img/playerShip1_orange.png')
    assets['nave'] = pygame.transform.scale(nave, (50, 40))

    pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg')
    assets['musica'] = False

    tiro = pygame.mixer.Sound('assets/snd/pew.wav')
    assets['tiro'] = tiro

    assets['estrelas'] = []
    for i in range(41):
        x = random.randint(0,1000)
        y = random.randint(0, 800)
        r = random.randint(1, 5)
        assets['estrelas'].append((x, y, r))

    assets['coracoes'] = pygame.font.Font('assets/font/PressStart2P.ttf', 20)

    state = {
        'nave_pos': [500, 760],
        'nave_vel': [200, 155],
        'vidas': 3,
        't0': 0,
        'fps': 0
    }

    assets['fps'] = pygame.font.Font('assets/font/PressStart2P.ttf', 10)

    meteoros = pygame.image.load('assets/img/meteorBrown_med1.png')
    assets['meteoros'] = pygame.transform.scale(meteoros, (25,15))
    state['pos_meteoros'] = []
    for i in range(18):
        x = random.randint(0,1000)
        y = random.randint(0, 800)
        state['pos_meteoros'].append([x, y])

    state['vel_meteoros'] = 200
    
        

    return janela, assets, state

def atualiza_estado(state, assets):
    game = True
    t0 = state['t0']
    t1 = pygame.time.get_ticks()
    if t1 - t0 > 0:
        fps = 1000/(t1-t0)
        state['fps'] = fps

    delta_t = (t1-t0)/1000
    state['t0'] = t1

    if assets['musica'] == False:
        pygame.mixer.music.play()
        assets['musica'] = True

    for meteoro in state['pos_meteoros']:
        ym = meteoro[1] + delta_t * state['vel_meteoros']

        if ym >= 800:
            ym = random.randint(-500, -50)

            meteoro[0] = random.randint(0, 950) 
        
        meteoro[1] = ym

        rect_meteoro = pygame.Rect(meteoro[0], meteoro[1], 25, 15)
        rect_nave = pygame.Rect(state['nave_pos'][0], state['nave_pos'][1], 50, 40)

        if rect_nave.colliderect(rect_meteoro):
            state['vidas'] -= 1
            if state['vidas'] <= 0:
                game = False 
                break

            meteoro[0] = random.randint(0, 950)
            meteoro[1] = random.randint(-500, -50)


    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            game = False 
            break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                assets['tiro'].play()

        
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        y = state['nave_pos'][1] + state['nave_vel'][1]*delta_t
        if y + 40 >= 800:
            y = 760
        state['nave_pos'][1] = y

    elif teclas[pygame.K_UP] or teclas[pygame.K_w]:
        y = state['nave_pos'][1] - state['nave_vel'][1]*delta_t
        if y < 0:
            y = 760
        state['nave_pos'][1] = y

    elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        x = state['nave_pos'][0] + state['nave_vel'][0]*delta_t
        if x + 50 >= 1000:
            x = 950
        state['nave_pos'][0] = x
    
    elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        x = state['nave_pos'][0] - state['nave_vel'][0]*delta_t
        if x < 0:
            x = 0
        state['nave_pos'][0] = x

    return game 


def desenha(janela, assets, state):
    janela.fill((0, 0, 0))

    janela.blit(assets['fundo'], (0, 0))
    
    branco = (255, 255, 255)
    for estrela in assets['estrelas']:
        pygame.draw.circle(janela, branco, (estrela[0], estrela[1]), estrela[2])
    
    janela.blit(assets['nave'], state['nave_pos'])

    coracoes_vidas = assets['coracoes'].render(chr(9829) * state['vidas'], True, (255, 0, 0))
    janela.blit(coracoes_vidas, (0,0))

    coracoes_perdas = assets['coracoes'].render(chr(9829) * (3-state['vidas']), True, (255, 255, 255))
    janela.blit(coracoes_perdas, (coracoes_vidas.get_width(), 0))
    

    fps = assets['fps'].render(f"FPS: {state['fps']:.2f}", True, (255,255,255))
    x_fps = janela.get_width() - fps.get_width()
    janela.blit(fps, (x_fps,0))

    for meteoro in state['pos_meteoros']:
        janela.blit(assets['meteoros'], meteoro)
    
    pygame.display.update()

    return janela

def game_loop(janela, assets, state):
    while atualiza_estado(state, assets):
        desenha(janela, assets, state)

if __name__ == '__main__':
    janela, assets, state = inicializa()
    game_loop(janela, assets, state)
    pygame.quit()