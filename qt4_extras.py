# -*- coding: iso-8859-1 -*-
# Additional Pretty-printers for Qt4.

# Copyright (C) 2013 Joseph Thomas-Kerr <jthomaskerr@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gdb
import itertools
import re
import traceback
from prettyprinters import *

@pretty_printer('^Q(Basic)?AtomicInt$')
class QAtomicInt (AbstractPrettyPrinter):
    def to_string(self):
      try:
        return str(self._value['_q_value'])
      except:
        print "ERRRRRR: %s for type %s" % (traceback.format_exc(), self._typename)

@pretty_printer('^Q(?:Shared|Weak|Scoped)?Pointer<(.*)>$')
class QSharedPointer (AbstractPrettyPrinter):
    def __init__(self, typename, value):
        AbstractPrettyPrinter.__init__(self,typename, value)
        self._T = self._value.type.template_argument(0)
        self._ptr = self._value['value']

    def to_string(self):
      try:
        if self._ptr == 0x0:
          return "NULL (%s)" % self._typename
        weakref = self._value['d']['weakref']
        strongref = self._value['d']['strongref']
        return '%s (%s #%s/weak#%s)' % (self.deref(),self._typename, weakref, strongref)
      except:
        print "ERRRRRR: %s" % traceback.format_exc()
   
    def deref(self):
        if self._ptr == 0x0:
            return "NULL"
        return self._ptr.cast(self._T.pointer()).dereference()

    def children(self):
        return [('*',self.deref())]

