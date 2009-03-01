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
from import_relative import import_relative
import tracer

# Our local modules
Mbase_cmd  = import_relative('base_cmd')
cmdfns     = import_relative('cmdfns')

class StepCommand(Mbase_cmd.DebuggerCommand):

    category      = 'running'
    min_args      = 0
    max_args      = None
    execution_set = ['Running']
    name_aliases  = ('step', 'step+', 'step-', 'step>', 'step<', 'step!',
                     's', 's+', 's-', 's<', 's>', 's!')
    need_stack    = True
    short_help    = 'Step program (possibly entering called functions)'

    def run(self, args):
        """step[+|-|<|>|!] [EVENT-NAME...] [count]
Execute the current line, stopping at the next event.

With an integer argument, step that many times.

EVENT-NAME... is list of an event name which is one on 'call',
'return', 'line', 'exception' 'c-call', 'c-return' or 'c-exception'.
If specified, only those stepping events will be considered. If no
list of event names is given, then any event triggers a stop when the
count is 0.

There is however another way to specify an *single* EVENT-NAME, by
suffixing one of the symbols '<', '>', or '!' after the command or on
an alias of that.  A suffix of '+' on a command or an alias forces a
move to another line, while a suffix of '-' disables this requirement.
A suffix of '>' will continue until the next call. ('finish' will run
run until the return for that call.)

If no suffix is given, the debugger setting 'different-line'
determines this behavior.

Examples: 
  step        # step 1 event, *any* event 
  step 1      # same as above
  step 5/5+0  # same as above
  step line   # step only line events
  step call   # step only call events
  step>       # same as above
  step call line # Step line *and* call events

Related and similar is the 'next' command.  See also the commands:
'skip', 'jump' (there's no "hop" yet), "continue", "return" and
"finish" for other ways to progress execution.
"""
        step_events  = []
        if args[0][-1] == '>':
            step_events  = ['call']
        elif args[0][-1] == '<':
            step_events  = ['return']
        elif args[0][-1] == '!':
            step_events  = ['exception']
            pass
        if len(args) <= 1:
            self.proc.debugger.core.step_ignore = 0
        else:
            pos = 1
            while pos < len(args):
                arg = args[pos]
                if arg in tracer.ALL_EVENT_NAMES:
                    step_events.append(arg)
                else:
                    break
                pos += 1
                pass
            if pos == len(args) - 1:
                try:
                    # 0 means stop now or step 1, so we subtract 1.
                    self.core.step_ignore = \
                        cmdfns.get_pos_int(self.errmsg, args[pos], default=1,
                                           cmdname='step') - 1
                except ValueError:
                    return False
            elif pos != len(args):
                self.errmsg("Invalid additional parameters %s" 
                            % ' '.join(args[pos]))
                return False
            pass

        if [] == step_events: 
            self.core.step_events = None
        else:
            self.core.step_events = step_events
            pass

        self.core.different_line   = \
            cmdfns.want_different_line(args[0], self.settings['different'])
        self.core.stop_level       = None
        self.core.last_frame       = None
        self.core.stop_on_finish   = False
        self.proc.continue_running = True # Break out of command read loop
        return True
    pass

if __name__ == '__main__':
    from mock import MockDebugger
    d = MockDebugger()
    cmd = StepCommand(d.core.processor)
    for c in (['s', '5'],
              ['step', '1+2'],
              ['s', 'foo']):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print 'Execute result: %s' % result
        print 'step_ignore %d, continue_running: %s' % (d.core.step_ignore,
                                                        cmd.continue_running,)
        pass
    for c in (['s'], ['step+'], ['s-'], ['s!'], ['s>'], ['s<']): 
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print cmd.core.different_line
        pass
    pass