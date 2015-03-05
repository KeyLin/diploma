# Adapter.py
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

import dbus
import types

import Device
import Agent
import errors
from utils import raise_dbus_error
from utils import raise_type_error
from BaseInterface import BaseInterface

class Adapter(BaseInterface):

    @raise_dbus_error
    def __init__(self, obj_path):
        super(Adapter, self).__init__('org.bluez.Adapter', obj_path)
    # __init__

    @raise_dbus_error
    def GetProperties(self):
        return self.GetInterface().GetProperties()
    # GetProperties

    @raise_dbus_error
    def SetProperty(self, name, value):
        if type(value) == types.IntType:
            value = dbus.UInt32(value)
        self.GetInterface().SetProperty(name, value)
    # SetProperty

    @raise_dbus_error
    def RequestSession(self):
        self.GetInterface().RequestSession()
    # RequestSession

    @raise_dbus_error
    def ReleaseSession(self):
        self.GetInterface().ReleaseSession()
    # ReleaseSession

    @raise_dbus_error
    def StartDiscovery(self):
        self.GetInterface().StartDiscovery()
    # StartDiscovery

    @raise_dbus_error
    def StopDiscovery(self):
        self.GetInterface().StopDiscovery()
    # StopDiscovery

    @raise_dbus_error
    def FindDevice(self, address):
        obj_path = self.GetInterface().FindDevice(address)
        return Device.Device(obj_path)
    # FindDevice

    @raise_dbus_error
    def ListDevices(self):
        obj_paths = self.GetInterface().ListDevices()
        devices = []
        for obj_path in obj_paths:
            devices.append(Device.Device(obj_path))
        return devices
    # ListDevices

    @raise_dbus_error
    def CreateDevice(self, address):
        obj_path = self.GetInterface().CreateDevice(address)
        return Device.Device(obj_path)
    # CreateDevice

    @raise_dbus_error
    def CreatePairedDevice(self, address, agent, capability='', reply_handler=None, error_handler=None):
        def reply_handler_wrapper(obj_path):
            if not callable(reply_handler):
                return
            reply_handler(Device.Device(obj_path))

        def error_handler_wrapper(exception):
            exception = errors.parse_dbus_error(exception)
            if not callable(error_handler):
                raise exception
            error_handler(exception)

        raise_type_error(agent, Agent.Agent)
        if reply_handler is None and error_handler is None:
            obj_path = self.GetInterface().CreatePairedDevice(address, agent.GetObjectPath(), capability)
            return Device.Device(obj_path)
        else:
            self.GetInterface().CreatePairedDevice(address,
                                                   agent.GetObjectPath(),
                                                   capability,
                                                   reply_handler=reply_handler_wrapper,
                                                   error_handler=error_handler_wrapper)
            return None
    # CreatePairedDevice

    @raise_dbus_error
    def CancelDeviceCreation(self, address):
        self.GetInterface.CancelDeviceCreation(address)
    # CancelDeviceCreation

    @raise_dbus_error
    def RemoveDevice(self, device):
        raise_type_error(device, Device.Device)
        self.GetInterface().RemoveDevice(device.GetObjectPath())
    # RemoveDevice

    @raise_dbus_error
    def RegisterAgent(self, agent, capability=''):
        raise_type_error(agent, Agent.Agent)
        self.GetInterface().RegisterAgent(agent.GetObjectPath(), capability)
    # RegisterAgent

    @raise_dbus_error
    def UnregisterAgent(self, agent):
        raise_type_error(agent, Agent.Agent)
        self.GetInterface().UnregisterAgent(agent.GetObjectPath())
    # UnregisterAgent
# Adapter
