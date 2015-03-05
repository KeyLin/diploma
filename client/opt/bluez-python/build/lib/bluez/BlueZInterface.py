# BlueZInterface.py
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

from utils import raise_type_error

class BlueZInterface(object):

    def __init__(self, interface_name, obj_path):
        self.__obj_path = obj_path
        self.__interface_name = interface_name
        self.__bus = dbus.SystemBus()
        self.__dbus_proxy = self.__bus.get_object('org.bluez', obj_path, follow_name_owner_changes=True)
        self.__interface = dbus.Interface(self.__dbus_proxy, interface_name)
        try:
            self._properties = self.__interface.GetProperties()
            self.__bus.add_signal_receiver(self._update_property,
                                           "PropertyChanged",
                                           interface_name,
                                           "org.bluez",
                                           obj_path)
        except dbus.exceptions.DBusException:
            self._properties = {}
    # __init__

    def _update_property(self, name, value):
        self._properties[name] = value
    # _update_property

    def __getattr__(self, name):
        if not name in self._properties:
            raise AttributeError("'%s' object has no attribute '%s'"
                                 % (self.__class__.__name__, name) )
        return self._properties[name]
    # __getattr__

    def GetObjectPath(self):
        return self.__obj_path
    # GetObjectPath

    def GetInterface(self):
        return self.__interface
    # GetInterface

    def GetInterfaceName(self):
        return self.__interface_name
    # GetInterfaceName

    def HandleSignal(self, handler, signal):
        '''
        The handler function will be called when specific signal is emitted.
        For available signals of each interface, check BlueZ4 documents.
        '''
        raise_type_error(handler, types.FunctionType)
        raise_type_error(signal, types.StringType)
        self.__bus.add_signal_receiver(handler,
                                       signal,
                                       self.__interface_name,
                                       'org.bluez',
                                       self.__obj_path)
    # HandleSignal
# BlueZInterface
