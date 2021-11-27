
PHONY: install setup update update_dependencies

install: setup
	cp cavernobot.service /usr/lib/systemd/system/
	systemctl enable cavernobot

setup:
	@echo "Setting up virtual environment (location: ./venv)..."
	@( \
		python3 -m venv ./venv; \
		source ./venv/bin/activate; \
		pip3 install -r requirements.txt; \
	)
	@echo "Generating default bot data (location: ./data)..."
	@mkdir -p data
	@echo "{}" >data/config.json
	@echo "{}" >data/counts.json
	@echo "Bot setup done!"

update:
	@echo "Pulling from github repo..."
	@git pull
	@echo "Bot updated!"

update_dependencies:
	@echo "Updating dependencies..."
	@( \
		source ./venv/bin/activate; \
		pip3 install --upgrade -r requirements.txt; \
	)
	@echo "Dependencies updated!"