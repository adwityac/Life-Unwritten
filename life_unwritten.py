import random

class Player:
    def __init__(self):
        self.mood = 50  # 0 = depressed, 100 = content and confident
        self.relationships = {"Friend": 50, "Mentor": 50, "Ex": 50, "Family": 50}
        self.current_location = "Park"
        self.past_choices = []

    def change_mood(self, change):
        self.mood += change
        self.mood = max(0, min(100, self.mood))  # Keep mood between 0 and 100

    def adjust_relationship(self, person, change):
        self.relationships[person] += change
        self.relationships[person] = max(0, min(100, self.relationships[person]))  # Clamped between 0 and 100

    def check_status(self):
        print(f"\nCurrent Mood: {self.mood}/100")
        print("Relationships Status:")
        for person, status in self.relationships.items():
            print(f"  {person}: {status}/100")
        print(f"\nCurrent Location: {self.current_location}")

    def add_past_choice(self, choice):
        self.past_choices.append(choice)

    def show_past_choices(self):
        if self.past_choices:
            print("\nPast Choices:")
            for choice in self.past_choices:
                print(f"- {choice}")
        else:
            print("\nNo past choices made yet.")

class NPC:
    def __init__(self, name, initial_relationship):
        self.name = name
        self.relationship_status = initial_relationship

    def interact(self, player):
        print(f"\nYou interact with {self.name}.")
        if self.relationship_status < 30:
            print(f"{self.name} seems distant, almost cold. There's tension in the air.")
        elif self.relationship_status < 60:
            print(f"{self.name} is somewhat neutral. They’re not angry, but they’re unsure about you.")
        else:
            print(f"{self.name} seems warm and welcoming, like nothing ever happened.")

    def offer_choice(self, player):
        print(f"\n{self.name} gives you a difficult choice to make.")
        choice = input("1. Reconnect and apologize.\n2. Ignore and move on.\nYour choice: ")
        if choice == '1':
            print(f"\nYou choose to reconnect with {self.name} and apologize for the past.")
            player.adjust_relationship(self.name, 20)
            player.add_past_choice(f"Apologized to {self.name}")
        elif choice == '2':
            print(f"\nYou choose to avoid the conversation with {self.name}.")
            player.adjust_relationship(self.name, -10)
            player.add_past_choice(f"Ignored {self.name}")
        else:
            print("\nInvalid choice. No action taken.")

# Game setup
def intro(player):
    print("Life Unwritten - A Journey of Choices")
    print("\nYou find yourself standing in the middle of a park. The world around you feels uncertain, like everything you've done in life has led you to this point.")
    print("You have the chance to reconnect with those who matter to you, reflect on your past decisions, and ultimately decide where you want your future to go.")

def game_loop(player):
    npc_friend = NPC("Old Friend", 50)
    npc_mentor = NPC("Mentor", 60)
    npc_ex = NPC("Ex-Partner", 40)
    npc_family = NPC("Family Member", 50)

    while player.mood > 0 and player.mood < 100:
        player.check_status()

        print("\nWhere do you want to go next?")
        print("1. Meet with your Old Friend.")
        print("2. Seek advice from your Mentor.")
        print("3. Talk to your Ex-Partner.")
        print("4. Visit a Family Member.")
        print("5. Reflect on your life.")
        print("6. Check past choices.")

        choice = input("Enter the number of your choice: ").strip()

        if choice == '1':
            npc_friend.interact(player)
            npc_friend.offer_choice(player)

        elif choice == '2':
            npc_mentor.interact(player)
            npc_mentor.offer_choice(player)

        elif choice == '3':
            npc_ex.interact(player)
            npc_ex.offer_choice(player)

        elif choice == '4':
            npc_family.interact(player)
            npc_family.offer_choice(player)

        elif choice == '5':
            print("\nYou sit on a bench, reflecting on your past decisions. You realize there are things you regret, but there's also potential for change.")
            player.change_mood(10)

        elif choice == '6':
            player.show_past_choices()

        else:
            print("\nInvalid choice. Please try again.")

        # Random mood impact based on previous actions
        if random.random() < 0.2:
            print("\nYou feel a wave of doubt and sadness about the past. Your mood drops.")
            player.change_mood(-5)

        # Check if game should end
        if player.mood <= 0:
            print("\nYou feel completely lost. You’ve fallen into a deep emotional slump and don’t know how to move forward.")
            print("The journey ends here. Perhaps it’s time to reflect on what’s next...")
            break
        elif player.mood >= 100:
            print("\nYou’ve come to terms with your past. You’ve made peace with yourself and others, and now you’re ready to move forward in life with clarity and purpose.")
            print("The journey ends here. You are at peace.")
            break

# Game start
if __name__ == "__main__":
    player = Player()
    intro(player)
    game_loop(player)
