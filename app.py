
import streamlit as st
import time

from environment import Environment
from algorithms import astar


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="EscapeMind",
    page_icon="🗝️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# SESSION STATE
# ==================================================

if "screen" not in st.session_state:
    st.session_state.screen = "menu"

if "game" not in st.session_state:
    st.session_state.game = Environment()

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

if "ai_path_positions" not in st.session_state:
    st.session_state.ai_path_positions = set()

if "game_start_time" not in st.session_state:
    st.session_state.game_start_time = None


# ==================================================
# GLOBAL THEME AND BOARD CSS
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Crimson+Text:wght@400;600&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at top, #f4e8f5 0%, #eadcf0 48%, #d9e9dc 100%);
    color: #44304f;
}

header, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: #704080 !important;
}

p, label {
    color: #513c5d;
    font-family: 'Crimson Text', serif;
    font-size: 17px;
}

hr {
    border-color: #c7a5d0 !important;
}

/* BUTTONS */

.stButton > button {
    background: linear-gradient(135deg, #81569a, #58376e);
    color: #fff8e8;
    border: 2px solid #d9b9e1;
    border-radius: 12px;
    min-height: 46px;
    font-family: 'Cinzel', serif !important;
    font-weight: 600;
    transition: all .2s ease;
    box-shadow: 0 4px 12px rgba(91, 53, 111, .18);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #a276b7, #704b88);
    border-color: #f2d69b;
    color: white;
    box-shadow: 0 0 16px rgba(143, 93, 165, .35);
}

/* AI BUTTON */

.stButton > button[kind="primary"] {
    background: linear-gradient(120deg, #f6d477, #dfa13c);
    border: 2px solid #fff0ae;
    color: #68451c;
    font-size: 16px;
    font-weight: bold;
    min-height: 58px;
    box-shadow: 0 4px 15px rgba(207, 151, 49, .3);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(120deg, #ffed9f, #ffc85b);
    color: #563916;
}

/* METRICS */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #fff8e9, #eadcf0);
    border: 2px solid #c7a5d0;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 4px 14px rgba(91, 53, 111, .12);
}

[data-testid="stMetricLabel"] {
    color: #704080 !important;
}

[data-testid="stMetricValue"] {
    color: #a87528 !important;
}

/* ALERTS */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* GAME BOARD */

.board-wrapper {
    display: flex;
    justify-content: center;
    padding: 18px;
    margin: 10px auto 20px;
    background: linear-gradient(135deg, #f8e9d6, #e5d5ed);
    border: 3px solid #bd91c9;
    border-radius: 16px;
    box-shadow: 0 6px 22px rgba(91, 53, 111, .2);
    overflow-x: auto;
}

.board {
    display: grid;
    grid-template-columns: repeat(7, 58px);
    gap: 5px;
}

.tile {
    width: 58px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-size: 28px;
    box-sizing: border-box;
}

/* FLOOR */

.empty {
    background: linear-gradient(135deg, #fff0d4, #ead9b9);
    border: 1px solid #c9ae79;
}

/* WALLS */

.wall {
    background: linear-gradient(135deg, #bba7c4, #806d8e);
    border: 2px solid #d8c4e0;
    box-shadow: inset 0 0 8px #66536f;
}

/* PLAYER */

.player {
    background: radial-gradient(circle, #f5c7ff, #a46bc0);
    border: 2px solid #f4d9ff;
    box-shadow: 0 0 15px #b77bd5;
}

/* KEY */

.key {
    background: radial-gradient(circle, #ffe78a, #d99a28);
    border: 2px solid #fff0a8;
    box-shadow: 0 0 15px #f6c54e;
}

/* DOOR */

.door {
    background: linear-gradient(135deg, #ed9b82, #c65e51);
    border: 2px solid #ffd0a8;
    box-shadow: 0 0 12px rgba(215, 93, 73, .4);
}

/* EXIT */

.exit {
    background: radial-gradient(circle, #8af0b1, #299a67);
    border: 2px solid #d0ffce;
    box-shadow: 0 0 18px #52df94;
}

/* AI PATH */

.path {
    background: radial-gradient(circle, #8ce4e1, #38a9a4);
    border: 2px solid #d1ffff;
    box-shadow: 0 0 13px #4cc9c5;
}

/* MOBILE BOARD */

@media (max-width: 550px) {

    .block-container {
        padding-left: 8px;
        padding-right: 8px;
    }

    .board {
        grid-template-columns: repeat(7, 38px);
        gap: 3px;
    }

    .tile {
        width: 38px;
        height: 38px;
        font-size: 20px;
    }

    .board-wrapper {
        padding: 8px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# START NEW GAME
# ==================================================

def start_new_game():

    st.session_state.game = Environment()
    st.session_state.screen = "game"

    st.session_state.ai_result = None
    st.session_state.ai_path_positions = set()

    st.session_state.game_start_time = time.perf_counter()

    st.rerun()


# ==================================================
# MAIN MENU
# ==================================================

def show_main_menu():

    st.html("""
    <div style="
        text-align:center;
        padding:100px 15px;
        margin-top:35px;
        background:linear-gradient(135deg,#9a70b0,#c9a5d7,#f1dca8);
        border:3px solid #fff0b0;
        border-radius:22px;
        box-shadow:0 8px 30px rgba(91,53,111,.25);
    ">

        <div style="
            font-size:75px;
            margin-bottom:15px;
        ">🗝️</div>

        <div style="
            font-family:Georgia,serif;
            font-size:clamp(36px,7vw,65px);
            font-weight:bold;
            letter-spacing:7px;
            color:#fff8e8;
            text-shadow:2px 3px 8px #704080;
        ">
            ESCAPEMIND
        </div>

    </div>
    """)

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "🗝️ ENTER THE MANSION",
            use_container_width=True
        ):
            start_new_game()


# ==================================================
# RENDER GAME BOARD
# ==================================================

def render_board(game, path_positions=None):

    if path_positions is None:
        path_positions = set()

    symbols = {
        "P": "🧍",
        ".": "",
        "#": "",
        "K": "🔑",
        "D": "🚪",
        "E": "🏁"
    }

    tiles_html = ""

    for row_index, row in enumerate(game.room):

        for col_index, cell in enumerate(row):

            position = (row_index, col_index)

            tile_class = {
                "P": "player",
                "#": "wall",
                "K": "key",
                "D": "door",
                "E": "exit",
                ".": "empty"
            }[cell]

            if cell == "." and position in path_positions:
                tile_class = "path"

            tiles_html += (
                f'<div class="tile {tile_class}">'
                f'{symbols[cell]}'
                f'</div>'
            )

    return (
        '<div class="board-wrapper">'
        '<div class="board">'
        + tiles_html +
        '</div></div>'
    )


# ==================================================
# GAME SCREEN
# ==================================================

def show_game_screen():

    game = st.session_state.game

    if game.game_won:
        st.session_state.screen = "ending"
        st.rerun()

    # PLAYER STATUS

    key_status = (
        "Collected 🔑"
        if game.has_key
        else "Find the key 🔍"
    )

    door_status = (
        "Unlocked 🔓"
        if game.door_unlocked
        else "Locked 🔒"
    )

    st.html(f"""
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        flex-wrap:wrap;
        gap:12px;
        background:linear-gradient(110deg,#81569a,#b28bc0);
        border:2px solid #e5c9ed;
        border-radius:12px;
        padding:15px 20px;
        margin:10px 0 20px;
        box-shadow:0 4px 15px rgba(91,53,111,.2);
        font-family:Georgia,serif;
    ">

        <div style="color:white;">
            🧍 PLAYER
            <strong style="color:#fff0ad;">{game.player_position}</strong>
        </div>

        <div style="color:white;">
            🗝️ KEY
            <strong style="color:#fff0ad;">{key_status}</strong>
        </div>

        <div style="color:white;">
            🚪 DOOR
            <strong style="color:#fff0ad;">{door_status}</strong>
        </div>

    </div>
    """)

    # GAME TITLE

    st.html("""
    <div style="
        text-align:center;
        font-family:Georgia,serif;
        font-size:clamp(22px,4vw,32px);
        letter-spacing:3px;
        color:#704080;
        margin:15px 0;
    ">
        THE MYSTERY MANSION
    </div>
    """)

    # GAME BOARD

    board_placeholder = st.empty()

    board_placeholder.html(
        render_board(
            game,
            st.session_state.ai_path_positions
        )
    )

    st.info(game.status)

    # MOVEMENT CONTROLS

    st.markdown("""
    <p style="
        text-align:center;
        font-weight:bold;
        font-family:Georgia,serif;
        letter-spacing:2px;
    ">
        MOVE THROUGH THE MANSION · W A S D
    </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col2:

        if st.button(
            "⬆️ UP",
            use_container_width=True,
            shortcut="W"
        ):

            game.move_player("up")

            st.session_state.ai_result = None
            st.session_state.ai_path_positions = set()

            st.rerun()

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "⬅️ LEFT",
            use_container_width=True,
            shortcut="A"
        ):

            game.move_player("left")

            st.session_state.ai_result = None
            st.session_state.ai_path_positions = set()

            st.rerun()

    with col2:

        if st.button(
            "⬇️ DOWN",
            use_container_width=True,
            shortcut="S"
        ):

            game.move_player("down")

            st.session_state.ai_result = None
            st.session_state.ai_path_positions = set()

            st.rerun()

    with col3:

        if st.button(
            "➡️ RIGHT",
            use_container_width=True,
            shortcut="D"
        ):

            game.move_player("right")

            st.session_state.ai_result = None
            st.session_state.ai_path_positions = set()

            st.rerun()

    # AI SOLVER

    st.write("")

    if st.button(
        "💡 LET AI SOLVE THE REST",
        type="primary",
        use_container_width=True
    ):

        start_state = game.get_state()

        result = astar(
            game.layout,
            start_state
        )

        st.session_state.ai_result = result

        if result["path"] is not None:

            row, col, has_key, door_unlocked = start_state

            path_positions = set()

            moves = {
                "up": (-1, 0),
                "down": (1, 0),
                "left": (0, -1),
                "right": (0, 1)
            }

            for action in result["path"]:

                dr, dc = moves[action]

                row += dr
                col += dc

                path_positions.add((row, col))

            st.session_state.ai_path_positions = path_positions

            board_placeholder.html(
                render_board(game, path_positions)
            )

            st.info("💡 A* has found a route! Watch the AI escape.")

            time.sleep(0.7)

            for action in result["path"]:

                game.move_player(action)

                board_placeholder.html(
                    render_board(game, path_positions)
                )

                time.sleep(0.35)

        else:

            st.warning(
                "A* could not find a solution from this position."
            )

        st.rerun()

    # RESTART

    if st.button(
        "↻ RESTART PUZZLE",
        use_container_width=True
    ):

        start_new_game()


# ==================================================
# ENDING SCREEN
# ==================================================

def show_ending_screen():

    game = st.session_state.game
    result = st.session_state.ai_result

    total_time = 0

    if st.session_state.game_start_time is not None:

        total_time = (
            time.perf_counter()
            - st.session_state.game_start_time
        )

    # VICTORY PANEL

    st.html("""
    <div style="
        text-align:center;
        padding:60px 20px;
        margin:15px 0 25px;
        background:linear-gradient(135deg,#a9e9b7,#70c99b,#8e69a8);
        border:3px solid #fff1ae;
        border-radius:20px;
        box-shadow:0 7px 30px rgba(65,133,91,.3);
    ">

        <div style="font-size:75px;">🏆</div>

        <div style="
            font-family:Georgia,serif;
            font-size:clamp(30px,6vw,50px);
            color:#fff9e8;
            letter-spacing:4px;
            text-shadow:2px 3px 8px #55734f;
            margin:15px 0;
        ">
            ESCAPE COMPLETED!
        </div>

        <div style="
            color:#ffffff;
            font-size:22px;
            line-height:1.7;
        ">
            You found the key.<br>
            You unlocked the door.<br>
            You successfully escaped the mansion!
        </div>

    </div>
    """)

    # AI PERFORMANCE

    st.markdown(
        "<h2 style='text-align:center;'>🤖 AI PERFORMANCE</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "A* SEARCH ALGORITHM · PERFORMANCE RESULTS"
        "</p>",
        unsafe_allow_html=True
    )

    if result is not None and result["path"] is not None:

        path_length = len(result["path"])
        explored_states = result["explored"]
        execution_time = result["time"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("👣 Path Length", path_length)

        with col2:
            st.metric("🔍 Explored States", explored_states)

        with col3:
            st.metric(
                "⚡ Execution Time",
                f"{execution_time:.6f}s"
            )

        st.success("A* successfully found a solution!")

        st.markdown("### 🧭 Solution Path")

        st.code(
            " → ".join(result["path"]),
            language="text"
        )

    else:

        st.info(
            "This escape was completed manually. "
            "A* performance results are shown when you use the AI solver."
        )

    # GAME STATISTICS

    st.divider()

    st.subheader("⏱️ Adventure Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Game Time",
            f"{total_time:.2f} seconds"
        )

    with col2:
        st.metric(
            "Final Position",
            str(game.player_position)
        )

    st.write("")

    # PLAY AGAIN

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "🔁 PLAY AGAIN",
            use_container_width=True
        ):

            start_new_game()

    if st.button(
        "🏠 MAIN MENU",
        use_container_width=True
    ):

        st.session_state.screen = "menu"
        st.session_state.game = Environment()

        st.session_state.ai_result = None
        st.session_state.ai_path_positions = set()
        st.session_state.game_start_time = None

        st.rerun()


# ==================================================
# SCREEN ROUTING
# ==================================================

if st.session_state.screen == "menu":

    show_main_menu()

elif st.session_state.screen == "game":

    show_game_screen()

elif st.session_state.screen == "ending":

    show_ending_screen()
