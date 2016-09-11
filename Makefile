init:
		pip3 install -r requirements.txt
		cd web && bower install && cd ..

run:
	  foreman start

test:
	  INDIANA_ENV=test pytest .
