import random
import time
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class Character:
    name: str
    relationship: str
    bond_level: int  # 0-100
    last_interaction: str
    backstory: str
    current_mood: str

class GameState:
    def __init__(self):
        self.player_name = ""
        self.mood = 50  # 0-100, 50 is neutral
        self.day = 1
        self.choices_made = []
        self.characters = {}
        self.game_over = False
        self.reflection_count = 0
        
    def save_choice(self, choice_description: str, impact: str):
        self.choices_made.append({
            'day': self.day,
            'choice': choice_description,
            'impact': impact,
            'mood_at_time': self.mood
        })

class LifeUnwritten:
    def __init__(self):
        self.state = GameState()
        self.initialize_characters()
        
    def initialize_characters(self):
        """Initialize the NPCs with their relationships and backstories"""
        characters_data = {
            "Maya": Character(
                name="Maya",
                relationship="Best Friend",
                bond_level=60,
                last_interaction="You haven't spoken in months after a disagreement",
                backstory="Your college roommate who became your closest friend. You had a falling out over a misunderstanding.",
                current_mood="distant"
            ),
            "David": Character(
                name="David",
                relationship="Mentor",
                bond_level=40,
                last_interaction="He offered career advice you didn't take",
                backstory="Your former boss who saw potential in you but felt you weren't living up to it.",
                current_mood="disappointed"
            ),
            "Sarah": Character(
                name="Sarah",
                relationship="Sister",
                bond_level=30,
                last_interaction="A heated argument about family responsibilities",
                backstory="Your younger sister who feels you've been absent from family events.",
                current_mood="hurt"
            ),
            "Alex": Character(
                name="Alex",
                relationship="Former Partner",
                bond_level=20,
                last_interaction="An awkward goodbye after your breakup",
                backstory="Your ex-partner who still cares about you but feels you both made mistakes.",
                current_mood="conflicted"
            )
        }
        self.state.characters = characters_data
    
    def clear_screen(self):
        """Clear the terminal screen"""
        print("\n" * 50)
    
    def print_header(self):
        """Display the game header"""
        print("="*60)
        print(" " * 15 + "🎮 LIFE UNWRITTEN 🎮")
        print(" " * 17 + "A Journey of Choices")
        print("="*60)
        print(f"Day {self.state.day} | Mood: {self.get_mood_description()} ({self.state.mood}/100)")
        print("-"*60)
    
    def get_mood_description(self):
        """Convert mood number to description"""
        if self.state.mood >= 80:
            return "Excellent 😊"
        elif self.state.mood >= 60:
            return "Good 🙂"
        elif self.state.mood >= 40:
            return "Okay 😐"
        elif self.state.mood >= 20:
            return "Low 😔"
        else:
            return "Terrible 😞"
    
    def print_slow(self, text: str, delay: float = 0.03):
        """Print text with a typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def get_user_input(self, prompt: str) -> str:
        """Get user input with a formatted prompt"""
        return input(f"\n💭 {prompt}: ").strip()
    
    def start_game(self):
        """Initialize the game and get player name"""
        self.clear_screen()
        self.print_header()
        
        print("\n🌟 Welcome to Life Unwritten 🌟")
        print("\nIn this journey, you'll navigate relationships, make important choices,")
        print("and reflect on your path through life. Every decision matters.")
        
        self.state.player_name = self.get_user_input("What's your name?")
        
        if not self.state.player_name:
            self.state.player_name = "Traveler"
        
        self.print_slow(f"\nHello, {self.state.player_name}. Your story begins now...")
        time.sleep(2)
        
        self.show_opening_story()
    
    def show_opening_story(self):
        """Display the opening narrative"""
        self.clear_screen()
        self.print_header()
        
        story = f"""
📖 Chapter 1: Reflection

{self.state.player_name}, you find yourself at a crossroads in life. 
Looking back, you realize that some of your most important relationships 
have grown distant due to choices you've made - or failed to make.

Your phone sits on the table with several unread messages. Your calendar 
shows missed family events. The weight of disconnection sits heavy on 
your shoulders.

But today feels different. Today, you have the chance to reconnect, 
to rebuild, and to rediscover what truly matters.

