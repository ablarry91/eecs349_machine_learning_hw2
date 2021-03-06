# This file will contain all the functions that handle comunication with CSV file and data management


from data_util import *
import csv

################ CONVENTIONS #################
##############################################
#          Array of DataRow = table			 #
#            Data Row = Instance             #
#         Not search = Inverse Search        #
##############################################

# IMPORT CSV DATA ##############################################################################

# Gets a string path for a CSV file and returns an array of DataRow (Table), where each position of the array
# will correpspond to a table line

# Entry -> (String) location of metadata.csv | (String) location of the CSV btrain.csv
# Returns -> array(DataRow) containing all data "Table"

def importDataCSV(metPath, dataPath):		
	metList = []
	dataList = []
	dataRowTable = []

	# Import and handle metadata.csv
	file = open(metPath)
	csvFile = csv.reader(file)
	for row in csvFile:
		metList.append(row)

	typeList = []
	for i in metList:
		typeList.append(i[1])
	typeList.pop(0)

	# Import and handle rawdata.csv
	file = open(dataPath)
	csvFile = csv.reader(file)
	for row in csvFile:
		dataList.append(row)

	tagList = dataList.pop(0)

	for row in dataList:
		dataRowTable.append(DataRow(tagList, row, typeList))

	return dataRowTable


###############################################################################################

# DATA FILTER #################################################################################

# Given a table, a feature and a value returns a table containing entries with that value

# Entry -> DataRow[] | String | String(Discrete) Float (Continuous) | None(Discrete) Float (Continuous) | (Optional) Boolean for inverse search
# Returns -> DataRow[] filtered accordingly

def filterTable(table, featureTag, value, toValue=None, nope=True):		
	if len(table) < 1:
		raise NameError('Empty Table!')
	else:
		filteredList = []


		if toValue == None:
			# Search for the instances with the value
			for row in table:
				if (str(row.retrieve(featureTag).getValue()) == str(value)) != (not(nope)) :
					filteredList.append(row)
		else:
			# Search for the instances with the value in the interval
			if table[0].retrieve(featureTag).fType == FeatureType.DISCRETE:
					raise NameError('This is a discrete data type!')
			else:
				for row in table:
					if (row.retrieve(featureTag).getValue() >= value and row.retrieve(featureTag).getValue() <= toValue) != (not(nope)):
						filteredList.append(row)
		return filteredList


###############################################################################################

# DATA FILTER BY ID ###########################################################################

# Given a table, and a list of IDs, retrieve a table containing all the DataRow

# Entry -> DataRow[] | List of Strings (IDs for the DataRows desired) | (Optional) Boolean for inverse search
# Returns -> DataRow[] filtered accordingly

def filterTableByID(table, idList, nope=True):		
	if len(table) < 1:
		raise NameError('Empty Table!')
	else:
		filteredList = []
		# do an inverse search
		for row in table:
			if (str(row.id) not in idList) != nope:
				filteredList.append(row)
		return filteredList


###############################################################################################

# ATRIBUTE PCT ################################################################################

# Given a table, a feature and a value returns a table containing entries with that value

# Entry -> DataRow[] | String | String | (Optional) String
# Returns -> Float (pct of the atribute occurence in data)

def atributePct(table, featureTag, value, toValue=None):		
	total = len(table)
	instances = 0

	if toValue == None:
		instances = len(filterTable(table,featureTag,value))
	else:
		instances = len(filterTable(table,featureTag,value,toValue))

	return float(instances)/float(total)


###############################################################################################

# DISTINCT ATRIBUTES ##########################################################################

# Given a table, a feature and a value returns a table containing entries with that value

# Entry -> DataRow[] | String (atribute name) 
# Returns -> List (distinct values for that atribute)

def distinctAtributes(table, featureTag):		
	if len(table) < 1:
		raise NameError('Empty Table!')
	else:
		result = []
		for row in table:
			val = row.retrieve(featureTag).getValue() 
			if(val not in result):
				result.append(val)
		return result

###############################################################################################

# GENERATE CSV FILE ###########################################################################

# Takes a table and output a .csv file of it

# Entry -> DataRow[] | (Optional) path, or it will put in the project root as sample.csv 
# Returns -> 

def createFileCSV(table, path="./sample"):		
	if len(table) < 1:
		raise NameError('Empty Table!')
	else:
		file = open(path + '.csv', 'w+')

		file.write(table[0].toStringHeaders() + "\n")

		for row in table:
			file.write(row.toStringCSV() + '\n')
		file.close() 

###############################################################################################

