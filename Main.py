from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

import json
import os

Window.clearcolor = (0.05, 0.05, 0.08, 1)

# ----------------------------
# 💾 SAVE SYSTEM
# ----------------------------
SAVE_FILE = "save.json"

def load_state():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)

    return {
        "location": "village",
        "inventory": [],
        "world_memory": {
            "visited": [],
            "events": []
        }
    }

def save_state(state):
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)


# ----------------------------
# 🌍 WORLD
# ----------------------------
WORLD = {
    "village": {
        "desc": "A quiet mist-covered village. Lanterns sway in the wind.",
        "exits": ["forest"],
        "npcs": ["guard", "merchant"]
    },
    "forest": {
        "desc": "A dense forest where the trees feel like they are watching you.",
        "exits": ["village", "cave"],
        "npcs": ["wanderer"]
    },
    "cave": {
        "desc": "A dark cave. The air feels heavy and still.",
        "exits": ["forest"],
        "npcs": []
    }
}


# ----------------------------
# 🎲 DUNGEON MASTER (BASIC BUT STABLE)
# ----------------------------
def dm(state):
    loc = state["location"]
    mem = state["world_memory"]

    visits = mem["visited"]
    count = visits.count(loc)

    if count == 0:
        intro = "You arrive somewhere unfamiliar for the first time."
    elif count < 3:
        intro = "This place feels slightly familiar now."
    else:
        intro = "The world here feels like it remembers you."

    tension = (
        "Everything feels calm… for now."
        if len(mem["events"]) < 5
        else "The world feels like it is slowly reacting to your actions."
    )

    data = WORLD[loc]

    return f"""
🎲 DUNGEON MASTER

📍 LOCATION: {loc.upper()}
{intro}

🪵 {data['desc']}

🌍 WORLD STATE:
{tension}

🚪 Exits: {', '.join(data['exits'])}
🧍 NPCs: {', '.join(data['npcs']) if data['npcs'] else 'None'}
"""


# ----------------------------
# ⚙️ COMMAND ENGINE
# ----------------------------
def process(state, cmd):
    cmd = cmd.lower().strip()

    # LOOK
    if "look" in cmd or "around" in cmd:
        return dm(state)

    # INVENTORY
    if "inventory" in cmd:
        inv = state["inventory"]
        return "🎒 " + (", ".join(inv) if inv else "Empty")

    # MOVE
    if "go" in cmd:
        for place in WORLD[state["location"]]["exits"]:
            if place in cmd:
                state["location"] = place

                if place not in state["world_memory"]["visited"]:
                    state["world_memory"]["visited"].append(place)

                state["world_memory"]["events"].append(f"travelled to {place}")

                return dm(state)

        return "You can't go there. Exits: " + ", ".join(WORLD[state["location"]]["exits"])

    # TALK (placeholder for future NPC system)
    if "talk" in cmd:
        return "NPC system coming next upgrade..."

    return "Unknown command. Try: look, go, inventory"


# ----------------------------
# 📱 MOBILE UI (STABLE FOR ANDROID BUILD)
# ----------------------------
class Game(App):
    def build(self):
        self.state = load_state()

        root = BoxLayout(orientation="vertical")

        # OUTPUT
        self.output = Label(
            text="🎮 AI DUNGEON RPG\nType 'look' to begin.\n",
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.output.bind(texture_size=self.resize_text)

        scroll = ScrollView(size_hint=(1, 0.9))
        self.output.text_size = (Window.width - dp(20), None)
        scroll.add_widget(self.output)

        # INPUT
        self.input = TextInput(
            size_hint=(1, 0.1),
            multiline=False,
            hint_text="Type command..."
        )

        self.input.bind(on_text_validate=self.enter)

        root.add_widget(scroll)
        root.add_widget(self.input)

        # initial scene
        self.output.text += "\n" + dm(self.state)

        return root

    def resize_text(self, *args):
        self.output.text_size = (Window.width - dp(20), None)
        self.output.height = self.output.texture_size[1]

    def enter(self, instance):
        cmd = self.input.text
        self.input.text = ""

        result = process(self.state, cmd)

        self.output.text += f"\n\n> {cmd}\n{result}\n"

        save_state(self.state)


if __name__ == "__main__":
    Game().run()