init:
		pip3 install -r requirements.txt
		cd web_app && bower install && cd ..

run:
	  foreman start

test:
	  pytest .
