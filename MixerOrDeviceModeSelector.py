from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ModeSelectorComponent import ModeSelectorComponent

class MixerOrDeviceModeSelector(ModeSelectorComponent):

    def __init__(self, shift_btn, encoders, dummy_encoders, vol_encoder, stop_button, play_button, record_button, select_button, up_button, down_button, left_button, right_button, mixer, session, device, mixer_modes, device_nav, pad_1, pad_2, pad_3, pad_4, pad_5, pad_6, pad_7, pad_8, pad_9, pad_10, pad_11, pad_12, pad_13, pad_14, pad_15, pad_16):
        ModeSelectorComponent.__init__(self)
        self._encoders = encoders
        self._vol_encoder = vol_encoder
        self._dummy_encoders = dummy_encoders
        self._select_button = select_button
        self._play_button = play_button
        self._stop_button = stop_button
        self._record_button = record_button
        self._up_button = up_button
        self._down_button = down_button
        self._left_button = left_button
        self._right_button = right_button
        self._mixer = mixer
        self._session = session
        self._device = device
        self._mixer_modes = mixer_modes
        self._device_nav = device_nav
        self._shift_btn = shift_btn
        self._pad1 = pad_1
        self._pad2 = pad_2
        self._pad3 = pad_3
        self._pad4 = pad_4
        self._pad5 = pad_5
        self._pad6 = pad_6
        self._pad7 = pad_7
        self._pad8 = pad_8

        self._pad9 = pad_9
        self._pad10 = pad_10
        self._pad11 = pad_11
        self._pad12 = pad_12
        self._pad13 = pad_13
        self._pad14 = pad_14
        self._pad15 = pad_15
        self._pad16 = pad_16

    def disconnect(self):
        self._encoders = None
        self._select_button = None
        self._up_button = None
        self._down_button = None
        self._left_button = None
        self._right_button = None
        self._mixer = None
        self._session = None
        self._device = None
        self._mixer_modes = None
        self._device_nav = None
        ModeSelectorComponent.disconnect(self)

    def number_of_modes(self):
        return 3

    def update(self):
        super(MixerOrDeviceModeSelector, self).update()
        if self.is_enabled():
            if self._mode_index == 0:
                # Volume/pan (mode determined by EncoderMixerModeSelector, mixer
                self._device.set_parameter_controls(None)
                self._mixer_modes.set_controls(self._encoders)
                self._device.set_bank_nav_buttons(None, None)
                self._device_nav.set_device_nav_buttons(None, None)
                self._mixer.set_select_buttons(self._right_button, self._left_button)
                self._session.set_page_left_button(self._left_button)
                self._session.set_page_right_button(self._right_button)
                self._device.set_on_off_button(None)
                self._mixer.selected_strip().set_arm_button(self._select_button)

            elif self._mode_index == 1:

                # Inst/FX
                self._mixer_modes.set_controls(None)
                
                self._device_nav.set_shift_btn(self._play_button)
                self._device.set_parameter_controls(self._encoders)
                self._mixer.set_select_buttons(self._right_button, self._left_button)
                self._session.set_page_left_button(None)
                self._session.set_page_right_button(None)
                self._device.set_bank_nav_buttons(None, None)
                self._device_nav.set_device_nav_buttons(None, None)
                self._device_nav.set_device_nav_arp1(self._pad1)
                self._device_nav.set_device_nav_arp2(self._pad2)
                self._device_nav.set_device_nav_throwRVB(self._pad3)
                self._device_nav.set_device_nav_throwDLY(self._pad4)
                # self._device_nav.set_device_nav_show_midi(self._play_button)
                self._device_nav.set_device_nav_dec_tempo(self._pad9)
                self._device_nav.set_device_nav_inc_tempo(self._pad10)
                self._device_nav.set_device_nav_dup_scene(self._pad12)
                self._device_nav.set_transp_down(self._pad5)
                self._device_nav.set_transp_up(self._pad6)
                self._device_nav.set_vol_encoder(self._vol_encoder)
                # self._mixer.selected_strip().set_arm_button(self._record_button)
                self._mixer.selected_strip().set_solo_button(self._pad8)
                self._mixer.selected_strip().set_mute_button(self._pad7)
                # self._device.set_on_off_button(self._select_button)

            elif self._mode_index == 2:

                # Hypercontrol off, plain old MIDI
                self._mixer_modes.set_controls(None)
                self._device.set_parameter_controls(None)
                self._device.set_bank_nav_buttons(None, None)
                self._device_nav.set_device_nav_buttons(None, None)
                self._mixer.set_select_buttons(None, None)
                self._session.set_page_left_button(None)
                self._session.set_page_right_button(None)
                self._device.set_on_off_button(None)
                self._mixer.selected_strip().set_arm_button(None)

