"""Parser for SensorPro BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/thermoplus.py

MIT License applies.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from struct import unpack

from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import BinarySensorDeviceClass, SensorLibrary

_LOGGER = logging.getLogger(__name__)


@dataclass
class SensorProDevice:

    model: str
    name: str


DEVICE_TYPES = {
    0x10: SensorProDevice("16", "Lanyard/mini hygrometer"),
    0x11: SensorProDevice("17", "Smart hygrometer"),
    0x15: SensorProDevice("21", "Smart hygrometer"),
}
MFR_IDS = set(DEVICE_TYPES)

SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"


class SensorProBluetoothDeviceData(BluetoothData):
    """Date update for SensorPro Bluetooth devices."""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing sensorpro BLE advertisement data: %s", service_info)
        if SERVICE_UUID not in service_info.service_uuids:
            return
        if not MFR_IDS.intersection(service_info.manufacturer_data):
            return
        changed_manufacturer_data = self.changed_manufacturer_data(service_info)
        if not changed_manufacturer_data:
            return
        last_id = list(changed_manufacturer_data)[-1]
        data = (
            int(last_id).to_bytes(2, byteorder="little")
            + changed_manufacturer_data[last_id]
        )
        msg_length = len(data)
        if msg_length not in (20, 22):
            return
        device_id = data[0]
        device_type = DEVICE_TYPES[device_id]
        name = device_type.name
        self.set_precision(2)
        self.set_device_type(device_id)
        self.set_title(f"{name} {short_address(service_info.address)}")
        self.set_device_name(f"{name} {short_address(service_info.address)}")
        self.set_device_manufacturer("SensorPro")
        self._process_update(data)

    def _process_update(self, data: bytes) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing SensorPro BLE advertisement data: %s", data)
        if len(data) != 20:
            return

        button_pushed = data[3] & 0x80
        xvalue = data[10:16]

        (volt, temp, humi) = unpack("<HhH", xvalue)

        if volt >= 3000:
            batt = 100
        elif volt >= 2600:
            batt = 60 + (volt - 2600) * 0.1
        elif volt >= 2500:
            batt = 40 + (volt - 2500) * 0.2
        elif volt >= 2450:
            batt = 20 + (volt - 2450) * 0.4
        else:
            batt = 0

        self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
        self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, temp / 16)
        self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, humi / 16)
        self.update_predefined_sensor(
            SensorLibrary.VOLTAGE__ELECTRIC_POTENTIAL_VOLT, volt / 1000
        )
        self.update_predefined_binary_sensor(
            BinarySensorDeviceClass.OCCUPANCY, bool(button_pushed)
        )
