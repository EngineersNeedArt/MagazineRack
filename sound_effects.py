import pygame


class SoundEffects:
    def __init__(self):
        pygame.mixer.init()     # Initialize Pygame mixer, load sounds.
        self.in_sound = pygame.mixer.Sound('sounds/in_sound.wav')
        self.out_sound = pygame.mixer.Sound('sounds/out_sound.wav')
        self.toc_in_sound = pygame.mixer.Sound('sounds/toc_in_sound.wav')
        self.toc_out_sound = pygame.mixer.Sound('sounds/toc_out_sound.wav')
        self.open_sound = pygame.mixer.Sound('sounds/open_sound.wav')
        self.left_sound = pygame.mixer.Sound('sounds/page-turn.wav')
        self.right_sound = pygame.mixer.Sound('sounds/page-turn.wav')
        self.fail_sound = pygame.mixer.Sound('sounds/fail_sound.wav')


    def play_open_toc(self):
        self.toc_in_sound.play()


    def play_close_toc(self):
        self.toc_out_sound.play()


    def play_nav_left(self):
        self.out_sound.play()


    def play_nav_right(self):
        self.in_sound.play()


    def play_nav_up(self):
        self.out_sound.play()


    def play_nav_down(self):
        self.in_sound.play()


    def play_open_magazine(self):
        self.open_sound.play()


    def play_left_page(self):
        self.left_sound.play()


    def play_right_page(self):
        self.right_sound.play()




    def play_fail(self):
        self.fail_sound.play()


