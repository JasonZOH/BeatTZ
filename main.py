from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from audio import Audio
from sound_service import SoundService
from track import TrackWidget

Builder.load_file("track.kv")

TRACK_NB_SIZE = 10


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.sound_service = SoundService()

        # kick_sound = self.sound_service.get_son_at(0)

        self.audio = Audio()
        self.mixer = self.audio.create_mixer(self.sound_service.soundkit.get_all_samples(), 100, TRACK_NB_SIZE)

    def on_parent(self, widget, parent):
        for i in range(0, self.sound_service.get_nb_son()):
            sound = self.sound_service.get_son_at(i)
            self.tracks_layout.add_widget(TrackWidget(sound, self.audio, TRACK_NB_SIZE, self.mixer.tracks[i]))


class BeatZApp(App):
    pass


BeatZApp().run()