import sys
from enum import Enum
from selector import CharacterSelector
from config import initialize_config

config = initialize_config('settings.ini')
character_selector = CharacterSelector(config)


def print_menu():
  print("Press Enter to select a random character to play.")
  print("Enter 1 to switch to survivors.")
  print("Enter 0 to switch to killers.")
  print("Enter M to switch selection modes.")
  print("Enter E to exit the program.")
  print("Enter 'remove' to exclude a character from current team.")
  print("Enter 'clear' to stop exluding a character from current team.")
  print("\n")


def yes():
  return ['y', 'yes', 'yes!']


def cancel():
  return ['cancel', 'abort']


def pick_character(user_choice):
  previous_team = "Survivor" if character_selector.last_selected_team else "Killer"
  if user_choice != '':
    new_team = "Survivor" if user_choice == '1' else "Killer"
    if previous_team != new_team:
      print("\nSwitching team...")
  if character_selector.selection_mode:
    character_selector.random_character(user_choice)
  else:
    character_selector.cycle_characters(user_choice)


def switch_mode():
  character_selector.selection_mode = not character_selector.selection_mode
  print(
    f"\nSwitching mode to {'normal random' if character_selector.selection_mode else 'cycle random'}..."
  )


def exit_program():
  confirmation = input('Are you sure you want to DC? ')
  if confirmation.lower() in yes():
    print('\nSee you in the fog...')
    sys.exit(0)
  else:
    print('GGEZ\n')


def display_characters(team, available_characters, description):
  """Displays the available characters for exclusion or clearing."""
  available_characters = sorted(available_characters, key=str.lower)
  print(f"\nCurrent {description} {team} characters:")
  for i, char in enumerate(available_characters, start=1):
    print(f"{i}. {char}")


def exclude_character():
  team = "survivor" if character_selector.last_selected_team else "killer"
  characters = list(character_selector.config_characters[team])
  excluded = character_selector.excluded_characters[team]

  while True:
    available_characters = [
      char for char in characters if char not in excluded
    ]
    if len(available_characters) == 3:
      print(
        "No more characters can be excluded. Please clear some characters from the excluded list first."
      )
      break

    display_characters(team, available_characters, 'included')

    try:
      exclusion_index = input(
        "\nEnter the number of the character to remove them or 'cancel' to go back: "
      )
      if exclusion_index in cancel():
        print("Returning to the main menu...\n")
        break
      else:
        exclusion_index = int(exclusion_index)
        if 1 <= exclusion_index <= len(available_characters):
          exclusion = available_characters[exclusion_index - 1]
          confirmation = input(
            f"Are you really sure you want to remove {exclusion} from {team}s? "
          )
          if confirmation.lower() in yes():
            character_selector.excluded_characters[team].append(exclusion)
            print(f"{exclusion} was successfully removed from {team}s.\n")
          else:
            continue
        else:
          print(
            "Invalid number selection. Please enter a number that corresponds to one of the listed characters."
          )
    except ValueError:
      print("Invalid input. Please enter a valid number or 'cancel'.")


def clear_exclusions():
  team = "survivor" if character_selector.last_selected_team else "killer"
  excluded_characters = character_selector.excluded_characters[team]

  while True:
    if not excluded_characters:
      print(f"No {team} characters are currently excluded.\n")
      break
    else:
      display_characters(team, excluded_characters, 'excluded')
    clear_choice = input(
      "\nEnter the number of the character to clear from this list.\n"
      "Enter 'all' to remove all characters from this list.\n"
      "Enter 'cancel' to go back: ")

    if clear_choice.isdigit():
      clear_index = int(clear_choice)
      if clear_index > 0 and clear_index <= len(excluded_characters):
        character = excluded_characters[clear_index - 1]
        confirmation = input(
          f"Are you sure you want to clear {character} from the {team} excluded list? "
        )
        if confirmation.lower() in yes():
          character_selector.excluded_characters[team].remove(character)
          print(f"{character} has been cleared from the {team} excluded list.")
        else:
          continue
      else:
        print(
          "Invalid number selection. Please enter a number that corresponds to one of the listed characters."
        )
    elif clear_choice.lower() == 'all':
      confirmation = input(
        f"Are you sure you want to remove all characters from the {team} excluded list? "
      )
      if confirmation.lower() in yes():
        character_selector.excluded_characters[team] = []
        print(
          f"All characters have been cleared from the {team} excluded list.")
      else:
        print("Clear exclusion operation canceled.")
      break
    elif clear_choice.lower() in cancel():
      print("Returning to the main menu...\n")
      break
    else:
      print("Invalid choice. Please enter a valid number, 'all', or 'cancel'.")


def determine_input(choice):
  choice = choice.lower()
  if choice in ['0', '1', '']:
    return Action.PICK_CHARACTER
  elif choice in ['m', 'mode']:
    return Action.SWITCH_MODE
  elif choice in ['e', 'exit', 'quit', 'dc']:
    return Action.EXIT
  elif choice in ['exclude', 'remove']:
    return Action.EXCLUDE
  elif choice == 'clear':
    return Action.CLEAR
  elif choice == 'menu':
    return Action.MENU
  else:
    return None


class Action(Enum):
    PICK_CHARACTER = ('pick_character', pick_character)
    SWITCH_MODE = ('switch_mode', switch_mode)
    EXIT = ('exit', exit_program)
    EXCLUDE = ('exclude', exclude_character)
    CLEAR = ('clear', clear_exclusions)
    MENU = ('menu', print_menu)

    def __init__(self, action_name, action_function):
        self.action_name = action_name
        self.action_function = action_function

    @staticmethod
    def from_input(choice):
        choice = choice.lower()
        for action in Action:
            if choice == action.action_name:
                return action
        return None

    def execute(self):
        self.action_function()


def get_user_choice():
    while True:
        current_team = "Survivor" if character_selector.last_selected_team else "Killer"
        choice = input(f"Current team is {current_team}. Make your choice: ")
        action = determine_input(choice)

        if action == Action.PICK_CHARACTER:
            pick_character(choice)
        elif action is not None:
            action.execute()
        else:
            print("\nYou made an invalid selection. Try again.\n")
            print_menu()


def main():
  print_menu()
  get_user_choice()


if __name__ == '__main__':
  main()
