server: source/server/src/server.py 
	python source/server/src/server.py 
client: source/client/src/client.py
	python source/client/src/client.py 
database: source/server/src/database.py 
	python source/server/src/database.py 

clean:
	rm source/server/contacts.db