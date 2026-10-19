# Estudo Pygame - Jogo da Navinha

Este é um projeto desenvolvido na disciplina Developer Life, do 1° semestre do curso de Ciência da Computação do Insper. O intuito deste projeto é aprender e praticar o uso da biblioteca Pygame para o desenvolvimento de jogos 2D usando Python.

## Descrição do jogo

Controle uma nave em meio a uma chuva de meteoros no espaço sideral. 
Desvie dos obstáculos, destrua os meteoros com seus tiros e sobreviva pelo maior tempo possível.

## Como jogar

Para jogar, é necessário ter o Python 3 instalado na máquina. Além disso, você deve instalar a biblioteca pygame com o comando:

```
pip install pygame
```

Após instalar a biblioteca, clone este repositório e execute o arquivo jogo.py, dentro da pasta codigo. O jogo será aberto em uma nova janela e pode ser jogado com as seguintes teclas:

Na tela inicial, pressione espaço para iniciar o jogo. Na tela de game over, pressione espaço para retornar para a tela inicial.

Utilize as setas ou as teclas a/w/s/d para controlar a nave e a tecla de espaço para disparar os tiros.


## Prova de pygame:

NO INÌCIO:

def atualiza_estado():
    game = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False 
            break
    return game 

def game_loop(window):
    while atualiza_estado():
        desenha(window)


RODAR O JOGO:

import pygame
from funcoes import inicializa
from funcoes import game_loop

window = inicializa()
game_loop(window)
pygame.quit()


COLISOES COM PONTO:

if event.type == pygame.MOUSEBUTTONDOWN:
    if event.button == 1:
        ponto_x, ponto_y = event.pos

def colisao_ponto_circulo(ponto_x, ponto_y, circulo_x, circulo_y, circulo_raio):
    d = ((circulo_x - ponto_x)**2 + (circulo_y - ponto_y)**2)**0.5

    if d <= circulo_raio:
        return True
    else:
        return False 

def colisao_ponto_retangulo(ponto_x, ponto_y, rect_x, rect_y, rect_w, rect_h):
    if (
        rect_x <= ponto_x and 
        ponto_x <= rect_x + rect_w and 
        rect_y <= ponto_y and 
        ponto_y <= rect_y + rect_h
    ):
        return True
    else:
        return False


COLISÕES ENTRE FORMAS:

def colisao_circulos(c1_x, c1_y, c2_x, c2_y, c1_raio, c2_raio)
    distancia_centros = ((cx1 - cx2)**2 + (cy1 - cy2)**2)**0.5
    if distancia_centros <= raio1 + raio2:
        return True
    else:
        return False

def colisao_retangulos(x1, y1, x2, y2, largura1, altura1, largura2, altura2):
    if (
    x1 < x2 + largura2 and
    x1 + largura1 > x2 and
    y1 < y2 + altura2 and
    altura1 + y1 > y2
):
        return True
    else:
        return False