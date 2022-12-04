FOLDERNAME ?= $(shell bash -c 'read -p "Name the folder >> " foldername; echo $$foldername')

folder:
	cp -r day-x-template/ $(FOLDERNAME)
