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
import threading
from import_relative import import_relative

# Our local modules
Mbase_cmd  = import_relative('base_cmd', top_name='pydbgr')
Mdebugger  = import_relative('debugger', '...', 'pydbgr')

class QuitCommand(Mbase_cmd.DebuggerCommand):
    """quit - gently terminate the debugged program.  

The program being debugged is aborted via a DebuggerQuit
exception. 

When the debugger from the outside (e.g. via a 'pydbgr' command), the
debugged program is contained inside a try block which handles the
DebuggerQuit exception.  However if you called the debugger was
started in the middle of a program, there might not be such an
exception handler; the debugged program still terminates but 
but generally with a traceback showing that exception. 

If the debugged program is threaded or worse threaded and deadlocked,
raising an exception in one thread isn't going to quit the
program. For this see 'exit' or 'kill' for more forceful termination
commands

Also, see 'run' and 'restart' for ways to restart the debugged
program.
"""

    category      = 'support'
    min_args      = 0
    max_args      = 0
    name_aliases  = ('quit', 'q',)
    need_stack    = False
    short_help    = 'Termintate the program - gently'

    def nothread_quit(self, arg):
        """ quit command when there's just one thread. """

        self.debugger.core.stop()
        self.debugger.core.execution_status = 'Quit command'
        raise Mdebugger.DebuggerQuit

    def threaded_quit(self, arg):
        """ quit command when several threads are involved. """
        self.msg("Quit for threading not fully done yet. Try 'kill'.")
        return False

    def run(self, args):
        threading_list = threading.enumerate()
        if (len(threading_list) == 1 and
            threading_list[0].getName() == 'MainThread'):
            # We just have a main thread so that's safe to quit
            return self.nothread_quit(args)
        else:
            return self.threaded_quit(args)
        pass

if __name__ == '__main__':
    mock = import_relative('mock')
    Mdebugger = import_relative('debugger', '...')
    d, cp = mock.dbg_setup()
    command = QuitCommand(cp)
    try: 
        command.run(['quit'])
    except Mdebugger.DebuggerQuit:
        print "A got 'quit' a exception. Ok, be that way - I'm going home."
        pass

    import threading

    class MyThread(threading.Thread):
        def run(self):
            command.run(['quit'])
            return
        pass

    t = MyThread()
    t.start()
    t.join()
    pass