import pygame
from funcoes import inicializa
from funcoes import recebe_eventos
from funcoes import desenha 
from funcoes import game_loop

janela = inicializa()
recebe_eventos()
desenha(janela)
game_loop(janela)

