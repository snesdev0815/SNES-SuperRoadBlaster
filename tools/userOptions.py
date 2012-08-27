#!/usr/bin/env python

'''
stupid little command-line args parser
'''

__author__ = "Matthias Nagler <matt@dforce.de>"
__url__ = ("dforce3000", "dforce3000.de")
__version__ = "0.1"


import os
import sys
import logging


class Options():
  def __init__( self, args, defaults ):
	self.__options = self.__parseUserArguments(args, defaults)

  def get( self, option ):
	if option in self.__options:
	  return self.__options[option]['value']
	else:
	  logging.error( 'Invalid option %s requested.' % option )
	  sys.exit(1)

  def manualSet( self, option, value ):
	self.__options[option]['value'] = value

  def set( self, option, value ):
	self.__options[option]['value'] = value

  def __parseUserArguments( self, args, defaults ):
	options = defaults
	  
	for i in range( len( args ) ):
	  if args[i][1:] in defaults:
		options[args[i][1:]]['value'] = args[i+1]
	return self.__sanitizeOptions( options )


  def __sanitizeOptions( self, options ):
	for optionName, optionValue in options.iteritems():
	  sanitizerLUT = self.__getSanitizerLUT()
	  options[optionName] = sanitizerLUT[optionValue['type']]( optionName, optionValue )	
	return options


  def __sanitizeInt( self, optionName, optionValue ):
	if type( optionValue['value'] ) is not int:
	  try:
		optionValue['value'] = int( optionValue['value'], 10 )
	  except ( TypeError, ValueError ):
		logging.error( 'Invalid argument %s for option -%s.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	if optionValue['value'] < optionValue['min'] or optionValue['value'] > optionValue['max']:
		logging.error( 'Argument %s for option -%s is out of allowed range %s - %s.' % ( optionValue['value'], optionName, optionValue['min'], optionValue['max'] ) )
		sys.exit(1)
	return optionValue

  def __sanitizeFloat( self, optionName, optionValue ):
	if type( optionValue['value'] ) is not float:
	  try:
		optionValue['value'] = float( optionValue['value'] )
	  except ( TypeError, ValueError ):
		logging.error( 'Invalid argument %s for option -%s.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	if optionValue['value'] < optionValue['min'] or optionValue['value'] > optionValue['max']:
		logging.error( 'Argument %s for option -%s is out of allowed range %s - %s.' % ( optionValue['value'], optionName, optionValue['min'], optionValue['max'] ) )
		sys.exit(1)
	return optionValue

  def __sanitizeHex( self, optionName, optionValue ):
	if type( optionValue['value'] ) is not int:
	  try:
		optionValue['value'] = int( optionValue['value'], 16 )
	  except ( TypeError, ValueError ):
		logging.error( 'Invalid argument %s for option -%s.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	if optionValue['value'] < optionValue['min'] or optionValue['value'] > optionValue['max']:
		logging.error( 'Argument %s for option -%s is out of allowed range %s - %s.' % ( optionValue['value'], optionName, optionValue['min'], optionValue['max'] ) )
		sys.exit(1)
	return optionValue
	
	
  def __sanitizeStr( self, optionName, optionValue ):
	if len( optionValue ) < 1:
		logging.error( 'Argument %s for option -%s is invalid.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	return optionValue


  def __sanitizeBool( self, optionName, optionValue ):
	if type( optionValue['value'] ) is str:
	  if optionValue['value'] not in ( 'on', 'off' ):
		logging.error( 'Argument %s for option -%s is invalid. Only on and off are allowed.' % ( optionValue['value'], optionName ) )
		sys.exit(1)
	  optionValue['value'] = True if optionValue['value'] == 'on' else False
	return optionValue
	
	
  def __getSanitizerLUT(self):
	return {
	  'int'	: self.__sanitizeInt,
	  'float'	: self.__sanitizeFloat,
	  'hex'	: self.__sanitizeHex,
	  'str'	: self.__sanitizeStr,
	  'bool'	: self.__sanitizeBool
	}