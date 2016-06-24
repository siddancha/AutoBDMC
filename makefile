install:
	sudo npm install -C webppl
	sudo npm install -g nodeunit grunt-cli -C webppl

clean-models:
	find models -type f ! -iname "*.stan" -delete