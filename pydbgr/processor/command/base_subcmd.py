# -*- coding: utf-8 -*-
#   Copyright (C) 2009 Rocky Bernstein
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#    02110-1301 USA.
"""A base class for debugger commands.

This file is the one module in this directory that isn't a real command
and commands.py needs to take care to avoid instantiating this class
and storing it as a list of known debugger commands.
"""

NotImplementedMessage = "This method must be overriden in a subclass"

# Note: don't end classname with Command (capital C) since cmdproc
# will think this a command name like QuitCommand 
#                                         ^
class DebuggerSubcommand():
    """Base Class for Debugger subcommands. We pull in some helper
    functions for command from module cmdfns."""

    in_list    = True  # Show item in help list of commands
    run_cmd    = True  # Run subcommand for those subcommands like "show"
                       # which append current settings to list output.
    min_abbrev = 1
    need_stack = False

    def __init__(self, cmd):
        """cmd contains the command object that this
        command is invoked through.  A debugger field gives access to
        the stack frame and I/O."""
        self.cmd = cmd

        # Convenience class access. We don't expect that any of these
        # will change over the course of the program execution like
        # errmsg(), msg(), and msg_nocr() might. (See the note below
        # on these latter 3 methods.)
        # 
        self.proc     = cmd.proc
        self.core     = cmd.core
        self.debugger = cmd.debugger
        self.settings = cmd.debugger.settings

        # By default the name of the subcommand will be the name of the
        # last part of module (e.g. "args" in "infos.args" or "basename"
        # in "shows.basename"). However it *is* possible for one to change
        # that -- perhaps one may want to put several subcommands into 
        # a single file. So in those cases, one will have to set self.name
        # accordingly by other means.
        self.name  = self.__module__.split('.')[-1]

        return

    def confirm(self, msg, default=False):
        """ Convenience short-hand for self.debugger.intf.confirm """
        return(self.debugger.intf[-1].confirm(msg, default))

    # Note for errmsg, msg, and msg_nocr we don't want to simply make
    # an assignment of method names like self.msg = self.debugger.intf.msg,
    # because we want to allow the interface (intf) to change 
    # dynamically. That is, the value of self.debugger may change
    # in the course of the program and if we made such an method assignemnt
    # we wouldn't pick up that change in our self.msg
    def errmsg(self, msg):
        """ Convenience short-hand for self.debugger.intf[-1].errmsg """
        return(self.debugger.intf[-1].errmsg(msg))
               
    def msg(self, msg):
        """ Convenience short-hand for self.debugger.intf[-1].msg """
        return(self.debugger.intf[-1].msg(msg))
               
    def msg_nocr(self, msg):
        """ Convenience short-hand for self.debugger.intf[-1].msg_nocr """
        return(self.debugger.intf[-1].msg_nocr(msg))

    name_aliases = ('YourCommandName', 'alias1', 'alias2..',)

        
    def run(self):
        """ The method that implements the debugger command.
        Help on the command comes from the docstring of this method.
        """
        raise NotImplementedError, NotImplementedMessage

    pass

from import_relative import *
Mcmdfns = import_relative('cmdfns', '.', 'pydbgr')

class DebuggerSetBoolSubcommand(DebuggerSubcommand):
    def run(self, args):
        Mcmdfns.run_set_bool(self, args)
        return

    def summary_help(self, subcmd_name, subcmd):
        return self.msg_nocr("%-12s: " % self.short_help)
    pass

class DebuggerShowIntSubcommand(DebuggerSubcommand):
    def run(self, args):
        if hasattr(self, 'short_help'):
            short_help = self.short_help
        else:
            short_help = self.__doc__[5:].capitalize()
            pass
        Mcmdfns.run_show_int(self, short_help)
        return

class DebuggerShowBoolSubcommand(DebuggerSubcommand):
    def run(self, args):
        Mcmdfns.run_show_bool(self, self.__doc__[5:].capitalize())
        return

if __name__ == '__main__':
    import os, sys
    from import_relative import *
    mock = import_relative('mock')
    d, cp = mock.dbg_setup()
    dd = DebuggerSubcommand(cp.name2cmd['quit'])