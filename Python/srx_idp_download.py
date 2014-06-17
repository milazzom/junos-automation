# Python script to download SRX IDP signature data files for installing everything offline.
# Michael A. Milazzo (mmilazzo@juniper.net)

import sys, httplib2, xml.etree.ElementTree as ET, hashlib


def calculateMd5(fileName):
	with open(fileName) as candidate_file:
		data = candidate_file.read()
		md5_digest = hashlib.md5(data).hexdigest()
	return md5_digest

# I thought about providing a menu-based selection to prevent invalid data entries, but with the different combinations of Junos versions and SRX devices,
# that may prove to be unmaintainable.

srxModel = raw_input("Enter SRX Model (i.e. srx550, ln2600): ")
junosVersion = raw_input("Enter version of Junos (i.e. 12.1): ")
	
url = "https://services.netscreen.com/cgi-bin/index.cgi?type=manifest&device=" + srxModel + "&feature=ai&detector=0.0.0&to=latest&os=" + junosVersion
resp, content = httplib2.Http().request(url)
fileCount = 0
errors = 0
# Upon an HTTP 200 response, the script assumes we're good to go.  I did test using bogus device/junos values and the success logic doesn't execute.
if resp.status == 200:
	manifest = ET.fromstring(content)
	conn = httplib2.Http()
	for entry in manifest.findall("entry"):
	
		filename = entry.find("id").text
		fileUrl = entry.find("url").text
		fileMd5 = entry.find("checksum").text
		print "Downloading " + filename + "..."
		response, fileContent = conn.request(fileUrl)
		fileCount = fileCount + 1
		
		with open(filename, "wb") as f:
			f.write(fileContent)
	
		print "Download of " + filename + " completed, checking checksum!"
		calculatedMd5 = calculateMd5(filename)
		if calculatedMd5 == fileMd5:
			print filename + " checksum matches!"
		else:
			print fileMd5 + " != " + calculatedMd5
			errors = errors + 1
	print "\n\n" + str(fileCount) + " files downloaded, " + str(errors) + " errors detected."
	
	
	

	


	
