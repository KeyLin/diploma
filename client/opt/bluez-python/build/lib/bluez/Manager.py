# Manager.py
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

import Adapter
import Agent
import errors
from utils import raise_dbus_error
from BaseInterface import BaseInterface

class Manager(BaseInterface):

    '''
    Pass the name of the mainloop as a string to __init__.
    The mainloop support could not be changed after the first init of Manager.
    Supported mainloops are gobject, pyqt4 and ecore, use your perferred one.
    And gobject is supported by dbus-python natively.
    If you wanna use pyqt4 or ecore, make sure you have python bindings for them.
    '''

    _mainloop_support = ''

    @raise_dbus_error
    def __init__(self, mainloop):
        if Manager._mainloop_support == '':
            self.__setup_event_loop(mainloop)
        elif Manager._mainloop_support != mainloop:
            raise errors.DBusMainLoopAlreadyExistsError("Already have " + Manager._mainloop_support)
        super(Manager, self).__init__('org.bluez.Manager', '/')
    # __init__

    def __setup_event_loop(self, mainloop):
        def raise_mainloop_not_found(mainloop):
            raise errors.DBusMainLoopModuleNotFoundError('Can not find mofule for ' + mainloop)
        def parse_gobject_mainloop(mainloop):
            try:
                import dbus.mainloop.glib
            except ImportError:
                raise_mainloop_not_found(mainloop)
            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
            return True

        def parse_pyqt4_mainloop(mainloop):
            try:
                import dbus.mainloop.qt
            except ImportError:
                raise_mainloop_not_found(mainloop)
            dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
            return True

        def parse_ecore_mainloop(mainloop):
            try:
                import e_dbus
            except ImportError:
                raise_mainloop_not_found(mainloop)
            e_dbus.DBusEcoreMainLoop(set_as_default=True)
            return True

        _supported_mainloops = {'gobject':parse_gobject_mainloop,
                                'pyqt4':parse_pyqt4_mainloop,
                                'ecore':parse_ecore_mainloop}
        if (not isinstance(mainloop, str)) or (mainloop not in _supported_mainloops):
            raise errors.DBusMainLoopNotSupportedError('Supported mainloops are gobject, pyqt4 and ecore')
        else:
            parse_mainloop = _supported_mainloops.get(mainloop)
            if parse_mainloop(mainloop):
                Manager._mainloop_support = mainloop
    # __setup_event_loop

    @raise_dbus_error
    def GetProperties(self):
        return self.GetInterface().GetProperties()
    # GetProperties

    @raise_dbus_error
    def DefaultAdapter(self):
        obj_path = self.GetInterface().DefaultAdapter()
        return Adapter.Adapter(obj_path)
    # DefaultAdapter

    @raise_dbus_error
    def FindAdapter(self, pattern):
        obj_path = self.GetInterface().FindAdapter(pattern)
        return Adapter.Adapter(obj_path)
    # FindAdapter

    @raise_dbus_error
    def ListAdapters(self):
        obj_paths = self.GetInterface().ListAdapters()
        adapters = []
        for obj_path in obj_paths:
            adapters.append(Adapter.Adapter(obj_path))
        return adapters
    # ListAdapters

    def CreateAgent(self, cls=Agent.Agent, obj_path='/org/bluez/Agent'):
        '''
        Paramater cls should be a custom sub-class of Agent.
        Paramater obj_path is the dbus object path for the agent, should start with '/'.
        Returns an instance of specified cls.
        '''
        if not issubclass(cls, Agent.Agent):
            raise TypeError('Expecting a subclass of Agent')
        return cls(obj_path)
    # CreateAgent
# Manager
