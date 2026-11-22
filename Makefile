
# Infer the repository URL from the git remote
REPO_URL := $(shell git config --get remote.origin.url)

APP_NAME = 'Cowabunga'
ICON = 'cowabunga/py_game/assets/favicon.png'

CNAME = 


publish:
	@uv run pygbag --build --app_name $(APP_NAME) --icon $(ICON) .
	@echo "Publishing to $(REPO_URL)"
ifdef CNAME
	@uv run ghp-import -n -p --cname $(CNAME) -f ./build/web 
else
	@uv run ghp-import -n -p -f ./build/web 
endif

runweb:
	@uv run pygbag .