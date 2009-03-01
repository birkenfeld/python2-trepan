#!/usr/bin/env python
'Unit test for the debugger pydbgrcore breakpoint'
import operator, os, sys, unittest
from import_relative import *

breakpoint = import_relative('lib.breakpoint', '...pydbgr')

class TestBreakpoint(unittest.TestCase):
    
    def test_breakpoint(self):
        'Test breakpoint'
        bpmgr = breakpoint.BreakpointManager()
        self.assertEqual(0, bpmgr.last())
        bp = bpmgr.add_breakpoint('foo', 5)
        self.assertEqual('1   breakpoint   keep yes   at foo:5', str(bp))
        self.assertEqual(True, bp.enabled)
        bp.disable()
        self.assertEqual('1   breakpoint   keep no    at foo:5', str(bp))
        self.assertEqual(False, bp.enabled)
        self.assertEqual(1, bpmgr.last())
        self.assertEqual((False, 'Breakpoint number (10) out of range 1.'),
                         bpmgr.delete_breakpoint_by_number(10))
        self.assertEqual((True, ''), bpmgr.delete_breakpoint_by_number(1))
        self.assertEqual((False, 'Breakpoint (1) previously deleted.'),
                          bpmgr.delete_breakpoint_by_number(1))
        bpmgr.reset()
        return

    def test_checkfuncname(self):
        'Test breakpoint.checkfuncname()'
        import inspect
        frame = inspect.currentframe()

        bpmgr = breakpoint.BreakpointManager()
        bp    = bpmgr.add_breakpoint('foo', 5)

        self.assertEqual(False, breakpoint.checkfuncname(bp, frame))

        def foo(bp, bpmgr):
            frame = inspect.currentframe()
            self.assertEqual(True, breakpoint.checkfuncname(bp, frame))
            # frame.f_lineno is constantly updated. So adjust for the 
            # line difference between the add_breakpoint and the check.
            bp3 = bpmgr.add_breakpoint('foo', frame.f_lineno+1) 
            self.assertEqual(True, breakpoint.checkfuncname(bp3, frame))
            self.assertEqual(False, breakpoint.checkfuncname(bp3, frame))
            return
    
        bp2 = bpmgr.add_breakpoint(None, None, False, None, 'foo')
        foo(bp2, bpmgr)
        return

if __name__ == '__main__':
    unittest.main()