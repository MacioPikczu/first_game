import sys

import pygame
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'island.settings')
django.setup()

from os.path import join
from random import randint, uniform
from account.models import User, RESOURCE, Resource, Statistics
from datetime import datetime


# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('digging')
running = True
clock = pygame.time.Clock()
game_time = 5 #s

#################
# USER LOGGED
def userLogged(username):
    id = User.objects.get(username=username).id
    return id
#################

# imports
images_location = '../island/static/images'
stone_ore_surf = pygame.transform.rotozoom(pygame.image.load(join(images_location, 'stone_ore.png')).convert_alpha(), 0, 0.8)
metal_ore_surf = pygame.transform.rotozoom(pygame.image.load(join(images_location, 'metal_ore.png')).convert_alpha(), 0, 0.7)
sulfur_ore_surf = pygame.transform.rotozoom(pygame.image.load(join(images_location, 'sulfur_ore.png')).convert_alpha(), 0, 0.5)
font = pygame.font.Font(join(images_location, 'Oxanium-Bold.ttf'), 40)
target_point_image = pygame.image.load(join(images_location, 'target.png')).convert_alpha()
target_point_rect = target_point_image.get_frect(center=(target_point_image.width / 2, target_point_image.height / 2))

# global variables
stone_ore = 0
sulfur_ore = 0
logged = False
user_logged = 'macius'

resources_list = []
for each in RESOURCE:
    resources_list.append(each[1])
resources = (stone_ore, sulfur_ore)

