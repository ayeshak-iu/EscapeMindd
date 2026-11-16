
class Environment:

    def __init__(self):

        # Static 7x7 mansion layout
        self.layout = [
            [".", ".", ".", "#", ".", ".", "."],
            ["#", "#", ".", "#", ".", "#", "."],
            [".", ".", ".", ".", ".", "#", "."],
            [".", "#", "#", "#", ".", ".", "."],
            [".", ".", "K", ".", ".", "#", "."],
            ["#", ".", "#", "D", ".", ".", "."],
            [".", ".", ".", "#", ".", ".", "E"]
        ]

        # Initial game state
        self.player_position = (0, 0)
        self.has_key = False
        self.door_unlocked = False
        self.game_won = False

        self.status = "Find the key to unlock the door."

        self.refresh_room()

    # ---------- UPDATE THE ROOM ----------

    def refresh_room(self):

        # Create a fresh copy of the original layout
        self.room = [row.copy() for row in self.layout]

        # Remove key after collection
        if self.has_key:
            self.room[4][2] = "."

        # Display player
        row, col = self.player_position
        self.room[row][col] = "P"

    # ---------- STATE REPRESENTATION ----------

    def get_state(self):

        row, col = self.player_position

        return (
            row,
            col,
            self.has_key,
            self.door_unlocked
        )

    # ---------- VALID ACTIONS ----------

    def get_valid_actions(self):

        actions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        valid_actions = []

        row, col = self.player_position

        for action, (dr, dc) in actions.items():

            new_row = row + dr
            new_col = col + dc

            # Check boundaries
            if not (0 <= new_row < 7 and 0 <= new_col < 7):
                continue

            target = self.layout[new_row][new_col]

            # Cannot cross walls
            if target == "#":
                continue

            # Cannot enter locked door without key
            if target == "D" and not self.has_key:
                continue

            # Cannot escape before unlocking door
            if target == "E" and not self.door_unlocked:
                continue

            valid_actions.append(action)

        return valid_actions

    # ---------- MOVE PLAYER ----------

    def move_player(self, direction):

        if self.game_won:
            self.status = "You have already escaped!"
            return False

        if direction not in self.get_valid_actions():

            self.status = "Invalid move! Check the walls, key or door."
            return False

        row, col = self.player_position

        moves = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        dr, dc = moves[direction]

        new_row = row + dr
        new_col = col + dc

        target = self.layout[new_row][new_col]

        # Collect key
        if target == "K":

            self.has_key = True
            self.status = "You collected the key!"

        # Unlock door
        elif target == "D":

            self.door_unlocked = True
            self.status = "The door is unlocked!"

        # Move player
        self.player_position = (new_row, new_col)

        # Check winning condition
        if target == "E":

            self.game_won = True
            self.status = "Congratulations! You escaped the mansion!"

        elif target not in ["K", "D"]:

            self.status = "You moved successfully."

        self.refresh_room()

        return True

    # ---------- GOAL TEST ----------

    def is_goal_state(self):

        return (
            self.player_position == (6, 6)
            and self.has_key
            and self.door_unlocked
        )

    # ---------- DISPLAY ROOM ----------

    def display_room(self):

        print("\n===== ESCAPEMIND =====\n")

        for row in self.room:
            print(" ".join(row))


# ---------- TEST ENVIRONMENT ----------

if __name__ == "__main__":

    game = Environment()

    game.display_room()

    print("\nInitial State:", game.get_state())

    print("Available Actions:", game.get_valid_actions())

    print("Goal Reached:", game.is_goal_state())

