import os
psql_password = os.getenv('psql_password')

#heroku PSQL
def PSQL_heroku_keys():
	global psql_password

	dbname = 'dckf07gmilugnu'
	port = '5432'
	user = 'onhedsjkayipmf'
	host = 'ec2-79-125-12-27.eu-west-1.compute.amazonaws.com'
	password = psql_password

	PSQL_heroku_keys = {'dbname' : dbname
						, 'port' : port
						, 'user' : user
						, 'host' : host
						, 'password' : password
						}

	return PSQL_heroku_keys