# saving on host
API_URL = 'http://127.0.0.1:8000/api/get_authenticated_user'

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.hit_animation_images = [pygame.image.load(join(images_location, 'hit', f'pickaxe_{i}.png')).convert_alpha() for i in range(8)]
        self.frame_index = 0
        self.image = pygame.image.load(join('static/images/hit', 'pickaxe_1.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))


        # cooldown
        self.can_hit = True
        self.pickaxe_hit_time = 0
        self.cooldown_duration = 1000
        self.pickaxe_animation_delay = 0

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def hit_timer(self):
        if not self.can_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.pickaxe_hit_time >= self.cooldown_duration:
                self.can_hit = True
        return self.can_hit

    def hit_animation(self):
        current_time = pygame.time.get_ticks()
        animation_delay = self.cooldown_duration / len(self.hit_animation_images)
        if self.can_hit:
            player.image = self.hit_animation_images[0]
            self.frame_index = 0
        else:
            if current_time - self.pickaxe_hit_time >= animation_delay * self.frame_index and self.frame_index < len(self.hit_animation_images) - 1:
                self.frame_index += 1
                player.image = self.hit_animation_images[self.frame_index]


    def update(self, dt):
        self.rect.midleft = pygame.mouse.get_pos()
        self.hit_timer()
        self.hit_animation()

class StoneOre(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_stone_ore = surf
        self.image = self.original_stone_ore
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(300,400)

        # rotate
        self.rotation = 0
        self.rotation_speed = randint(-200, 200)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time > self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_stone_ore, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)

class SulfurOre(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_sulfur_ore = surf
        self.image = self.original_sulfur_ore
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(450,550)

        # rotate
        self.rotation = 0
        self.rotation_speed = randint(-300, 300)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time > self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_sulfur_ore, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)





    while True:
        display_surface.fill((0, 0, 0))
        draw_text()

def timeLeft():
    time_left = game_time - (pygame.time.get_ticks()/1000)
    return round(time_left,1)

def showTime():
    time_surf = font.render(str(timeLeft()), True, (240, 240, 240))
    time_rect = time_surf.get_frect(topright=(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50))
    display_surface.blit(time_surf, time_rect)
    pygame.draw.rect(display_surface, (240, 240, 240), time_rect.inflate(20,10).move(0,-8),5,10)

def showEq(stone,sulfur):
    eq_surf = font.render(str(f'Stone: {stone}, Sulfur: {sulfur}'),True,(200,200,200))
    eq_rect = eq_surf.get_frect(topright=(WINDOW_WIDTH - 50, WINDOW_HEIGHT - 150))
    display_surface.blit(eq_surf, eq_rect)
    pygame.draw.rect(display_surface,(240,240,240), eq_rect.inflate(20,10).move(0,-8),5,10)

def loadResources(id):
    resources_on_server = Resource.objects.filter(user_id=id)
    for i in resources_on_server:
        print(f'Nazwa: {i.name}, ilość: {i.quantity}, właściciel: {i.user}')
    return resources_on_server

def saveResources(id):
    for resource in Resource.objects.filter(user_id=id):
        if resource.name == 'stone_ore':
            resource.quantity += stone_ore
            resource.save()
        if resource.name == 'sulfur_ore':
            resource.quantity += sulfur_ore
            resource.save()
    loadResources(id)



# def get_authenticated_user():
#     try:
#         response = requests.get(API_URL, cookies={'sessionid': 'YOUR_SESSION_ID'})
#
#         if response.status_code == 200:
#             user_data = response.json()
#             username = user_data.get('username', 'Nieznany użytkownik')
#             print(f'Zalogowany użytkownik: {username}')
#         else:
#             print(f'Błąd: {response.status_code} - {response.text}')
#             return None
#     except requests.exceptions.RequestException as e:
#         print(f'Błąd połączenia: {e}')

# def save_resources_on_host(username, all_resources):
#     data = {
#         'username': username,
#         'resources': all_resources
#     }
#
#     try:
#         response = requests.post(API_URL, json=data)
#         if response.status_code == 200:
#             print('Dane zostały wysłane.')
#         else:
#             print('Błąd w dostarczeniu danych.')
#     except requests.exceptions.RequestException as e:
#         print("Błąd połączenia.")
#
# # player data
# username = get_authenticated_user()
# if username:
#     print(f'Zalogowany jako: {username}')
# else:
#     print('Nie można pobrać użytkownika')

# class Resources:
#     def __init__(self, username, resources_type=None, resources_amount=None, created=None):
#         self.username = username
#         self.resources_type = resources_type
#         self.resources_amount = resources_amount
#         self.created = created or datetime.now()


# resources = Resources(username=username, resources_type= resources_type, resources_amount=resources_amount)
resources_new = [
    {'name': 'stone_ore',
     'quantity': stone_ore},
    {'name': 'sulfur_ore',
     'quantity': sulfur_ore},
]

def checkUser():
    all_usernames = User.objects.all().values_list('id', 'username').order_by('id')
    for username in all_usernames:
        if user_logged == username[1]:
            return user_logged
        else:
            return None



# sprites
all_sprites = pygame.sprite.Group()
ore_sprites = pygame.sprite.Group()
stone_ore_sprites = pygame.sprite.Group()
metal_ore_sprites = pygame.sprite.Group()
sulfur_ore_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
player = Player((all_sprites, player_sprites))


# custom event
stone_ore_event = pygame.event.custom_type()
sulfur_ore_event = pygame.event.custom_type()
metal_ore_event = pygame.event.custom_type()
pygame.time.set_timer(stone_ore_event,500)
pygame.time.set_timer(sulfur_ore_event, 1500)

def main_menu(): # Main Menu Screen
    while True:

        display_surface.fill((0, 0, 0))
        draw_text("Menu", font, (255, 255, 255), display_surface, 20, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def mountain():
    pass

def forest():
    pass

def options():
    pass



while running:
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or timeLeft()<=0 or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            saveResources(userLogged('macius'))
            print(f'stone ore = ', stone_ore, '||| sulfur ore = ', sulfur_ore)
            print(f"Zalogowany użytkownik: {checkUser()}")

            if checkUser() != None:
                print("Zapisano dane")

            # print(serializer)
            # print(serializer.data)


        if event.type == stone_ore_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            StoneOre(stone_ore_surf, (x, y), (all_sprites, ore_sprites, stone_ore_sprites))
        if event.type == sulfur_ore_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            SulfurOre(sulfur_ore_surf,(x, y), (all_sprites, ore_sprites, sulfur_ore_sprites))
        # if event.type = metal_ore_event:


        # collecting resources
        hitting_point = player.rect.midleft

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player.hit_timer():
                for stone_ore_ in stone_ore_sprites:
                    if stone_ore_.rect.collidepoint(hitting_point):
                        stone_ore_.kill()
                        stone_ore += 1
                        player.pickaxe_hit_time = pygame.time.get_ticks()
                        player.can_hit = False
                for sulfur_ore_ in sulfur_ore_sprites:
                    if sulfur_ore_.rect.collidepoint(hitting_point):
                        sulfur_ore_.kill()
                        sulfur_ore += 1
                        player.pickaxe_hit_time = pygame.time.get_ticks()
                        player.can_hit = False


    # update
    all_sprites.update(dt)
    target_point_rect.center = pygame.mouse.get_pos()
    # collisions()

    # draw the game
    display_surface.fill('gray')
    stone_ore_sprites.draw(display_surface)
    sulfur_ore_sprites.draw(display_surface)
    showTime()
    showEq(stone_ore, sulfur_ore)
    all_sprites.draw(display_surface)
    display_surface.blit(target_point_image, target_point_rect)
    pygame.display.update()



pygame.quit()