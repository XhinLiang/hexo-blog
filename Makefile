run:
	docker run -p 2333:2333 -d xhinliang/site

push:
	git add . --all && git commit -m 'push article' && git pull origin master && git push origin master

build:
	docker build -t xhinliang/site . 
