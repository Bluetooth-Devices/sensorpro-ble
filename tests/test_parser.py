from uuid import UUID

from bleak.backends.device import BLEDevice
from bluetooth_data_tools import monotonic_time_coarse
from bluetooth_sensor_state_data import SensorUpdate
from habluetooth import BluetoothServiceInfoBleak
from sensor_state_data import (
    DeviceKey,
    SensorDescription,
    SensorDeviceClass,
    SensorDeviceInfo,
    SensorValue,
    Units,
)

from sensorpro_ble.parser import SensorProBluetoothDeviceData


def make_bluetooth_service_info(  # noqa: PLR0913
    name: str,
    manufacturer_data: dict[int, bytes],
    service_uuids: list[str],
    address: str,
    rssi: int,
    service_data: dict[UUID, bytes],
    source: str,
    tx_power: int = 0,
    raw: bytes | None = None,
) -> BluetoothServiceInfoBleak:
    return BluetoothServiceInfoBleak(
        name=name,
        manufacturer_data=manufacturer_data,
        service_uuids=service_uuids,
        address=address,
        rssi=rssi,
        service_data=service_data,
        source=source,
        device=BLEDevice(
            name=name,
            address=address,
            details={},
            rssi=rssi,
        ),
        time=monotonic_time_coarse(),
        advertisement=None,
        connectable=True,
        tx_power=tx_power,
        raw=raw,
    )


def test_can_create():
    SensorProBluetoothDeviceData()


MFR_T201 = make_bluetooth_service_info(
    name="T201",
    address="aa:bb:cc:dd:ee:ff",
    rssi=-60,
    service_data={},
    manufacturer_data={
        43605: b"\x01\x01\xa4\xc18.\xcan\x01\x07\n\x02\x13\x9dd\x00\x01\x01\x01\xa4\xc18.\xcan\x01\x07\n\x02\x13\x9dd\x00\x01"
    },
    service_uuids=[],
    source="local",
)

MFR_T301 = make_bluetooth_service_info(
    name="T301",
    address="aa:bb:cc:dd:ee:ff",
    rssi=-60,
    service_data={},
    manufacturer_data={43605: b"\x01\x05\xa4\xc18\x1aWv\x01\x07\tV\x17\x0ca\x00\x01"},
    service_uuids=[],
    source="local",
)

MFR_T301_RAW = make_bluetooth_service_info(
    name="T301",
    address="aa:bb:cc:dd:ee:ff",
    rssi=-60,
    service_data={},
    manufacturer_data={44: b""},
    service_uuids=[],
    source="local",
    raw=b"\x14\xffU\xaa\x01\x05\xa4\xc18\x1aWv\x01\x07\tV\x17\x0ca\x00\x01",
)

MFR_T301_NO_NAME = make_bluetooth_service_info(
    name="",
    address="aa:bb:cc:dd:ee:ff",
    rssi=-60,
    service_data={},
    manufacturer_data={43605: b"\x01\x05\xa4\xc18\x1aWv\x01\x07\tV\x17\x0ca\x00\x01"},
    service_uuids=[],
    source="local",
)


def test_t201():
    parser = SensorProBluetoothDeviceData()
    update = parser.update(MFR_T201)
    assert update == SensorUpdate(
        title="T201 EEFF",
        devices={
            None: SensorDeviceInfo(
                name="T201 EEFF",
                model=1,
                manufacturer="SensorPro",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="voltage", device_id=None): SensorDescription(
                device_key=DeviceKey(key="voltage", device_id=None),
                device_class=SensorDeviceClass.VOLTAGE,
                native_unit_of_measurement=Units.ELECTRIC_POTENTIAL_VOLT,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=SensorDeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=SensorDeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
        },
        entity_values={
            DeviceKey(key="voltage", device_id=None): SensorValue(
                device_key=DeviceKey(key="voltage", device_id=None),
                name="Voltage",
                native_value=2.63,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=50.21,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-60,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=100,
            ),
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=25.62,
            ),
        },
        binary_entity_descriptions={},
        binary_entity_values={},
    )


def test_t301():
    parser = SensorProBluetoothDeviceData()
    update = parser.update(MFR_T301)
    assert update == SensorUpdate(
        title="T301 EEFF",
        devices={
            None: SensorDeviceInfo(
                name="T301 EEFF",
                model=5,
                manufacturer="SensorPro",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="voltage", device_id=None): SensorDescription(
                device_key=DeviceKey(key="voltage", device_id=None),
                device_class=SensorDeviceClass.VOLTAGE,
                native_unit_of_measurement=Units.ELECTRIC_POTENTIAL_VOLT,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=SensorDeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=SensorDeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="voltage", device_id=None): SensorValue(
                device_key=DeviceKey(key="voltage", device_id=None),
                name="Voltage",
                native_value=2.63,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=59.0,
            ),
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=23.9,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=97,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-60,
            ),
        },
        binary_entity_descriptions={},
        binary_entity_values={},
    )


def test_t301_raw():
    parser = SensorProBluetoothDeviceData()
    update = parser.update(MFR_T301_RAW)
    assert update == SensorUpdate(
        title="T301 EEFF",
        devices={
            None: SensorDeviceInfo(
                name="T301 EEFF",
                model=5,
                manufacturer="SensorPro",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="voltage", device_id=None): SensorDescription(
                device_key=DeviceKey(key="voltage", device_id=None),
                device_class=SensorDeviceClass.VOLTAGE,
                native_unit_of_measurement=Units.ELECTRIC_POTENTIAL_VOLT,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=SensorDeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=SensorDeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="voltage", device_id=None): SensorValue(
                device_key=DeviceKey(key="voltage", device_id=None),
                name="Voltage",
                native_value=2.63,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=59.0,
            ),
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=23.9,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=97,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-60,
            ),
        },
        binary_entity_descriptions={},
        binary_entity_values={},
    )


def test_t301_passive():
    parser = SensorProBluetoothDeviceData()
    update = parser.update(MFR_T301_NO_NAME)
    assert update == SensorUpdate(
        title="T301 EEFF",
        devices={
            None: SensorDeviceInfo(
                name="T301 EEFF",
                model=5,
                manufacturer="SensorPro",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="voltage", device_id=None): SensorDescription(
                device_key=DeviceKey(key="voltage", device_id=None),
                device_class=SensorDeviceClass.VOLTAGE,
                native_unit_of_measurement=Units.ELECTRIC_POTENTIAL_VOLT,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=SensorDeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=SensorDeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="voltage", device_id=None): SensorValue(
                device_key=DeviceKey(key="voltage", device_id=None),
                name="Voltage",
                native_value=2.63,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=59.0,
            ),
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=23.9,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=97,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-60,
            ),
        },
        binary_entity_descriptions={},
        binary_entity_values={},
    )
