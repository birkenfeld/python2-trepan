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
import sys

# Our local modules
from import_relative import import_relative

import_relative('lib', '...', 'pydbgr')
Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns    = import_relative('cmdfns', top_name='pydbgr')
Mfile      = import_relative('file', '...lib', 'pydbgr')
Mmisc      = import_relative('misc', '...', 'pydbgr')
Mbreak     = import_relative('break', '.', 'pydbgr')

class TempBreakCommand(Mbase_cmd.DebuggerCommand):
    """tbreak [LOCATION] [if CONDITION]]

With a line number argument, set a break there in the current file.
With a function name, set a break at first executable line of that
function.  Without argument, set a breakpoint at current location.  If
a second argument is "if", subequent arguments given an expression
which must evaluate to true before the breakpoint is honored.

The location line number may be prefixed with a filename or module
name and a colon. Files is searched for using sys.path, adnd the .py
suffix may be omitted in the file name.

Examples:
   tbreak     # Break where we are current stopped at
   tbreak 10  # Break on line 10 of the file we are currently stopped at
   tbreak os.path.join # Break in function os.path.join
   tbreak os.path:45   # Break on line 45 of os.path
   tbreak myfile.py:45 # Break on line 45 of myfile.py
   tbreak myfile:45    # Same as above.
"""

    category      = 'breakpoints'
    min_args      = 0
    max_args      = None
    name_aliases  = ('tbreak',)
    need_stack    = True
    short_help    = 'Set temporary breakpoint at specified line or function'

    def run(self, args):
        func, filename, lineno, condition = Mbreak.parse_break_cmd(self,
                                                                   args[1:])
        Mbreak.set_break(self, func, filename, lineno, condition, True, args)
        return 

if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = TempBreakCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()

    print Mbreak.parse_break_cmd(command, [])
    print Mbreak.parse_break_cmd(command, ['10'])
    print Mbreak.parse_break_cmd(command, [__file__ + ':10'])
    def foo():
        return 'bar'
    print Mbreak.parse_break_cmd(command, ['foo'])
    print Mbreak.parse_break_cmd(command, ['os.path'])
    print Mbreak.parse_break_cmd(command, ['os.path', '5+1'])
    print Mbreak.parse_break_cmd(command, ['os.path.join'])
    print Mbreak.parse_break_cmd(command, ['if', 'True'])
    print Mbreak.parse_break_cmd(command, ['foo', 'if', 'True'])
    print Mbreak.parse_break_cmd(command, ['os.path:10', 'if', 'True'])
    command.run(['tbreak'])
    command.run(['tbreak', 'command.run'])
    command.run(['tbreak', '10'])
    command.run(['tbreak', __file__ + ':10'])
    command.run(['tbreak', 'foo'])
    pass