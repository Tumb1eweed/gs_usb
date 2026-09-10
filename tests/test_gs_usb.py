from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

from gs_usb.constants import GS_CAN_MODE_HW_TIMESTAMP, GS_CAN_MODE_NORMAL
from gs_usb.gs_usb import GsUsb


class TestGsUsbStart(TestCase):
    def make_device(self):
        usb_device = MagicMock()
        usb_device.is_kernel_driver_active.return_value = False

        device = GsUsb(usb_device)
        device.capability = SimpleNamespace(feature=GS_CAN_MODE_HW_TIMESTAMP)
        return device, usb_device

    @patch("gs_usb.gs_usb.platform.system", return_value="Darwin")
    def test_start_resets_usb_device_by_default(self, _system):
        device, usb_device = self.make_device()

        device.start(flags=GS_CAN_MODE_NORMAL | GS_CAN_MODE_HW_TIMESTAMP)

        usb_device.reset.assert_called_once_with()
        usb_device.ctrl_transfer.assert_called_once()

    @patch("gs_usb.gs_usb.platform.system", return_value="Darwin")
    def test_start_can_skip_usb_device_reset(self, _system):
        device, usb_device = self.make_device()

        device.start(
            flags=GS_CAN_MODE_NORMAL | GS_CAN_MODE_HW_TIMESTAMP,
            reset_device=False,
        )

        usb_device.reset.assert_not_called()
        usb_device.ctrl_transfer.assert_called_once()
