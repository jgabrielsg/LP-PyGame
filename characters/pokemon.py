import math
import pygame
import random
import math

class Pokemon:
    pokemon_list = []

    def __init__(self,img_path, nome, tipo, xp, nivel, velocidade, ataque, defesa, hp, posx, posy, visible):
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (90, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)
        self.nome = nome
        self.tipo = tipo
        self.nivel = nivel
        self.xp = xp
        self.velocidade = velocidade
        self.ataque = ataque
        self.defesa = defesa
        self.hp = hp
        self.ultimo_movimento = 3
        self.dx = random.randrange(-1,1)
        self.dy = random.randrange(-1,1)
        self.visible = visible

        Pokemon.pokemon_list.append(self)


    def atacar(self, alvo):
        dano = self.ataque - alvo.defesa
        if dano > 0:
            alvo.hp -= dano

    def update(self, dt, SCREEN, SCREEN_WIDTH,SCREEN_HEIGHT):
        #Movimentação do pokemon
        self.ultimo_movimento += dt
        if self.rect.x >= SCREEN_WIDTH or self.rect.y >= SCREEN_HEIGHT or self.rect.x <= 0 or self.rect.y <=0:
            self.dx = -1*self.dx
            self.dy = -1*self.dy
            self.ultimo_movimento = 0
        if self.ultimo_movimento >= 2:
            self.dx = random.randrange(-1,1)
            self.dy = random.randrange(-1,1)
            self.ultimo_movimento = 0
        self.rect.x += self.dx*5
        self.rect.y += self.dy*5

        #Atualiza a imagem do pokemon ao andar
        if self.visible:
            SCREEN.blit(self.image, self.rect)

    def nivel_up(self):
        self.nivel += 1
        self.ataque = math.floor(self.ataque*1.1)
        self.defesa = math.floor(self.defesa*1.1)
        self.hp = math.floor(self.hp*1.1)
        self.velocidade = math.floor(self.velocidade*1.1)

    def ganhar_xp(self, xp_inimigo):
        # Calcular a quantidade de XP com base no nível do inimigo
        xp_ganho = math.floor(xp_inimigo * 0.2)

        # Adicionar o XP ganho ao XP atual do Pokémon
        self.xp += xp_ganho

    def status(self):
        print(f"Nome: {self.nome}")
        print(f"Tipo: {self.tipo}")
        print(f"Nível: {self.nivel}")
        print(f"Velocidade: {self.velocidade}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"HP: {self.hp}")
