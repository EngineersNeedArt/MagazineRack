import pygame


class SoundEffects:
    def __init__(self):
        pygame.mixer.init()     # Initialize Pygame mixer, load sounds.
        self.right_sound = pygame.mixer.Sound('page-turn.wav')
        self.left_sound = pygame.mixer.Sound('page-turn.wav')
        self.fail_sound = pygame.mixer.Sound('ankh.wav')


    def play_open(self):
        self.right_sound.play()


    def play_right(self):
        self.right_sound.play()


    def play_left(self):
        self.left_sound.play()


    def play_fail(self):
        self.fail_sound.play()


