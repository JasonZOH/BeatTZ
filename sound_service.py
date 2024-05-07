import wave
from array import array


class Sound:
    samples = None
    nb_samples = 0


    def __init__(self, filename, displayname):
        self.filename = filename
        self.displayname = displayname
        self.load_son()

    def load_son(self):
        wav_file = wave.open(self.filename, mode='rb')
        self.nb_samples = wav_file.getnframes()
        frames = wav_file.readframes(self.nb_samples) # octet/byte : 8bits
        self.samples = array('h', frames)


class SoundKit:
    sounds = ()

    def get_nb_son(self):
        return len(self.sounds)

    def get_all_samples(self):
        all_samples = []
        for i in range(0, len(self.sounds)):
            all_samples.append(self.sounds[i].samples)
        return all_samples


class SoundKit1(SoundKit):
    sounds = ( Sound("sounds/kit1/kick.wav", "KICK"),
               Sound("sounds/kit1/clap.wav", "CLAP"),
               Sound("sounds/kit1/snare.wav", "SNARE"),
               Sound("sounds/kit1/shaker.wav", "SHaker"),
               Sound("sounds/kit1/kesseEtOsman.wav", "kesOsm"))


class SoundService:
    soundkit = SoundKit1()

    def get_nb_son(self):
        return self.soundkit.get_nb_son()

    def get_son_at(self, index):
        if index >= len(self.soundkit.sounds):
            return None
        return self.soundkit.sounds[index]