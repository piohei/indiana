.PHONY: init run production test

init:
	pip3 install -r requirements.txt
	npm install
	npm run build
	cd web && $(npm bin)/bower install && cd ..

run:
	foreman start

production:
	INDIANA_ENV=production foreman start

test:
	INDIANA_ENV=test pytest ./test

simulate:
	python3 -m simulator.path_simulator path6 00:00:00:00:00:01 1

simulate2:
	python3 -m simulator.path_simulator path6 00:00:00:00:00:02 1

simulator_test:
	INDIANA_ENV=test python3 -m simulator.simulator_manual_test

request_pos:
	python3 -m scripts.request_position

