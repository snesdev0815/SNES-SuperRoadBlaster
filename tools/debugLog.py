#!/usr/bin/env python

'''
couple of debug logging functions
'''

__author__ = "Matthias Nagler <matt@dforce.de>"
__url__ = ("dforce3000", "dforce3000.de")
__version__ = "0.1"

import logging

def debugLog( data, message = '' ):
	logging.debug( message )
	debugLogRecursive( data, '' )


def debugLogExit( data, message = '' ):
	logging.debug( message )
	debugLogRecursive( data, '' )
	sys.exit()


def debugLogRecursive( data, nestStr ):
  nestStr += ' '
  if type( data ) is dict:
	logging.debug( '%s dict{' % nestStr )	
	for k, v in data.iteritems():
	  logging.debug( ' %s %s:' % tuple( [nestStr, k] ) )
	  debugLogRecursive( v, nestStr )
	logging.debug( '%s }' % nestStr )

  elif type( data ) is list:
	logging.debug( '%s list[' % nestStr )
	for v in data:
	  debugLogRecursive( v, nestStr )
	logging.debug( '%s ]' % nestStr )

  else:
	if type( data ) is int:
	  logging.debug( ' %s 0x%x %s ' % ( nestStr, data, type( data ) ) )
	else:
	  logging.debug( ' %s "%s" %s' % ( nestStr, data, type( data ) ) )
