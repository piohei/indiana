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
