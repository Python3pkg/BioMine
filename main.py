#!/usr/bin/python
# author: Adam D Scott (amviot@gmail.com)
# first created: 2015*09*28

import sys
import getopt
import requests
import json
import tempfile
from ensemblAPI import ensemblAPI
from requests.auth import HTTPDigestAuth
from xmlutils.xml2json import xml2json
import xml.etree.ElementTree as ET

def parseArgs( argv ):
	helpText = "python main.py" + " "
	helpText += "-i <inputFile> -o <outputFile>\n"
	helpText += "-s \"HGVS notation\" -t (boolean flag for tsv output)\n"
	inputFile = ""
	output = ""
	hgvs = ""
	tsv = False
	try:
		opts, args = getopt.getopt( argv , "h:i:o:s:t" , ["input=" , "output=" , "hgvs="] )
	except getopt.GetoptError:
		print "ADSERROR: Command not recognized"
		print( helpText ) 
		sys.exit(2)
	if not opts:
		print "ADSERROR: Expected flagged input"
		print( helpText ) 
		sys.exit(2)
	for opt, arg in opts:
		print opt + " " + arg
		if opt in ( "-h" , "--help" ):
			print( helpText )
			sys.exit()
		elif opt in ( "-i" , "--input" ):
			inputFile = arg
		elif opt in ( "-o" , "--output" ):
			output = arg
		elif opt in ( "-s" , "--hgvs" ):
			hgvs = arg
		elif opt in ( "-t" , "--tsv" ):
			tsv = True
	return { "input" : inputFile , "output" : output , "hgvs" : hgvs , "tsv" : tsv }
	
def checkConnection():
	ensemblInstance = "http://rest.ensembl.org/info/ping?content-type=application/json"
	res = requests.get( ensemblInstance )
	if res:
		print "have response"
	else:
		print res.status_code

def readMutations( inputFile ):
	variants = []
	if inputFile:
		inFile = open( inputFile , 'r' )
		for line in inFile:
			fields = line.split( '\t' )
			variants.append( fields[0] + ":" + fields[1] )
	return variants
	
def main( argv ):
	values = parseArgs( argv )
	inputFile = values["input"]
	outputFile = values["output"]
	hgvs = values["hgvs"]
	tsv = values["tsv"]

	results = ""
	variants = readMutations( inputFile )
	ensemblInstance = ensemblAPI()
	if inputFile and outputFile:
		ensemblInstance.fOutAnnotateHGVS( outputFile , variants )
	elif inputFile and not outputFile:
		results = ensemblInstance.annotateHGVSArray2tsv( variants )
	#results["annotations"]
	#results["errors"]

	if hgvs:
		if tsv:
			resultsErrors = ensemblInstance.annotateHGVSScalar2tsv( hgvs )
			results = resultsErrors["annotations"]
		else:
			ensemblInstance.annotateHGVSScalar2Response( hgvs )
			results = ensemblInstance.response.text

	print results

	#print ensemblInstance.headers
	#print ensemblInstance.data
	#print ensemblInstance.buildURL()
	#for key , value in response.iteritems():
	#	fout.write( key + "\t" + value )
	#if response:
	#	print response.text
	#else:
	#	print response.status_code
	#print ensemblInstance

if __name__ == "__main__":
	main( sys.argv[1:] )
