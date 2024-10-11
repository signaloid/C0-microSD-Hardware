#!/usr/bin/env python3

# Copyright (c) 2024, Signaloid.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import smbus
import RPi.GPIO as GPIO
from typing import Union, Tuple
import time


class SDDev:
    """
        Top level class with SDDev constants
    """

    MCP3426_I2C_ADDRESS = 0x68

    # Reference voltage of the ADC (Volts)
    MCP3426_VREF = 2.048

    # The resistance of the shunt resistor (Ohms). This is the same for
    # both channels
    SDDEV_RSENSE = 0.5

    # Current measurement opamp gain values
    SDDEV_SD_OPAMP_GAIN = 20.1
    SDDEV_USD_OPAMP_GAIN = 201

    # Full-size SD and microSD supply voltage
    SDDEV_SD_USD_VOLTAGE = 3.3

    # Reset microSD controller GPIO pin
    USD_RST_N = 6

    # Reset full-size SD controller GPIO pin
    SD_RST_N = 5

    # Reset USB hub
    USB_HUB_RST = 22

    # Power enable GPIO pin for both microSD and full-size SD slots
    SD_PWR_EN = 27

    # Full-size SD slot card-detect GPIO pin
    SD_CD_N = 15

    # microSD slot card-detect GPIO pin. This works using the onboard current
    # sensing circuitry and triggers when a microSD card draws more than 1mA
    USD_CD = 14


class SDDevADCInterface(SDDev):
    """Communication interface for C0-microSD.

    This class provides basic functionality for interfacing with the
    Signaloid C0-microSD.
    """

    def __init__(
            self,
            target_smbus_number: int,
            channel: int = 1,
            conversion_mode: int = 1,
            sample_rate_bits: int = 12,
            pga_gain: int = 4
            ) -> None:
        super().__init__()

        self.target_smbus_number = target_smbus_number

        self.channel: Union[None, int] = None
        self.conversion_mode: Union[None, int] = None
        self.sample_rate_bits: Union[None, int] = None
        self.pga_gain: Union[None, int] = None

        # Calculated per configuration
        self.channel_gain: Union[None, float] = None
        self.max_adc_value: Union[None, float] = None
        self.current_sense_resolution: Union[None, float] = None
        self.max_current_sense: Union[None, float] = None

        # Initialize MSB mask and configuration register
        self.input_MSB_mask = 0x00
        self.configuration_register = 0x00

        self.bus = smbus.SMBus(target_smbus_number)

        self.configure(channel, conversion_mode, sample_rate_bits, pga_gain)

    def configure(
            self,
            channel: int,
            conversion_mode: int,
            sample_rate_bits: int,
            pga_gain: int
            ) -> None:
        """
        Configure object and ADC. This function also calculates the
        channel gain, max_adc_value, current_sense_resolution, and
        max_current_sense parameters.

        Args:
            channel (int):          The measurement channel of the ADC
                                    (0 or 1).
            conversion_mode (int):  The ADC conversion mode
                                    (0 or 1).
            sample_rate_bits (int): The resolution of the ADC
                                    (12, 14, or 16).
            pga_gain (int):         The gain of the Programmable Gain Amplifier
                                    (1, 2, 4, or 8).
        """

        self.channel = channel
        self.conversion_mode = conversion_mode
        self.sample_rate_bits = sample_rate_bits
        self.pga_gain = pga_gain

        # Gain is different for channel 0 and channel 1:
        if self.channel == 0:
            self.channel_gain = self.SDDEV_SD_OPAMP_GAIN
        else:
            self.channel_gain = self.SDDEV_USD_OPAMP_GAIN

        # Maximum value for the given ADC resolution.
        # sample_rate_bits -1 since the ADC returns signed integer
        self.max_adc_value = 2**(self.sample_rate_bits - 1) - 1

        self.current_sense_resolution = (
            (self.MCP3426_VREF) /
            (
                self.max_adc_value *
                self.SDDEV_RSENSE *
                self.channel_gain *
                self.pga_gain
            )
        )

        # Calculate the maximum input voltage to the ADC
        max_input_voltage = self.MCP3426_VREF / self.pga_gain

        # Calculate the maximum current
        self.max_current_sense = max_input_voltage / (
            self.SDDEV_RSENSE * self.channel_gain)

        self._configure_adc()

    def _configure_adc(self) -> None:
        """
        Construct and write configuration register to ADC
        """
        configuration_register = 0x00

        # Configuration register topology
        # - bit 7:    0
        # - bit 6-5:  Channel
        # - bit 4:    Conversion mode
        # - bit 3-2:  Sample rate bits
        # - bit 1-0:  Programmable Gain Amplifier

        # Add checks
        if self.channel == 0:
            configuration_register = configuration_register
        elif self.channel == 1:
            configuration_register = configuration_register | 0x20
        else:
            raise IndexError("Invalid channel index")

        if self.conversion_mode == 0:
            configuration_register = configuration_register
        elif self.conversion_mode == 1:
            configuration_register = configuration_register | 0x10
        else:
            raise ValueError("Invalid conversion_mode value")

        if self.sample_rate_bits == 12:
            configuration_register = configuration_register
            self.input_MSB_mask = 0x7F
        elif self.sample_rate_bits == 14:
            configuration_register = configuration_register | 0x04
            self.input_MSB_mask = 0x1F
        elif self.sample_rate_bits == 16:
            configuration_register = configuration_register | 0x08
            self.input_MSB_mask = 0x07
        else:
            raise ValueError("Invalid sample_rate_bits value")

        if self.pga_gain == 1:
            configuration_register = configuration_register
        elif self.pga_gain == 2:
            configuration_register = configuration_register | 0x01
        elif self.pga_gain == 4:
            configuration_register = configuration_register | 0x02
        elif self.pga_gain == 8:
            configuration_register = configuration_register | 0x03
        else:
            raise ValueError("Invalid pga_gain value")

        self.configuration_register = configuration_register
        self.bus.write_byte(
            self.MCP3426_I2C_ADDRESS,
            self.configuration_register)

    def adc_to_current(
            self,
            adc_value: int
            ) -> float:
        """
        Convert ADC value to current and calculate the min/max current sense
        range and resolution.

        Args:
            adc_value (int): The digital output value from the ADC.

        Returns:
            float: Measured current (Amps)
        """

        # Calculate the measured current
        current = adc_value * self.current_sense_resolution

        return current

    def convert_i2c_bytes_to_adc(self, data: bytes) -> Tuple[bool, int]:
        """
        Convert bytes to ADC value. This function also determines whether
        the received data are valid (from new conversion).

        Args:
            data (bytes): The received bytes (3) from ADC

        Returns:
            tuple containing

            - data_ready (bool): ADC conversion ready
            - adc_value (int): ADC value
        """

        # MSB of data[0] is sign bit
        # 256 is 8 bits shift left
        data_ready = not bool((data[2] >> 7) & 1)

        if (data[0] & 0x80):
            adc_value = -((data[0] & self.input_MSB_mask) * 256 + data[1])
        else:
            adc_value = data[0] * 256 + data[1]

        return data_ready, adc_value

    def read_raw_i2c_data(self) -> bytes:
        """
        Read ADC byte data

        Returns:
            bytes: Received data from ADC
        """
        data = self.bus.read_i2c_block_data(
            self.MCP3426_I2C_ADDRESS,
            self.configuration_register,
            3
        )
        return bytes(data)

    def read_raw_ADC_data(self, blocking=True) -> int:
        """
        Read raw ADC data

        Args:
            blocking (bool): Block and continuously read data from ADC until
                             valid conversion is detected.

        Returns:
            int: Integer representation of the ADC output
        """
        while True:
            data = self.read_raw_i2c_data()
            data_ready, adc_value = self.convert_i2c_bytes_to_adc(data)
            if data_ready or not blocking:
                break
        return adc_value

    def read_converted_current_measurement(self) -> float:
        """
        Read ADC data and convert to current

        Returns:
            float: Current measurement (Amps)
        """
        converted_current_measurement =\
            self.adc_to_current(self.read_raw_ADC_data())
        return converted_current_measurement


