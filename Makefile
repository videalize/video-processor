DEPENDENCIES_FILE=requirements.txt

all:
	@pip install -r $(DEPENDENCIES_FILE)
	@python setup.py develop

run:
	@./bin/videalize

write_dependencies:
	@pip freeze | grep -v videalize | grep -v video-processor > $(DEPENDENCIES_FILE)
	@echo "Dependencies written to $(DEPENDENCIES_FILE)"
