# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random
import tempfile
import emoji
import wave
import pyaudio
import threading
import sounddevice as sd
import numpy as np
from EartAgent.Agent.text_agents import QwenAgent, AgentConfig
from EartAgent.Agent.Audio_Agents import AudioAgentConfig, QwenAudioAgent, SambertAgent


class VoiceAssistant:
    def __init__(self, api_key: str):
        QwenAudioAgent.api_key = api_key
        QwenAgent.api_key = api_key
        SambertAgent.api_key = api_key

        self.audio_config = AudioAgentConfig(system_prompt="The output format is: The audio says..")
        self.audio_agent = QwenAudioAgent(self.audio_config)

        self.text_config = AgentConfig(name='Xiao Li', system_prompt='Please note you are having a real-time conversation with a person, keep the text concise',
                                       remember=True)
        self.text_agent = QwenAgent(self.text_config)

        self.speech_synthesis_config = AudioAgentConfig(system_prompt="")
        self.speech_synthesis_agent = SambertAgent(self.speech_synthesis_config)

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.lock = threading.Lock()

    # Other methods remain unchanged
    def start_recording(self):
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                                      frames_per_buffer=1024)
        self.is_recording = True
        print("Recording started...")
        threading.Thread(target=self.record_audio).start()

    def record_audio(self):
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        print("Recording stopped...")

        with self.lock:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_wav = os.path.join(temp_dir, 'temp.wav')
                waveFile = wave.open(temp_wav, 'wb')
                waveFile.setnchannels(1)
                waveFile.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                waveFile.setframerate(16000)
                waveFile.writeframes(b''.join(self.frames))
                waveFile.close()

                # Add a delay before releasing the file

                # time.sleep(0.5)
                audio_response = self.audio_agent(temp_wav)
                print(f"User: {audio_response}")
                emoji_list = ['😀', '😃', '😁', '😄', '🙂', '😘', '😊', '🤗', '🤪', '😋', '😍']
                rdn = random.randint(0, len(emoji_list) - 1)
                text_response = self.text_agent.chat(audio_response)
                self.text_agent.speak(text_response + emoji.emojize(emoji_list[rdn]))
                # Synthesize speech response
                speech_data = self.speech_synthesis_agent.chat(text_response)
                if speech_data:
                    self.play_audio(speech_data)

                # Ensure enough time before deleting the temporary directory
                # time.sleep(1)

        # The temporary directory will be automatically deleted when exiting the context manager
    def play_audio(self, audio_data):
        sample_rate = 44100
        bit_depth = 16
        # Determine the type of audio data (8-bit, 16-bit, 32-bit)
        dtype = {
            8: np.uint8,
            16: np.int16,
            32: np.int32
        }[bit_depth]

        # Convert byte data to a numpy array
        audio_data = np.frombuffer(audio_data, dtype=dtype)

        # If the audio is stereo, convert to mono
        if audio_data.ndim == 2 and audio_data.shape[1] == 2:
            audio_data = audio_data.mean(axis=1)

        # Play the audio data
        sd.play(audio_data, sample_rate)

        # Wait for the audio to finish playing
        sd.wait()

    def run(self):
        while True:
            try:
                print("Press Enter to start recording, press Enter again to stop recording...")
                input()
                self.start_recording()
                input()
                self.stop_recording()
            except KeyboardInterrupt:
                break


