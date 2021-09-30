"""Simple module to load configuration from file"""
import json
import os
from pathlib import Path

# Parse configuration file (if it exists)
cfg_path = os.environ.get('APY_CONFIG', '~/.config/apy/apy.json')
cfg_file = Path(cfg_path).expanduser()
if cfg_file.exists():
    with cfg_file.open(encoding='utf8') as f:
        cfg = json.load(f)
else:
    cfg = {}


# Ensure that cfg has required keys
for required, default in [('base', None),
                          ('img_viewers', {
                              'svg': ['display', '-density', '300'],
                          }),
                          ('img_viewers_default', ['feh']),
                          ('markdown_models', ['Basic']),
                          ('presets', {}),
                          ('profile', None),
                          ('query', 'tag:marked OR -flag:0')]:
    if required not in cfg:
        cfg[required] = default


# Ensure that default preset is defined
if 'default' not in cfg['presets']:
    cfg['presets']['default'] = {
        'model': 'Basic',
        'tags': [],
    }


# If base not defined: Look in environment variables
if cfg['base'] is None:
    for var in ['APY_BASE', 'ANKI_BASE']:
        if var in os.environ:
            cfg['base'] = os.environ[var]
            break


# Ensure base path is a proper absolute path
if cfg['base']:
    cfg['base'] = os.path.abspath(os.path.expanduser(cfg['base']))


# Set terminal width for output
try:
    cfg['width'] = os.get_terminal_size()[0] - 3
except OSError:
    cfg['width'] = 120
