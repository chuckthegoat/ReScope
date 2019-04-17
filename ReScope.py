#!/usr/bin/python

# Import modules
import requests
import argparse
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

# Import config
from config import *

# Declare a class to hold Jamf object IDs and names
class JAMF_OBJ:
	def __init__(self, id, name):
		self.id = id
		self.name = name

def handle_obj(type, ids):
	'''
	
	Function to build the PUT requests to the Jamf API to change the scoping
	for objects of a given type with the provided ids to a list of computers
	and computer groups provided by the user.
	
	'''

	# Declare a dictionary to parse object type names from shortnames
	types = {
		'policy': ('policies', 'policy'),
		'config': ('osxconfigurationprofiles', 'osxconfigurationprofile'),
		'group': ('computer_groups', 'computer_group')
	}

	# Gets the location in the JSSResource and the XML tag name from the dictionary
	resource_url = types[type][0]
	resource_type = types[type][1]

	objects = []

	# For each provided id, make a request to the API and create a JAMF_OBJ
	# with the information retrieved from that request
	for id in ids:
		try:
			xml = requests.get(APIURL+resource_url+"/id/"+id, auth=HTTPBasicAuth(USERNAME, PASSWORD))
		except:
			print "Error: could not connect to", APIURL+resource_url+"/id/"+id
			pass

		jamf_obj = ET.fromstring(xml.content)
		objects.append(JAMF_OBJ(jamf_obj[0][0].text, jamf_obj[0][1].text))
	print "You are changing the scoping for the following objects:"
	for object in objects:
		print object.id+",", object.name

	# Prompt the user for a comma-separated list of computer IDs followed by
	# a comma-separated list of group-IDs to scope the JAMF_OBJs declared 
	# above to.
	computers = raw_input("Please enter a comma-separated list of computer IDs to add to the scope: ").replace(" ","").split(",")
	computer_groups = raw_input("Please enter a comma-separated list of computer group IDs to add to the scope: ").replace(" ","").split(",")

	# Format the data for the PUT request
	put_data = "<"+resource_type+"><scope><computers>"
	# Iterate over the list of computers and format them for the request
	for computer in computers:
		if (computer != ""):
			computer = "<computer><id>"+computer+"</id></computer>"
			put_data = put_data+computer
	put_data = put_data+"</computers><computer_groups>"
	# Iterate over the list of computer groups and format them for the request
	for computer_group in computer_groups:
		if (computer_group != ""):
			computer_group = "<computer_group><id>"+computer_group+"</id></computer_group>"
			put_data = put_data+computer_group
	put_data = put_data+"</computer_groups></scope></"+resource_type+">"

	print put_data
	
	# For each JAMF_OBJ, make a PUT request to the API to change the scoping for that object
	for id in ids:
		print id, requests.put(APIURL+resource_url+"/id/"+id, auth=HTTPBasicAuth(USERNAME, PASSWORD), data=put_data)

	return 0

def main():
	# Parse arguments
	parser = argparse.ArgumentParser(description="Scope JAMF Objects.")
	parser.add_argument('type', nargs=1, choices=['policy', 'config', 'group'], help='Type of objects to scope')
	parser.add_argument('ids', nargs='+', help='IDs of objects to scope')
	args = parser.parse_args()

	# Handle the request
	handle_obj(args.type[0], args.ids)

if __name__ == '__main__':
	main()