The question is: where do you begin?
"""
        
        self.print_slow(story, 0.05)
        input("\nPress Enter to continue...")
        self.main_menu()
    
    def main_menu(self):
        """Display the main game menu"""
        while not self.state.game_over:
            self.clear_screen()
            self.print_header()
            
            print(f"\n🏠 What would you like to do today, {self.state.player_name}?")
            print("\n1. 💬 Reach out to someone")
            print("2. 🪞 Reflect on your journey")
            print("3. 📚 Review your past choices")
            print("4. 📊 Check relationship status")
            print("5. 🚪 End the day")
            print("6. ❌ Quit game")
            
            choice = self.get_user_input("Choose an option (1-6)")
            
            if choice == "1":
                self.character_interaction_menu()
            elif choice == "2":
                self.reflection_menu()
            elif choice == "3":
                self.review_choices()
            elif choice == "4":
                self.show_relationship_status()
            elif choice == "5":
                self.end_day()
            elif choice == "6":
                self.quit_game()
            else:
                print("❌ Invalid choice. Please try again.")
                time.sleep(1)
    
    def character_interaction_menu(self):
        """Show available characters to interact with"""
        self.clear_screen()
        self.print_header()
        
        print(f"\n💬 Who would you like to reach out to, {self.state.player_name}?")
        print("\nYour relationships:")
        
        for i, (name, char) in enumerate(self.state.characters.items(), 1):
            bond_status = self.get_bond_description(char.bond_level)
            print(f"{i}. {char.name} ({char.relationship}) - {bond_status}")
            print(f"   Last interaction: {char.last_interaction}")
        
        print(f"{len(self.state.characters) + 1}. 🔙 Go back")
        
        choice = self.get_user_input("Choose someone to contact (number)")
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(self.state.characters):
                char_name = list(self.state.characters.keys())[choice_num - 1]
                self.interact_with_character(char_name)
            elif choice_num == len(self.state.characters) + 1:
                return
            else:
                print("❌ Invalid choice.")
                time.sleep(1)
        except ValueError:
            print("❌ Please enter a valid number.")
            time.sleep(1)
    
    def get_bond_description(self, bond_level: int) -> str:
        """Convert bond level to description"""
        if bond_level >= 80:
            return "💚 Strong Bond"
        elif bond_level >= 60:
            return "💛 Good Connection"
        elif bond_level >= 40:
            return "🧡 Strained"
        elif bond_level >= 20:
            return "❤️ Distant"
        else:
            return "💔 Broken"
    
    def interact_with_character(self, char_name: str):
        """Handle interaction with a specific character"""
        character = self.state.characters[char_name]
        
        self.clear_screen()
        self.print_header()
        
        print(f"\n📱 Reaching out to {character.name} ({character.relationship})")
        print(f"Current bond: {self.get_bond_description(character.bond_level)}")
        print(f"\n📖 Background: {character.backstory}")
        
        # Generate interaction scenarios based on character and bond level
        scenarios = self.get_interaction_scenarios(character)
        
        print(f"\n💭 {character.name} responds to your message...")
        time.sleep(2)
        
        print(f"\n'{scenarios['response']}'")
        print(f"\nHow do you respond?")
        
        for i, option in enumerate(scenarios['options'], 1):
            print(f"{i}. {option['text']}")
        
        choice = self.get_user_input("Your choice")
        
        try:
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(scenarios['options']):
                self.process_interaction_choice(character, scenarios['options'][choice_num])
            else:
                print("❌ Invalid choice.")
                time.sleep(1)
        except ValueError:
            print("❌ Please enter a valid number.")
            time.sleep(1)
    
    def get_interaction_scenarios(self, character: Character) -> Dict[str, Any]:
        """Generate interaction scenarios based on character relationship"""
        scenarios = {
            "Maya": {
                "response": "Oh... hi. I wasn't expecting to hear from you. How have you been?",
                "options": [
                    {"text": "I've been thinking about our fight. I'm sorry.", "bond_change": 15, "mood_change": 5},
                    {"text": "I wanted to catch up like old times.", "bond_change": 8, "mood_change": 3},
                    {"text": "I need someone to talk to.", "bond_change": 5, "mood_change": 2}
                ]
            },
            "David": {
                "response": "Good to hear from you. I hope you've been considering what we discussed about your career path.",
                "options": [
                    {"text": "You were right. I should have listened to your advice.", "bond_change": 20, "mood_change": 8},
                    {"text": "I've been exploring new opportunities.", "bond_change": 12, "mood_change": 5},
                    {"text": "I'm happy with my current path.", "bond_change": -5, "mood_change": -2}
                ]
            },
            "Sarah": {
                "response": "I'm surprised you're calling. Mom's been asking about you again.",
                "options": [
                    {"text": "I know I've been absent. I want to change that.", "bond_change": 18, "mood_change": 6},
                    {"text": "How is everyone? I've been busy with work.", "bond_change": 5, "mood_change": 1},
                    {"text": "I'll try to visit soon.", "bond_change": 8, "mood_change": 3}
                ]
            },
            "Alex": {
                "response": "Hey... this is unexpected. I hope you're doing well.",
                "options": [
                    {"text": "I miss what we had. Can we talk?", "bond_change": 10, "mood_change": -5},
                    {"text": "I wanted to apologize for how things ended.", "bond_change": 15, "mood_change": 5},
                    {"text": "I hope we can be friends someday.", "bond_change": 8, "mood_change": 2}
                ]
            }
        }
        
        return scenarios.get(character.name, {
            "response": "Hello there. It's been a while.",
            "options": [
                {"text": "I wanted to reconnect.", "bond_change": 10, "mood_change": 3},
                {"text": "How have you been?", "bond_change": 5, "mood_change": 2}
            ]
        })
    
    def process_interaction_choice(self, character: Character, choice: Dict[str, Any]):
        """Process the outcome of an interaction choice"""
        old_bond = character.bond_level
        old_mood = self.state.mood
        
        # Apply changes
        character.bond_level = max(0, min(100, character.bond_level + choice['bond_change']))
        self.state.mood = max(0, min(100, self.state.mood + choice['mood_change']))
        
        # Update last interaction
        character.last_interaction = choice['text']
        
        # Save the choice
        impact = f"Bond with {character.name}: {old_bond} → {character.bond_level}, Mood: {old_mood} → {self.state.mood}"
        self.state.save_choice(f"Talked to {character.name}: {choice['text']}", impact)
        
        # Show outcome
        print(f"\n✨ Outcome:")
        print(f"Bond with {character.name}: {old_bond} → {character.bond_level}")
        print(f"Your mood: {old_mood} → {self.state.mood}")
        
        # Generate follow-up response
        follow_up = self.generate_follow_up_response(character, choice['bond_change'])
        print(f"\n{character.name}: '{follow_up}'")
        
        input("\nPress Enter to continue...")
    
    def generate_follow_up_response(self, character: Character, bond_change: int) -> str:
        """Generate a follow-up response based on the interaction outcome"""
        if bond_change > 15:
            responses = [
                "Thank you for reaching out. This means a lot to me.",
                "I'm glad we're talking again. I've missed this.",
                "You don't know how much I needed to hear that."
            ]
        elif bond_change > 5:
            responses = [
                "It's good to hear from you. Let's talk more soon.",
                "I appreciate you taking the time to connect.",
                "This is a good start. I'm glad you called."
            ]
        elif bond_change > 0:
            responses = [
                "Well, it's something. Thanks for reaching out.",
                "I'm glad you called, even if things are still complicated.",
                "We still have a lot to work through, but this is a start."
            ]
        else:
            responses = [
                "I'm not sure what you expected me to say.",
                "This doesn't really change anything between us.",
                "I think we both need more time."
            ]
        
        return random.choice(responses)
    
    def reflection_menu(self):
        """Handle personal reflection to improve mood"""
        self.clear_screen()
        self.print_header()
        
        if self.state.reflection_count >= 2:
            print("🪞 You've spent enough time reflecting today.")
            print("Sometimes action is better than contemplation.")
            input("\nPress Enter to continue...")
            return
        
        print("🪞 Time for reflection...")
        print("\nTaking a moment to think about your journey can help clarify your thoughts")
        print("and improve your emotional well-being.")
        
        reflections = [
            {
                "prompt": "What relationship in your life brings you the most joy?",
                "responses": [
                    "Focus on gratitude for the people who support you",
                    "Remember the laughter and shared memories",
                    "Appreciate the unconditional love in your life"
                ]
            },
            {
                "prompt": "What's one mistake you've learned from recently?",
                "responses": [
                    "Growth comes from acknowledging our imperfections",
                    "Every mistake is a lesson in disguise",
                    "Forgiveness starts with forgiving yourself"
                ]
            },
            {
                "prompt": "What are you most grateful for today?",
                "responses": [
                    "Gratitude transforms ordinary moments into blessings",
                    "The simple act of appreciation can shift your entire perspective",
                    "Even small things deserve recognition and thanks"
                ]
            }
        ]
        
        reflection = random.choice(reflections)
        
        print(f"\n💭 Reflection: {reflection['prompt']}")
        
        for i, response in enumerate(reflection['responses'], 1):
            print(f"{i}. {response}")
        
        choice = self.get_user_input("Choose your reflection")
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(reflection['responses']):
                mood_boost = random.randint(8, 15)
                old_mood = self.state.mood
                self.state.mood = min(100, self.state.mood + mood_boost)
                self.state.reflection_count += 1
                
                print(f"\n✨ You feel more centered and peaceful.")
                print(f"Mood: {old_mood} → {self.state.mood}")
                
                # Save the reflection
                self.state.save_choice(
                    f"Reflected on: {reflection['prompt']}", 
                    f"Mood boost: +{mood_boost}"
                )
                
                input("\nPress Enter to continue...")
            else:
                print("❌ Invalid choice.")
                time.sleep(1)
        except ValueError:
            print("❌ Please enter a valid number.")
            time.sleep(1)
    
    def review_choices(self):
        """Show the player's choice history"""
        self.clear_screen()
        self.print_header()
        
        print("📚 Your Journey So Far")
        
        if not self.state.choices_made:
            print("\nYou haven't made any significant choices yet.")
            print("Your story is just beginning...")
        else:
            print(f"\nChoices made: {len(self.state.choices_made)}")
            print("-" * 50)
            
            for i, choice in enumerate(self.state.choices_made[-10:], 1):  # Show last 10 choices
                print(f"\nDay {choice['day']}: {choice['choice']}")
                print(f"Impact: {choice['impact']}")
                print(f"Mood at time: {choice['mood_at_time']}")
        
        input("\nPress Enter to continue...")
    
    def show_relationship_status(self):
        """Display current relationship status with all characters"""
        self.clear_screen()
        self.print_header()
        
        print("📊 Relationship Status Report")
        print("=" * 40)
        
        total_bond = 0
        for char in self.state.characters.values():
            bond_desc = self.get_bond_description(char.bond_level)
            print(f"\n{char.name} ({char.relationship})")
            print(f"Bond Level: {char.bond_level}/100 - {bond_desc}")
            print(f"Current mood: {char.current_mood}")
            print(f"Last interaction: {char.last_interaction}")
            total_bond += char.bond_level
        
        avg_bond = total_bond / len(self.state.characters)
        print(f"\n📈 Overall Relationship Health: {avg_bond:.1f}/100")
        
        if avg_bond >= 70:
            print("🌟 Your relationships are thriving!")
        elif avg_bond >= 50:
            print("🌱 Your relationships are growing stronger.")
        elif avg_bond >= 30:
            print("⚠️ Your relationships need attention.")
        else:
            print("🚨 Your relationships are in crisis.")
        
        input("\nPress Enter to continue...")
    
    def end_day(self):
        """End the current day and show progress"""
        self.clear_screen()
        self.print_header()
        
        print(f"🌅 Day {self.state.day} comes to an end...")
        
        # Calculate day's progress
        total_bond = sum(char.bond_level for char in self.state.characters.values())
        avg_bond = total_bond / len(self.state.characters)
        
        print(f"\n📊 Today's Summary:")
        print(f"Mood: {self.get_mood_description()}")
        print(f"Average relationship strength: {avg_bond:.1f}/100")
        print(f"Choices made today: {len([c for c in self.state.choices_made if c['day'] == self.state.day])}")
        
        # Check for game ending conditions
        if avg_bond >= 75 and self.state.mood >= 70:
            self.good_ending()
        elif avg_bond <= 20 and self.state.mood <= 30:
            self.bad_ending()
        elif self.state.day >= 7:  # Game ends after 7 days
            self.neutral_ending()
        else:
            self.state.day += 1
            self.state.reflection_count = 0  # Reset daily reflection limit
            
            print(f"\n🌄 Tomorrow is Day {self.state.day}.")
            print("What will you choose to do?")
            
            input("\nPress Enter to continue...")
    
    def good_ending(self):
        """Show the good ending"""
        self.clear_screen()
        self.print_header()
        
        ending_text = f"""
🌟 ENDING: A Life Rewritten 🌟

{self.state.player_name}, you've done something remarkable. Through conscious choices,
genuine reflection, and the courage to reach out, you've transformed not just 
your relationships, but yourself.

Looking at your phone now, you see messages filled with warmth and connection.
Your calendar shows upcoming gatherings with people who matter. The weight 
that once sat on your shoulders has lifted, replaced by a sense of purpose 
and belonging.

Your relationships have flourished:
"""
        
        self.print_slow(ending_text, 0.04)
        
        for char in self.state.characters.values():
            status = "thriving" if char.bond_level >= 70 else "much stronger"
            print(f"• {char.name}: Your {char.relationship.lower()} bond is {status}")
        
        final_text = f"""
Most importantly, you've learned that relationships require intention, 
vulnerability, and consistent effort. You've rewritten your story from 
one of isolation to one of connection.

Your mood: {self.get_mood_description()}
Days played: {self.state.day}
Choices made: {len(self.state.choices_made)}

The future looks bright, {self.state.player_name}. 
Your life is no longer unwritten - it's being authored with love.

🎉 Congratulations! You've achieved the best possible ending! 🎉
"""
        
        self.print_slow(final_text, 0.04)
        self.state.game_over = True
        input("\nPress Enter to finish...")
    
    def bad_ending(self):
        """Show the bad ending"""
        self.clear_screen()
        self.print_header()
        
        ending_text = f"""
😔 ENDING: The Weight of Silence 😔

{self.state.player_name}, despite having opportunities to reconnect and heal,
the gap between you and those who matter most has only grown wider.

Your phone remains mostly silent. Your calendar shows missed opportunities.
The weight on your shoulders has grown heavier, and loneliness has become 
a constant companion.

Your relationships reflect the distance:
"""
        
        self.print_slow(ending_text, 0.04)
        
        for char in self.state.characters.values():
            status = "broken" if char.bond_level <= 20 else "severely strained"
            print(f"• {char.name}: Your {char.relationship.lower()} bond is {status}")
        
        final_text = f"""
But remember, {self.state.player_name} - this is just one ending to your story.
In real life, it's never too late to reach out, to apologize, to try again.
Every day offers new chances to rewrite your relationships.

Your mood: {self.get_mood_description()}
Days played: {self.state.day}
Choices made: {len(self.state.choices_made)}

Perhaps it's time to try a different approach...

💫 Your story doesn't have to end here. 💫
"""
        
        self.print_slow(final_text, 0.04)
        self.state.game_over = True
        input("\nPress Enter to finish...")
    
    def neutral_ending(self):
        """Show the neutral ending"""
        self.clear_screen()
        self.print_header()
        
        ending_text = f"""
🌅 ENDING: A Journey Continues 🌅

{self.state.player_name}, you've taken steps on a path that many never 
dare to walk. You've reached out, reflected, and made choices - some 
more successful than others.

Your relationships are a mixed tapestry of progress and setbacks, 
much like real life. Some bonds have strengthened, others remain 
fragile, but you've learned that change takes time and patience.

Your relationships show varied progress:
"""
        
        self.print_slow(ending_text, 0.04)
        
        for char in self.state.characters.values():
            if char.bond_level >= 60:
                status = "much stronger"
            elif char.bond_level >= 40:
                status = "showing improvement"
            else:
                status = "still needs work"
            print(f"• {char.name}: Your {char.relationship.lower()} bond is {status}")
        
        final_text = f"""
What matters most is that you've begun the journey. You've learned that 
relationships are like gardens - they require consistent care, patience, 
and sometimes forgiveness when things don't go as planned.

Your mood: {self.get_mood_description()}
Days played: {self.state.day}
Choices made: {len(self.state.choices_made)}

The story of your relationships is still being written, {self.state.player_name}.
Keep choosing connection over isolation, understanding over judgment.

🌱 Your journey of growth continues... 🌱
"""
        
        self.print_slow(final_text, 0.04)
        self.state.game_over = True
        input("\nPress Enter to finish...")
    
    def quit_game(self):
        """Handle game quit"""
        print("\n👋 Thanks for playing Life Unwritten!")
        print("Remember: In real life, it's never too late to reach out to someone you care about.")
        self.state.game_over = True

def main():
    """Main game loop"""
    try:
        game = LifeUnwritten()
        game.start_game()
        
        while not game.state.game_over:
            game.main_menu()
            
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing Life Unwritten!")
        print("Your story continues in real life...")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Sometimes life has unexpected turns. Try again!")

if __name__ == "__main__":
    main()