# Cavernobot
Cavernobot is a bot created with the [discord.py API](https://pypi.org/project/discord.py/) \
A lot of stuff is **hard-coded** into this bot so it is not adviced to use it yourself. \
This code is here mostly for ease of deployment and transparence

## How to install

Make sure you've got **at least python 3.5** (discord.py requirement)

### Clone the repository on your server

`git clone https://github.com/UnFefeSauvage/Cavernobot.git`

### Go to project root and generate a virtual environment

```bash
cd Cavernobot/
python -m venv .venv/
```

### Enter the virtual environment and install dependencies

```bash
src ./venv/bin/activate
pip install -r requirements.txt
```

### Create a `Resrcs/` folder in which you'll put:

* a `config.json` file with the `"token"` and `"prefix"` attribute
* an empty (contains `{}`) `counts.json` file

### Launch the bot

By being in the virtual environment using `python src/main.py`
