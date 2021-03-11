--clone:
		git pull origin master

--install-requirements:
		pip3 install -r requirements.txt

--system-d:
		sudo ln -snf $(shell pwd)/inesc/systemd-python.service /usr/lib/systemd/system/systemd-python.service && \
		sudo systemctl is-enabled systemd-python.service &>/dev/null || sudo systemctl enable systemd-python.service;

--restart-systemd:
		sudo systemctl restart systemd-python

--systemd-reload:
		sudo systemctl daemon-reload


install: --install-requirements --system-d --systemd-reload --restart-systemd