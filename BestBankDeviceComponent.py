from __future__ import absolute_import, print_function, unicode_literals
import Live
from .Devices import BANK_NAME_DICT, DEVICE_BOB_DICT, DEVICE_DICT, parameter_bank_names, parameter_banks
from _Framework.DeviceComponent import DeviceComponent
from _Generic.Devices import device_parameters_to_map
from ableton.v2.base import liveobj_valid
from _Framework.DisplayDataSource import DisplayDataSource
BOP_BANK_NAME = 'Best of Parameters'

class BestBankDeviceComponent(DeviceComponent):

    def __init__(self, *a, **k):
        (super(BestBankDeviceComponent, self).__init__)(*a, **k)
        new_banks = {}
        new_bank_names = {}
        self._device_banks = DEVICE_DICT
        self._device_bank_names = BANK_NAME_DICT
        self._device_best_banks = DEVICE_BOB_DICT



        self._device_banks = new_banks
        self._device_bank_names = new_bank_names
        self._bank_name_data_source = DisplayDataSource()


    def disconnect(self):
        self._bank_name_data_source = None
        DeviceComponent.disconnect(self)

    def bank_name_data_source(self):
        return self._bank_name_data_source

    def _bank_up_value(self, value):
        DeviceComponent._bank_up_value(self, value)
        self._update_bank_display()

    def _bank_down_value(self, value):
        DeviceComponent._bank_down_value(self, value)
        self._update_bank_display()

    def _update_bank_display(self):
        if self.is_enabled():
            bank_name = ''
            if self._device != None:
                if self._bank_name != '<No Bank>':
                    bank_name = self._bank_name
                    if bank_name in (BOP_BANK_NAME, 'Bank 1'):
                        bank_name = 'Home'
            self._bank_name_data_source.set_display_string(bank_name)

    def _is_banking_enabled(self):
        return True

    def _number_of_parameter_banks(self):
        result = 0
        if self._device != None:
            if self._device.class_name in list(self._device_banks.keys()):
                result = len(self._device_banks[self._device.class_name])
            else:
                result = DeviceComponent._number_of_parameter_banks(self)
        return result

    def _parameter_banks(self):
        return parameter_banks(self._device, self._device_banks)

    def _parameter_bank_names(self):
        return parameter_bank_names(self._device, self._device_bank_names)