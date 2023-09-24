from __future__ import absolute_import, print_function, unicode_literals
import Live
import math
import threading
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework import Task

# to notify TD of play state changes
import socket
import sys

DeviceType = Live.Device.DeviceType

def _deferred_solo_selected_track():
    t = Live.Song.view.selected_track
    t.solo = 1

def _deferred_unsolo_selected_track():
    t = Live.Song.view.selected_track
    t.solo = 0

def _deferred_arm_selected_track():
    t = Live.Song.view.selected_track
    t.arm = 1

def _deferred_unarm_selected_track():
    t = Live.Song.view.selected_track
    t.arm = 0



class DeviceNavComponent(ControlSurfaceComponent):


    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._left_button = None
        self._right_button = None
        self._arp1_button = None
        self._arp2_button = None
        self._shift_btn = None
        self._throwRVB_button = None
        self._throwDLY_button = None
        self._show_midi_button = None
        self._inc_tempo_button = None
        self._dec_tempo_button = None
        self._dup_scene_button = None
        self._transp_down_button = None
        self._transp_up_button = None
        self._vol_encoder = None

        self._shift_state = False
        self._last_mod_value = 0

        self._last_reported_time = 0.0
        self._song.view.add_selected_track_listener(self._arm_selected_track)
        self._song.add_is_playing_listener(self._play_state_changed)


    def _report_song_position(self):

        beatsPerSecond = self._song.tempo / 60.0
        millisecondsPerBeat = 1000.0 / beatsPerSecond
        latencyFraction = 90.0 / millisecondsPerBeat


        cst = math.ceil(self._song.current_song_time + latencyFraction)

        if(cst > self._last_reported_time):

            self._last_reported_time = cst

            
            if(cst % self._song.signature_numerator == 0):    

                timer = threading.Timer(0.1, _deferred_solo_selected_track)
                # self.dm = self._tasks.add(Task.run( self._solo_selected_track ))
                
            else:

                timer = threading.Timer(0.1, _deferred_unsolo_selected_track)
                #self.em = self._tasks.add(Task.run( self._unsolo_selected_track ))
      

    def _play_state_changed(self):

        is_playing = self._song.is_playing
        
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10000)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)

        try:

            # Send data
            message = b'playstate:' + str(is_playing).encode('ascii') + '\n'.encode('ascii')
            print('sending {!r}'.format(message))
            sock.sendall(message)

        finally:
            print('closing socket')
            sock.close()

    def _deferred_arm_selected_track(self):

        t = self._song.view.selected_track
        if(t.can_be_armed):
            tracks = self._song.tracks
            for tr in tracks:
                tr.arm = 0
            t.arm = 1

            app_view = self.application().view
            if not (app_view.is_view_visible('Detail') and app_view.is_view_visible('Detail/DeviceChain')):
                app_view.show_view('Detail')
                app_view.show_view('Detail/DeviceChain')
            
            # if (app_view.is_view_visible('Detail') and app_view.is_view_visible('Detail/DeviceChain')):
            directions = Live.Application.Application.View.NavDirection
            direction = directions.left
            modifier_pressed = True
            app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
            app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
            app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
            app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)

            direction = directions.right
            app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)


            app_view.focus_view('Session')

    def _deferred_unarm_selected_track(self):
        t = self._song.view.selected_track
        t.arm = 0

     
    def _arm_selected_track(self):
        self.ast = self._tasks.add(Task.run( self._deferred_arm_selected_track ))
        # self.switchView = self._tasks.add(Task.run( self._deferred_arm_selected_track ))

    def _unarm_selected_track(self):
        self.uast = self._tasks.add(Task.run( self._deferred_unarm_selected_track ))

    def _enable_metronome(self):
        self._song.metronome = 1
        self._song.tempo = self._song.tempo + 1
        self.em.kill()

    def _disable_metronome(self):
        self._song.metronome = 0
        self._song.tempo = self._song.tempo - 1
        self.dm.kill()

    def _solo_selected_track(self):
        t = self._song.view.selected_track
        t.solo = 1

    def _unsolo_selected_track(self):
        t = self._song.view.selected_track
        t.solo = 0
    
    def _mute_selected_track(self):
        t = self._song.view.selected_track
        t.mute = 1

    def _mute_selected_track(self):
        t = self._song.view.selected_track
        t.mute = 0


    def disconnect(self):
        if self._left_button != None:
            self._left_button.remove_value_listener(self._nav_value)
            self._left_button = None
        if self._right_button != None:
            self._right_button.remove_value_listener(self._nav_value)
            self._right_button = None
        if self._arp1_button != None:
            self._arp1_button.remove_value_listener(self._nav_arp1)
            self._arp1_button = None
        if self._arp2_button != None:
            self._arp2_button.remove_value_listener(self._nav_arp1)
            self._arp2_button = None
        if self._throwRVB_button != None:
            self._throwRVB_button.remove_value_listener(self._nav_throwRVB)
            self._throwRVB_button = None
        if self._throwDLY_button != None:
            self._throwDLY_button.remove_value_listener(self._nav_throwDLY)
            self._throwDLY_button = None
        if self._show_midi_button != None:
            self._show_midi_button.remove_value_listener(self._nav_show_midi)
            self._show_midi_button = None
        if self._inc_tempo_button != None:
            self._inc_tempo_button.remove_value_listener(self._nav_inc_tempo)
            self._inc_tempo_button = None
        if self._dec_tempo_button != None:
            self._dec_tempo_button.remove_value_listener(self._nav_dec_tempo)
            self._dec_tempo_button = None
        if self._dup_scene_button != None:
            self._dup_scene_button.remove_value_listener(self._nav_dup_scene)
            self._dup_scene_button = None
        if self._transp_down_button != None:
            self._transp_down_button.remove_value_listener(self._transp_down)
            self._transp_down_button = None
        if self._transp_up_button != None:
            self._transp_up_button.remove_value_listener(self._transp_up)
            self._transp_up_button = None
        if self._vol_encoder != None:
            self._vol_encoder.remove_value_listener(self._update_track_vol)
            self._vol_encoder = None
        if self._shift_btn != None:
            self._shift_btn.remove_value_listener(self._update_shift_state)
            self._shift_btn = None
        self._sock.close()

    def set_device_nav_buttons(self, left_button, right_button):
        identify_sender = True
        if self._left_button != None:
            self._left_button.remove_value_listener(self._nav_value)
        self._left_button = left_button
        if self._left_button != None:
            self._left_button.add_value_listener(self._nav_value, identify_sender)
        if self._right_button != None:
            self._right_button.remove_value_listener(self._nav_value)
        self._right_button = right_button
        if self._right_button != None:
            self._right_button.add_value_listener(self._nav_value, identify_sender)
        self.update()



    def set_vol_encoder(self, encoder):
        
        identify_sender = True
        if self._vol_encoder != None:
            self._vol_encoder.remove_value_listener(self._update_track_vol)
        self._vol_encoder = encoder
        self._vol_encoder.add_value_listener(self._update_track_vol, identify_sender)
        self.update()

    def set_shift_btn(self, encoder):
        
        identify_sender = True
        if self._shift_btn != None:
            self._shift_btn.remove_value_listener(self._update_shift_state)
        self._shift_btn = encoder
        self._shift_btn.add_value_listener(self._update_shift_state, identify_sender)
        self.update()

    def _update_track_vol(self, value, sender):
        
        tr = self._song.view.selected_track
        if(tr.can_be_armed):
            md = tr.mixer_device
            md.volume.value = value / 127.0

    def _update_shift_state(self, value, sender):
        
        if(value > self._last_mod_value):
            self._shift_state = True
        else:
            self._shift_state = False

        self._last_mod_value = value


    def set_device_nav_arp1(self, button):
        identify_sender = True
        if self._arp1_button != None:
            self._arp1_button.remove_value_listener(self._nav_arp1)
        self._arp1_button = button
        if self._arp1_button != None:
            self._arp1_button.add_value_listener(self._nav_arp1, identify_sender)
        self.update()

    def set_device_nav_arp2(self, button):
        identify_sender = True
        if self._arp2_button != None:
            self._arp2_button.remove_value_listener(self._nav_arp2)
        self._arp2_button = button
        if self._arp2_button != None:
            self._arp2_button.add_value_listener(self._nav_arp2, identify_sender)
        self.update()

    def set_device_nav_throwRVB(self, button):
        identify_sender = True
        if self._throwRVB_button != None:
            self._throwRVB_button.remove_value_listener(self._nav_throwRVB)
        self._throwRVB_button = button
        if self._throwRVB_button != None:
            self._throwRVB_button.add_value_listener(self._nav_throwRVB, identify_sender)
        self.update()

    def set_device_nav_throwDLY(self, button):
        identify_sender = True
        if self._throwDLY_button != None:
            self._throwDLY_button.remove_value_listener(self._nav_throwDLY)
        self._throwDLY_button = button
        if self._throwDLY_button != None:
            self._throwDLY_button.add_value_listener(self._nav_throwDLY, identify_sender)
        self.update()

    def set_device_nav_fx(self, button):
        identify_sender = True
        if self._fx_button != None:
            self._fx_button.remove_value_listener(self._nav_fx)
        self._fx_button = button
        if self._fx_button != None:
            self._fx_button.add_value_listener(self._nav_fx, identify_sender)
        self.update()

    def set_device_nav_show_midi(self, button):
        identify_sender = True
        if self._show_midi_button != None:
            self._show_midi_button.remove_value_listener(self._nav_show_midi)
        self._show_midi_button = button
        if self._show_midi_button != None:
            self._show_midi_button.add_value_listener(self._nav_show_midi, identify_sender)
        self.update()

    def set_device_nav_dec_tempo(self, button):
        identify_sender = True
        if self._dec_tempo_button != None:
            self._dec_tempo_button.remove_value_listener(self._nav_dec_tempo)
        self._dec_tempo_button = button
        if self._dec_tempo_button != None:
            self._dec_tempo_button.add_value_listener(self._nav_dec_tempo, identify_sender)
        self.update()

    def set_device_nav_inc_tempo(self, button):
        identify_sender = True
        if self._inc_tempo_button != None:
            self._inc_tempo_button.remove_value_listener(self._nav_inc_tempo)
        self._inc_tempo_button = button
        if self._inc_tempo_button != None:
            self._inc_tempo_button.add_value_listener(self._nav_inc_tempo, identify_sender)
        self.update()

    def set_device_nav_dup_scene(self, button):
        identify_sender = True
        if self._dup_scene_button != None:
            self._dup_scene_button.remove_value_listener(self._nav_dup_scene)
        self._dup_scene_button = button
        if self._dup_scene_button != None:
            self._dup_scene_button.add_value_listener(self._nav_dup_scene, identify_sender)
        self.update()

    def set_transp_up(self, button):
        identify_sender = True
        if self._transp_up_button != None:
            self._transp_up_button.remove_value_listener(self._transp_up)
        self._transp_up_button = button
        if self._transp_up_button != None:
            self._transp_up_button.add_value_listener(self._transp_up, identify_sender)
        self.update()

    def set_transp_down(self, button):
        identify_sender = True
        if self._transp_down_button != None:
            self._transp_down_button.remove_value_listener(self._transp_down)
        self._transp_down_button = button
        if self._transp_down_button != None:
            self._transp_down_button.add_value_listener(self._transp_down, identify_sender)
        self.update()

    def set_transp_down(self, button):
        identify_sender = True
        if self._transp_down_button != None:
            self._transp_down_button.remove_value_listener(self._transp_down)
        self._transp_down_button = button
        if self._transp_down_button != None:
            self._transp_down_button.add_value_listener(self._transp_down, identify_sender)
        self.update()


    def on_enabled_changed(self):
        self.update()

    def _nav_value(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                app_view = self.application().view
                if not (app_view.is_view_visible('Detail') and app_view.is_view_visible('Detail/DeviceChain')):
                    app_view.show_view('Detail')
                    app_view.show_view('Detail/DeviceChain')
                else:
                    directions = Live.Application.Application.View.NavDirection
                    direction = directions.right if sender == self._right_button else directions.left
                    modifier_pressed = True
                    app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)


    def _change_arp_state(self, direction):

        positions = {
            '1/16' : 54.0,
            '1/8': 74.0,
            '1/4': 93.0,
            '1/2': 113.0,
            '1/1': 123.0
        }

        tr = self._song.view.selected_track
        devs = tr.devices

        # text = "---------\n"
        for device in devs:
            if device.type == DeviceType.midi_effect:
                if device.name == "Improv MIDI rack":
                    deviceActive = 127.0
                    toggleDeviceActive = False
                    for param in device.parameters:

                        if(param.name == "Synced Rate"):
                            curval = param.value
                            
                            
                            if(curval >= positions['1/16'] and curval < positions['1/8']):
                                if(curval == positions['1/16']):     
                                    if(direction == -1): # at 1/16, going down so toggle   
                                        toggleDeviceActive = True
                                    else:
                                        param.value = positions['1/8']
                                else:
                                    param.value = positions['1/8'] if direction == 1 else positions['1/16']
                            elif(curval >= positions['1/8'] and curval < positions['1/4']):
                                param.value = positions['1/4'] if direction == 1 else positions['1/16']
                            elif(curval >= positions['1/4'] and curval < positions['1/2']):
                                param.value = positions['1/2'] if direction == 1 else positions['1/8']
                            elif(curval >= positions['1/2'] and curval <= positions['1/1']):
                                if(curval == positions['1/1']):
                                    if(direction == 1): # at 1/1, going up so turn off
                                        toggleDeviceActive = True
                                    else:
                                        param.value = positions['1/2']
                                else:
                                    param.value = positions['1/1'] if direction == 1 else positions['1/4']
                            elif(curval > positions['1/1']):
                                if(direction == 1): # at 1/1, going up so turn off
                                        toggleDeviceActive = True
                                else:
                                    param.value = positions['1/2']

                        # text += 'name: ' + param.name + ' / val: ' + str(param.value) + ' / min: ' + str(param.min) + ' / max: ' + str(param.min) + ' / q: ' + str(param.is_quantized) + "\n"
                        if(param.name == 'Arp On'):
                            if(toggleDeviceActive):
                                param.value = 127.0 - param.value
                            else:  
                                param.value = deviceActive
                break
            # text += "----------\n"

        # raise Exception(text)

    def _nav_arp1(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                if(self._shift_state):
                    self._nav_dec_tempo(127.0, sender)
                else:
                    self._change_arp_state(-1)


    def _nav_arp2(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                if(self._shift_state):
                    self._nav_inc_tempo(127.0, sender)
                else:
                    self._change_arp_state(1)

    def _throw(self, value, mode):

        tr = self._song.view.selected_track
        mx = tr.mixer_device

        send2 = mx.sends[1]

        if value != 0:
            send2.value = 1.0
        else:  
            send2.value = 0.0

        # enable requested device in return track, disable other(s)
        returns = self._song.return_tracks
        text = "-------\n"
        for r in returns:

            text += "RETURN NAME: " + r.name + "\n"
            if r.name == 'B-THROW':
                text += "BORK FOUND\n"
                devices = r.devices

                for device in devices:
                    if device.name != 'COMP':
                        text += "DEVICE NAME: " + device.name + "\n"
                        params = device.parameters
                        for param in params:
                            if param.name == 'Device On':
                                if device.name == mode:
                                    param.value = 1.0
                                else:
                                    param.value = 0.0
                                break

        # raise Exception(text)

    def _nav_throwRVB(self, value, sender):
        if self.is_enabled():
            self._throw(value, 'REVERB')

    def _nav_throwDLY(self, value, sender):
        if self.is_enabled():
            if(self._shift_state):
                self._nav_dup_scene(value, sender)
            else:
                self._throw(value, 'DELAY')

    def _nav_fx(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                app_view = self.application().view
                if not (app_view.is_view_visible('Detail') and app_view.is_view_visible('Detail/DeviceChain')):
                    app_view.show_view('Detail')
                    app_view.show_view('Detail/DeviceChain')
                
                directions = Live.Application.Application.View.NavDirection
                direction = directions.left
                modifier_pressed = True
                app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
                app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
                app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
                app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
                app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)

                direction = directions.right
                app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
                app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
                app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
                app_view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)

                app_view.focus_view('Session')

    def _nav_show_midi(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                app_view = self.application().view
                if not (app_view.is_view_visible('Detail') and app_view.is_view_visible('Detail/Clip')):
                    app_view.show_view('Detail')
                    app_view.show_view('Detail/Clip')

    def _nav_dec_tempo(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                self._song.tempo = self._song.tempo - 1

    def _nav_inc_tempo(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                self._song.tempo = self._song.tempo + 1

    def _nav_dup_scene(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                scene = self._song.view.selected_scene
                scene_index = list(self._song.scenes).index(scene)
                self._song.duplicate_scene(scene_index)

    def _transp(self, delta):
        scene = self._song.view.selected_scene
        tr = self._song.view.selected_track

        current_clip_slot = self._song.view.highlighted_clip_slot

        for clip_slot in scene.clip_slots:
            if (clip_slot.clip is not None) and (abs(delta) <= 1 or clip_slot == current_clip_slot):
                clip_slot.clip.select_all_notes()
                notes = clip_slot.clip.get_selected_notes()

                newNotes = []
                for note in notes:
                    newNote = (note[0] + delta, note[1], note[2], note[3], note[4])
                    newNotes.append(newNote)

                clip_slot.clip.replace_selected_notes(tuple(newNotes))

    def _transp_down(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                if(self._shift_state):
                    self._transp(-12)
                else:
                    self._transp(-1)

    def _transp_up(self, value, sender):
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                if(self._shift_state):
                    self._transp(12)
                else:
                    self._transp(1)
