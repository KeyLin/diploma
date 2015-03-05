# Device.py
#
# Copyright (C) 2008 Vinicius Gomes <vcgomes [at] gmail [dot] com>
# Copyright (C) 2008 Li Dongyang <Jerry87905 [at] gmail [dot] com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from utils import raise_dbus_error
from BaseInterface import BaseInterface

class Device(BaseInterface):

    @raise_dbus_error
    def __init__(self, obj_path):
        super(Device, self).__init__('org.bluez.Device', obj_path)
    # __init__

    @raise_dbus_error
    def GetProperties(self):
        return self.GetInterface().GetProperties()
    # GetProperties

    @raise_dbus_error
    def SetProperty(self, name, value):
        self.GetInterface().SetProperty(name, value)
    # SetProperty

    @raise_dbus_error
    def DiscoverServices(self, pattern):
        return self.GetInterface().DiscoverServices(pattern)
    # DiscoverServices

    @raise_dbus_error
    def CancelDiscovery(self):
        self.GetInterface().CancelDiscovery()
    # CancelDiscovery

    @raise_dbus_error
    def Disconnect(self):
        self.GetInterface().Disconnect()
    # Disconnect
# Device
