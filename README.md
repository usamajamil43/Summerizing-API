# Sections
- Requirements
- Environment Setup
- Dependencies Installation
- Configuration
- Execution

## Requirements
1) Python and Pip
2) Pyenv
3) [Pyenv Virtualenv](https://github.com/pyenv/pyenv-virtualenv)

## Environment Setup
```bash
pyenv install 3.7.11             # Installs python 3.7.11
pyenv virtualenv 3.7.11 <name>   # Creates a virtual env for python 3.7.11
pyenv activate <name>            # Activates the virtual env
```

## Dependencies Installation
```bash
pip install -r requirements.txt
```

## Configuration

The following parameters can be configured inside `constants.py`.
-  XML source URLS
-  API token
-  API endpoint
-  Repeat time
-  Template id
-  Slide template id
-  Layer template id

## Execution
```
python main.py 
```