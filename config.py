import os
import sys
import configparser


def default_killers():
  return [
    'Huntress', 'Mastermand', 'Nurse', 'Knight', 'Cenobite', 'Deathslinger',
    'Skull Merchant', 'Executioner', 'Hag', 'Nemesis', 'Ghost Face', 'Legion',
    'Clown', 'Cannibal', 'Pig', 'Oni', 'Twins', 'Trapper', 'Spirit',
    'Hillbilly', 'Doctor', 'Plague', 'Onryo', 'Artist', 'Dredge', 'Trickster',
    'Blight', 'Wraith', 'Nightmare', 'Shape'
  ]


def default_survivors():
  return [
    'David', 'Jeff', 'Ada', 'Elodie', 'Dwight', 'Thalita', 'Bill', 'Haddie',
    'Claudette', 'Meg', 'Felix', 'Kate', 'Leon', 'Jonah', 'Laurie', 'Feng',
    'Mikaela', 'Ash', 'Yoichi', 'Zarina', 'Jane', 'Ace', 'Cheryl', 'Vittorio',
    'Yui', 'Quentin', 'Nea', 'Adam', 'Yun-Jin', 'Renato', 'Rebecca', 'Jill',
    'Jake', 'Tapp'
  ]


def configparser_instance():
  # create a new instance of the ConfigParser class from the configparser module
  return configparser.ConfigParser(allow_no_value=True)


def get_config_file_path(config_file):
  # get the directory name of the current file
  dir_name = os.path.dirname(os.path.abspath(__file__))
  return os.path.join(dir_name, config_file)


def create_config(config_file):
  config = configparser_instance()
  config.add_section('Settings')

  config.set('Settings', 'team', 0)
  config.set('Settings',
             '# Default team selection: 0 = killer, 1 = survivor\n', None)

  config.set('Settings', 'mode', 0)
  config.set('Settings',
             '# Default mode selection: 0 = rotating, 1 = normal\n', None)

  config.set('Settings', 'killerList', ','.join(default_killers()))
  config.set('Settings',
             '# Default list of Killers. NO SPACES BETWEEN COMMAS\n', None)

  config.set('Settings', 'survivorList', ','.join(default_survivors()))
  config.set('Settings',
             '# Default list of Survivors. NO SPACES BETWEEN COMMAS', None)

  with open(get_config_file_path(config_file), 'w') as f:
    config.write(f)


def parse_boolean(config, key):
  try:
    return config.getboolean('Settings', key)
  except ValueError:
    print(
      f"Warning: Invalid value for '{key}' in configuration file. Using default value 0.\n"
    )
    return False


def parse_list(config, name, default_fn):
  list_as_string = config.get('Settings', name)
  list = list_as_string.split(',')
  # check if the list is empty or has less than 3 characters
  if list_as_string == '' or len(list) < 3:
    # if this is true, then we assign a default list
    print(
      f"Warning: Invalid value for '{name}' in configuration file. Using default list.\n"
    )
    list = default_fn()
  return list


def initialize_config(config_file):
  config = configparser_instance()

  try:
    with open(config_file) as f:
      config.read_file(f)
      config.get('Settings', 'team')
  except FileNotFoundError:
    print("Configuration file not found. Creating default config.\n")
    create_config(config_file)
    with open(config_file) as f:
      config.read_file(f)
  except configparser.NoSectionError:
    print(
      "Invalid configuration file: 'Settings' section not found. Creating default config\n"
    )
    create_config(config_file)
    with open(config_file) as f:
      config.read_file(f)
  except Exception as e:
    print(f"Unexpected error while reading configuration file: {e}\n")
    sys.exit(1)

  mode = parse_boolean(config, 'mode')
  team = parse_boolean(config, 'team')
  killers = parse_list(config, 'killers', default_killers)
  survivors = parse_list(config, 'survivors', default_survivors)

  # create a dictionary with the configuration settings
  return {
    "team": team,
    "mode": mode,
    "killers": killers,
    "survivors": survivors
  }
