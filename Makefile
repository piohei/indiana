.PHONY: init run production test

init:
	pip3 install -r requirements.txt
	npm install
	npm run build
	cd web && bower install && cd ..

run:
	foreman start

production:
	INDIANA_ENV=production foreman start

test:
	INDIANA_ENV=test pytest ./test

simulate:
	python3 -m simulator.path_simulator path3

simulator_test:
	INDIANA_ENV=test python3 -m simulator.simulator_manual_test

request_pos:
	python3 -m scripts.request_position

