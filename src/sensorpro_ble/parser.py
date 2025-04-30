"""Parser for SensorPro BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/brifit.py

MIT License applies.
"""

from __future__ import annotations

import logging
from struct import unpack

from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from habluetooth import BluetoothServiceInfoBleak
from sensor_state_data import SensorLibrary

_LOGGER = logging.getLogger(__name__)


DEVICE_TYPES = {
    0x01: "T201",
    0x05: "T301",
}
DEFAULT_MODEL = "T201"
MFR_IDS = set(DEVICE_TYPES)


class SensorProBluetoothDeviceData(BluetoothData):
    """Date update for SensorPro Bluetooth devices."""

    def _start_update(self, service_info: BluetoothServiceInfoBleak) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing sensorpro BLE advertisement data: %s", service_info)
        changed_manufacturer_data = self.changed_manufacturer_data(service_info)
        if 43605 not in changed_manufacturer_data:
            return
        if not changed_manufacturer_data or len(changed_manufacturer_data) > 1:
            # If len(changed_manufacturer_data) > 1 it means we switched
            # ble adapters so we do not know which data is the latest
            # and we need to wait for the next update.
            return
        last_id = list(changed_manufacturer_data)[-1]

        changed = changed_manufacturer_data[last_id]
        if not changed.startswith(b"\x01\x01\xa4\xc1") and not changed.startswith(
            b"\x01\x05\xa4\xc1"
        ):
            return
        data = int(last_id).to_bytes(2, byteorder="little") + changed
        device_id = data[3]
        device_type = service_info.name or DEVICE_TYPES.get(device_id) or DEFAULT_MODEL
        name = device_type
        self.set_precision(2)
        self.set_device_type(device_id)
        self.set_title(f"{name} {short_address(service_info.address)}")
        self.set_device_name(f"{name} {short_address(service_info.address)}")
        self.set_device_manufacturer("SensorPro")
        xvalue = data[10:17]
        (volt, temp, humi, batt) = unpack(">HhHB", xvalue)
        self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, batt)
        self.update_predefined_sensor(SensorLibrary.TEMPERATURE__CELSIUS, temp / 100)
        self.update_predefined_sensor(SensorLibrary.HUMIDITY__PERCENTAGE, humi / 100)
        self.update_predefined_sensor(
            SensorLibrary.VOLTAGE__ELECTRIC_POTENTIAL_VOLT, volt / 100
        )
