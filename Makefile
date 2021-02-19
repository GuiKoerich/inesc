--clone:
		git pull origin master

--restart-systemd:
		sudo systemctl restart systemd-python


install: --clone --restart-systemd