class SDDevController(SDDev):
    # Seconds to delay between a power cycle event
    POWER_CYCLE_DELAY_BETWEEN = 1
    # Seconds to delay after a power cycle event
    POWER_CYCLE_DELAY_AFTER = 5

    def __init__(self):
        super().__init__()

    def reset_controllers(
            self,
            reset_usb_hub: bool = False,
            reset_sd_controller: bool = False,
            reset_microsd_controller: bool = False,
            power_cycle_sd_cards: bool = False) -> None:

        """
            Reset USB and SD controllers, and power cycle the sd card slots.

            Args:
                reset_usb_hub (bool): Reset onboard USB hub
                reset_sd_controller (bool): Reset full-size SD controller
                reset_microsd_controller (bool): Reset microSD controller
                power_cycle_sd_cards (bool): Power-cycle full-size SD
                                             and microSD cards
        """

        # Use BCM GPIO numbering
        GPIO.setmode(GPIO.BCM)

        if reset_usb_hub:
            GPIO.setup(self.USB_HUB_RST, GPIO.OUT)
            GPIO.output(self.USB_HUB_RST, GPIO.HIGH)
        if reset_sd_controller:
            GPIO.setup(self.SD_RST_N, GPIO.OUT)
            GPIO.output(self.SD_RST_N, GPIO.LOW)
        if reset_microsd_controller:
            GPIO.setup(self.USD_RST_N, GPIO.OUT)
            GPIO.output(self.USD_RST_N, GPIO.LOW)
        if power_cycle_sd_cards:
            GPIO.setup(self.SD_PWR_EN, GPIO.OUT)
            GPIO.output(self.SD_PWR_EN, GPIO.LOW)

        time.sleep(self.POWER_CYCLE_DELAY_BETWEEN)

        if reset_usb_hub:
            GPIO.output(self.USB_HUB_RST, GPIO.LOW)
        if reset_sd_controller:
            GPIO.output(self.SD_RST_N, GPIO.HIGH)
        if reset_microsd_controller:
            GPIO.output(self.USD_RST_N, GPIO.HIGH)
        if power_cycle_sd_cards:
            GPIO.output(self.SD_PWR_EN, GPIO.HIGH)

        time.sleep(self.POWER_CYCLE_DELAY_AFTER)

        GPIO.cleanup()

    def refresh_sd_cards(self) -> None:
        """
        Refresh sd cards. Reset SD and microSD controllers and
        power cycles the sd cards.
        """
        self.reset_controllers(False, True, True, True)

    def detect_cards(self) -> Tuple[bool, bool]:
        """
        Detect inserted full-size SD and microSD cards

        Returns:
            tuple containing

            - full_size_sd_detect (bool): Full-size SD card detected
            - micro_sd_detect (book): MicroSD card detected
        """
        # Use BCM GPIO numbering
        GPIO.setmode(GPIO.BCM)

        # Set up input pins
        GPIO.setup(self.SD_CD_N, GPIO.IN)
        GPIO.setup(self.USD_CD, GPIO.IN)

        full_size_sd_detect = not GPIO.input(self.SD_CD_N)
        micro_sd_detect = bool(GPIO.input(self.USD_CD))

        GPIO.cleanup()

        return full_size_sd_detect, micro_sd_detect
