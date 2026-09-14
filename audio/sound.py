from pygame import mixer


class Sound():
    def __init__(self, path, volume):
        self.mixer_sound = mixer.Sound(path)
        self.volume = volume

    def play(self):
        self.mixer_sound.set_volume(self.volume)
        self.mixer_sound.play()