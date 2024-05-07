from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton


class TrackStepButton(ToggleButton):
    pass


class TrackSoundButton(Button):
    pass


class TrackWidget(BoxLayout):
    def __init__(self, sound, audio, nb_steps, source_track, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)
        sound_button = TrackSoundButton()
        sound_button.text = sound.displayname
        sound_button.on_press = self.on_sound_button_press
        self.add_widget(sound_button)
        self.audio = audio
        self.sound = sound
        self.source_track = source_track
        self.step_buttons = []
        self.nb_steps = nb_steps
        for i in range(0, nb_steps):
            step_button = TrackStepButton()
            step_button.bind(state=self.on_step_state)
            self.step_buttons.append(step_button)
            self.add_widget(step_button)

    def on_sound_button_press(self):
        self.audio.play_sound(self.sound.samples)

    def on_step_state(self, widget, value):
        steps = []
        for i in range(0, self.nb_steps):
            if self.step_buttons[i].state == "down":
                steps.append(1)
            else:
                steps.append(0)
        self.source_track.set_step(steps)