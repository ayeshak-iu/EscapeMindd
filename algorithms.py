
import heapq
import time


# ---------- STATE TRANSITIONS ----------

def get_successors(layout, state):

    row, col, has_key, door_unlocked = state

    actions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    successors = []

    for action, (dr, dc) in actions.items():

        new_row = row + dr
        new_col = col + dc

        # Check room boundaries
        if not (0 <= new_row < 7 and 0 <= new_col < 7):
            continue

        target = layout[new_row][new_col]

        # Cannot move through walls
        if target == "#":
            continue

        # Need key before entering door
        if target == "D" and not has_key:
            continue

        # Need unlocked door before reaching exit
        if target == "E" and not door_unlocked:
            continue

        new_has_key = has_key
        new_door_unlocked = door_unlocked

        # Collect key
        if target == "K":
            new_has_key = True

        # Unlock door
        if target == "D":
            new_door_unlocked = True

        new_state = (
            new_row,
            new_col,
            new_has_key,
            new_door_unlocked
        )

        successors.append((new_state, action))

    return successors


# ---------- GOAL TEST ----------

def is_goal(state):

    row, col, has_key, door_unlocked = state

    return (
        row == 6
        and col == 6
        and has_key
        and door_unlocked
    )


# ---------- HEURISTIC ----------

def heuristic(state):

    row, col, has_key, door_unlocked = state

    # Manhattan distance to the exit
    return abs(6 - row) + abs(6 - col)


# ---------- PATH RECONSTRUCTION ----------

def reconstruct_path(parent, state):

    path = []

    while parent[state] is not None:

        previous_state, action = parent[state]

        path.append(action)

        state = previous_state

    path.reverse()

    return path


# ---------- A* SEARCH ----------

def astar(layout, start_state):

    start_time = time.perf_counter()

    priority_queue = []

    counter = 0

    heapq.heappush(
        priority_queue,
        (heuristic(start_state), counter, 0, start_state)
    )

    g_score = {start_state: 0}

    parent = {start_state: None}

    explored = 0

    while priority_queue:

        f_score, _, current_g, current = heapq.heappop(
            priority_queue
        )

        # Ignore outdated queue entries
        if current_g != g_score.get(current):
            continue

        explored += 1

        # Check whether the goal is reached
        if is_goal(current):

            return {
                "path": reconstruct_path(parent, current),
                "explored": explored,
                "time": time.perf_counter() - start_time
            }

        # Explore neighbouring states
        for next_state, action in get_successors(
            layout, current
        ):

            tentative_g = current_g + 1

            if tentative_g < g_score.get(
                next_state, float("inf")
            ):

                g_score[next_state] = tentative_g

                parent[next_state] = (current, action)

                counter += 1

                f_score = (
                    tentative_g + heuristic(next_state)
                )

                heapq.heappush(
                    priority_queue,
                    (
                        f_score,
                        counter,
                        tentative_g,
                        next_state
                    )
                )

    return {
        "path": None,
        "explored": explored,
        "time": time.perf_counter() - start_time
    }


# ---------- TEST A* ON ESCAPEMIND ----------

if __name__ == "__main__":

    from environment import Environment

    game = Environment()

    start_state = game.get_state()

    result = astar(game.layout, start_state)

    print("\n===== ESCAPEMIND A* SOLVER =====")

    if result["path"] is not None:

        print("\nSolution Found!")

        print("Path:", result["path"])

        print("Path Length:", len(result["path"]))

    else:

        print("\nNo solution found!")

    print("Explored States:", result["explored"])

    print("Execution Time:", result["time"], "seconds")
