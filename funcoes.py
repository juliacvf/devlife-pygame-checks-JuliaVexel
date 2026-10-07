import pygame 

def calcula_tempo(t0):
    t1 = pygame.time.get_ticks()
    intervalo = t1 - t0

    fps = 0
    if intervalo > 0:
        fps = 1000 / intervalo

    delta_t = intervalo / 1000

    return t1, delta_t, fps