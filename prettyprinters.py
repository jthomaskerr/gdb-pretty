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

class static:
    "Creates a 'static' method"
    def __init__(self, function):
              self.__call__ = function

pretty_printers = { }

class pretty_printer:
  
  def __init__(self, regex):
    self.__regex = re.compile(regex)
  
  def __call__(self,pretty_printer):
    "Registers a Pretty Printer"
    try:
      pretty_printers[self.__regex] = pretty_printer
      return pretty_printer
    except:
        print "ERRRRRR: %s" % traceback.format_exc()


class AbstractPrettyPrinter:
    "Abstract Base Class for all Pretty Printer"
    
    def __init__(self, typename, value):
        self._typename = typename
        self._value = value


def find_pretty_printer(value):
  "Find a pretty printer suitable for value"
  try:
    type = value.type

    if type.code == gdb.TYPE_CODE_REF:
             type = type.target()

    type = type.unqualified().strip_typedefs()

    typename = type.tag
    if typename == None:
              return None

    for ppRegex in pretty_printers:
      if ppRegex.search(typename):
         return pretty_printers[ppRegex](typename, value)

    return None
  except:
        print "ERRRRRR: %s" % traceback.format_exc()

def register_pretty_printers(obj):
    "Register  Pretty Printers."
    if obj == None:
              obj = gdb
    obj.pretty_printers.append(find_pretty_printer)
