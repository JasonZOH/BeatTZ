from array import array

from audiostream.sources.thread import ThreadSource

from audio_source_track import AudioSourceTrack


class AudioSourceMixer(ThreadSource):
    buf = None

    def __init__(self, output_stream, all_wav_samples, bpm, sample_rate, nb_steps, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)

        self.tracks = []
        for i in range(0, len(all_wav_samples)):
            track = AudioSourceTrack(output_stream, all_wav_samples[i], bpm, sample_rate)
            track.set_step((0,) * nb_steps)
            self.tracks.append(track)

        self.nb_steps = nb_steps
        self.current_sample_index = 0
        self.current_step_index = 0
        self.sample_rate = sample_rate

    def set_step(self, index, steps):
        if index >= len(self.tracks):
            return

        if not len(steps) == self.nb_steps:
            self.tracks[index].set_step(steps)

    def set_bpm(self, bpm):
        for i in range(0, len(self.tracks)):
            self.tracks[i].set_bpm(bpm)

    def get_bytes(self, *args, **kwargs):
        step_nb_sample = self.tracks[0].step_nb_samples
        if self.buf is None or not len(self.buf) == step_nb_sample:
            self.buf = array('h', b"\x00\x00" * step_nb_sample)

        track_buffers = []
        for i in range(0, len(self.tracks)):
            track = self.tracks[i]
            track_buffer = track.get_bytes_array()
            track_buffers.append(track_buffer)

        for i in range(0, step_nb_sample):
            self.buf[i] = 0
            for j in range(0, len(track_buffers)):
                self.buf[i] += track_buffers[j][i]

        self.current_step_index += 1
        if self.current_step_index >= self.nb_steps:
            self.current_step_index = 0

        return self.buf.tobytes()