# Agent.py
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

import inspect
import dbus
import dbus.service
import errors

__SIGNATURES__ = {'Release':('', ''),
                  'RequestPinCode':('o', 's'),
                  'RequestPasskey':('o', 'u'),
                  'DisplayPasskey':('ou', ''),
                  'RequestConfirmation':('ou', ''),
                  'Authorize':('os', ''),
                  'ConfirmModeChange':('s', ''),
                  'Cancel':('', '')}

def AgentMethod(func):
    '''
    The decorator for customizing the agent methods.
    To use async callbacks, add two extra parameters for
    success callback and error callback in the def of the agent method.
    '''
    global __SIGNATURES__
    try:
        signatures = __SIGNATURES__[func.__name__]
    except KeyError:
        raise errors.BluezUnavailableAgentMethodError('method name ' + func.__name__ + ' unavailable for agent')
    args = inspect.getargspec(func)[0]
    if len(args) - len(signatures[0]) == 3:
        async_callbacks = (args[-2], args[-1])
    else:
        async_callbacks = None
    warp = dbus.service.method('org.bluez.Agent',
                               in_signature=signatures[0],
                               out_signature=signatures[1],
                               async_callbacks=async_callbacks)
    return warp(func)
# AgentMethod

class Agent(dbus.service.Object):

    '''
    Inherit from this class and use AgentMethod decorator
    to customize the methods.
    The simple-agent is provided by default.
    '''

    def __init__(self, obj_path):
        self.__obj_path = obj_path
        dbus.service.Object.__init__(self, dbus.SystemBus(), obj_path)
    # __init__

    def GetObjectPath(self):
        '''Returns the dbus object path of the agent.'''
        return self.__obj_path
    # GetObjectPath

    @AgentMethod
    def Release(self):
        print "Release"
    # Release

    @AgentMethod
    def RequestPinCode(self, device):
        print "RequestPinCode (%s)" % (device)
        return raw_input("Enter PIN Code:")
    # RequestPinCode

    @AgentMethod
    def RequestPasskey(self, device):
        print "RequestPasskey (%s)" % (device)
        passkey = raw_input("Enter Passkey:")
        return dbus.UInt32(passkey)
    # RequestPasskey

    @AgentMethod
    def DisplayPasskey(self, device, passkey):
        print "DisplayPasskey (%s, %d)" % (device, passkey)
    # DisplayPasskey

    @AgentMethod
    def RequestConfirmation(self, device, passkey):
        print "RequestConfirmation (%s, %d)" % (device, passkey)
        confirm = raw_input("Confirm passkey (y/n): ")
        if confirm == 'y':
            return
        raise errors. DBusAuthenticationRejectedError("Passkey doesn't match")
    # RequestConfirmation

    @AgentMethod
    def Authorize(self, device, uuid):
        print "Authorize (%s, %s)" % (device, uuid)
    # Authorize

    @AgentMethod
    def ConfirmModeChange(self, mode):
        print "ConfirmModeChange (%s)" % (mode)
    # ConfirmModeChange

    @AgentMethod
    def Cancel(self):
        print "Cancel"
    # Cancel
# Agent
