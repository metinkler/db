import xmltodict as xmltd

def parseXML(xml):
	gameDict = xmltodict.parse(xml, process_namespaces=True)


