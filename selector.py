import random

# The CharacterSelector class handles character selection based on user input and settings from a configuration file.
class CharacterSelector:

  # The __init__ function initializes the CharacterSelector object with settings from the configuration file.
  def __init__(self, config: dict) -> None:
    """
    Initializes the CharacterSelector object with settings from the configuration.

    Args:
        config (dict): A dictionary containing the configuration settings.

    Attributes:
        config (dict): The configuration settings.
        selection_mode (bool): The selection mode from the configuration (True for random, False for cycling).
        last_selected_team (bool): The last selected team (True for survivors, False for killers).
        config_characters (dict): A dictionary of characters for each team from the configuration (no duplicates).
        remaining_characters (dict): A dictionary of remaining characters for each team.
        selected_characters (dict): A dictionary of selected characters for each team.
        excluded_characters (dict): A dictionary of excluded characters for each team.
        previous_selection (dict): A dictionary to store the previous selection for each team.
    """
    self.config = config
    self.selection_mode = config['mode']
    self.last_selected_team = config['team']
    self.config_characters = {'killer': set(config['killers']), 'survivor': set(config['survivors'])}
    self.unselected_characters = {'killer': [], 'survivor': []}
    self.selected_characters = {'killer': [], 'survivor': []}
    self.excluded_characters = {'killer': [], 'survivor': []}
    self.previous_selection = {'killer': None, 'survivor': None}


  
  def print_character_selection(self, character: str) -> None:
    '''The print_character_selection function prints the chosen character and their team (Killer or Survivor).'''
    # Determine the team based on whether the character is in the survivors list
    team = "Survivor" if character in self.config_characters['survivor'] else "Killer"
    self.previous_selection[team.lower()] = character
    # If the team is "Killer", add "The" before the character's name
    if team == "Killer":
      character = "The " + character
    # Print the chosen character and their team
    print(f'Play {team}: {character}!\n')

      
  def _update_team_info(self, user_choice: str) -> tuple[str, list[str]]:
      """Return team and team list based on the user's input."""
      if user_choice != '':
          self.last_selected_team = True if user_choice == '1' else False
    
      team = "survivor" if self.last_selected_team else "killer"
      team_list = list(self.config_characters[team])
            
      return team, team_list

  def random_character(self, user_choice: str) -> None:
    '''The random_character function selects a random character from the current team without repeating the previous selection.'''
    team, team_list = self._update_team_info(user_choice)

    # Choose a random character from the team list, excluding the previously selected character for the current team
    character = random.choice(
      [i for i in team_list if i != self.previous_selection[team] and i not in self.excluded_characters[team]])
    # Print the chosen character and their team
    self.print_character_selection(character)

  
  def cycle_characters(self, user_choice: str) -> None:
      team, team_list = self._update_team_info(user_choice)
  
      unselected = self.unselected_characters[team]
      selected = self.selected_characters[team]
      available = [i for i in unselected if i != self.previous_selection[team] and i not in selected and i not in self.excluded_characters[team]]
    
      if not available:
          unselected = self.unselected_characters[team] = team_list
          selected = self.selected_characters[team] = []
          available = [i for i in unselected if i != self.previous_selection[team] and i not in selected and i not in self.excluded_characters[team]]

      # if debug == True:
        #print("Available characters:", available)
        #print("Unselected characters:", unselected)
        #print("Selected characters:", selected)
        #print("Excluded characters:", self.excluded_characters[team])
        #input("")
    
      character = random.choice(available)
      unselected.remove(character)
      selected.append(character)
      self.print_character_selection(character)