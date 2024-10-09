import pygame


pygame.mixer.init()     # Initialize Pygame mixer, load sounds.
right_sound = pygame.mixer.Sound('page-turn.wav')
left_sound = pygame.mixer.Sound('page-turn.wav')
fail_sound = pygame.mixer.Sound('ankh.wav')

def play_right_sound():
    right_sound.play()

def play_left_sound():
    left_sound.play()

def play_fail_sound():
    fail_sound.play()