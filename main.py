import time
import datetime
import os
import json
import math

# ================== TERMINAL COLORS ==================
RESET = "\033[0m"
BOLD = "\033[1m"
NEON = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"

class HabitApp:
    DB_FILE = "habit_data.json"
    
    def __init__(self):
        self.energy_levels = {
            "1": ("Low", 15, "☕"),
            "2": ("Medium", 25, "⚡"),
            "3": ("High", 45, "🔥"),
        }
        self.load_data()

    def load_data(self):
        if os.path.exists(self.DB_FILE):
            try:
                with open(self.DB_FILE, "r") as f:
                    data = json.load(f)
                    data["history"] = [datetime.date.fromisoformat(d) for d in data.get("history", [])]
                    self.habit = data
            except: self.init_default_habit()
        else:
            self.init_default_habit()

    def init_default_habit(self):
        self.habit = {
            "name": "Study",
            "level": 1,
            "minutes": 5,
            "xp": 0,
            "streak": 0,
            "history": [],
        }

    def save_data(self):
        data = self.habit.copy()
        data["history"] = [d.isoformat() for d in data["history"]]
        with open(self.DB_FILE, "w") as f:
            json.dump(data, f)

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def draw_progress_bar(self, percent, width=30):
        filled = int(width * percent / 100)
        bar = f"{GREEN}━" * filled + f"{GRAY}━" * (width - filled)
        return f"[{bar}{RESET}] {percent}%"

    def banner(self):
        print(f"{NEON}{BOLD}")
        print(" 🌌  HABIT BUILDER ULTIMATE  🌌 ")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + RESET)

    def get_stats(self):
        today = datetime.date.today()
        h = self.habit
        history = h["history"]
        
        # Consistency
        consist = sum(1 for d in history if (today - d).days <= 21)
        
        # Streak calculation
        streak = 0
        check_date = today
        while any(d == check_date for d in history):
            streak += 1
            check_date -= datetime.timedelta(days=1)
        
        # XP and Leveling (Simplified RPG mechanic)
        xp_to_next = 100 * h["level"]
        xp_percent = min(100, int((h["xp"] / xp_to_next) * 100))
        
        return consist, streak, xp_to_next, xp_percent

    def show_dashboard(self):
        consist, streak, xp_to_next, xp_percent = self.get_stats()
        h = self.habit
        
        print(f"{WHITE}{BOLD}Habit: {h['name'].upper()} {RESET}")
        print(f"{PURPLE}Rank: {['Novice', 'Apprentice', 'Master'][h['level']-1]} (Lvl {h['level']})")
        print(f"{self.draw_progress_bar(xp_percent)}")
        print(f"{GRAY}XP: {h['xp']}/{xp_to_next} | 🔥 Streak: {streak} days")
        print(f"Consistency: {consist}/21 days{RESET}")
        print(f"{NEON}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")

    def run_timer(self, minutes):
        self.clear()
        self.banner()
        print(f"{YELLOW}🎯 FOCUSING FOR {minutes} MINUTES...{RESET}\n")
        
        seconds = minutes * 60
        total_seconds = seconds
        try:
            while seconds > 0:
                mins, secs = divmod(seconds, 60)
                progress = 100 - int((seconds / total_seconds) * 100)
                
                # Visual Timer UI
                print(f"\r{WHITE}{BOLD} {mins:02d}:{secs:02d} {RESET} {self.draw_progress_bar(progress, 20)}", end="", flush=True)
                time.sleep(1)
                seconds -= 1
            
            print(f"{GREEN}\n\n✨ MISSION ACCOMPLISHED! +25 XP{RESET}")
            return True
        except KeyboardInterrupt:
            print(f"{RED}\n\n⚠️ SESSION ABORTED.{RESET}")
            return False

    def start(self):
        while True:
            self.clear()
            self.banner()
            self.show_dashboard()

            print(f"{WHITE}How are you feeling today?{RESET}")
            for k, (name, t, icon) in self.energy_levels.items():
                print(f" {k}. {icon} {name:<8} {GRAY}({t} min session){RESET}")
            print(f" 0. 🚪 Exit\n")

            choice = input(f"{NEON}Select an action: {RESET}")
            if choice == "0": break
            if choice not in self.energy_levels: continue

            name, p_time, icon = self.energy_levels[choice]
            
            self.clear()
            self.banner()
            print(f"{WHITE}MODE: {icon} {name.upper()}{RESET}")
            print(f"{GRAY}You need to focus for {p_time} minutes to gain XP.{RESET}\n")
            
            if input(f"{YELLOW}Ready to start? (y/n): {RESET}").lower() == 'y':
                if self.run_timer(p_time):
                    today = datetime.date.today()
                    if not any(d == today for d in self.habit["history"]):
                        self.habit["history"].append(today)
                    
                    self.habit["xp"] += 25
                    
                    # Level up logic
                    xp_needed = 100 * self.habit["level"]
                    if self.habit["xp"] >= xp_needed:
                        self.habit["level"] = min(3, self.habit["level"] + 1)
                        self.habit["xp"] = 0
                        print(f"{YELLOW}{BOLD}\n🌟 LEVEL UP! You are now a {['Novice', 'Apprentice', 'Master'][self.habit['level']-1]}{RESET}")
                    
                    self.save_data()
                    input(f"\n{GRAY}Press Enter to continue...{RESET}")
            else:
                print(f"{RED}\nTaking a break is fine. See you later!{RESET}")
                time.sleep(1.5)

if __name__ == "__main__":
    try:
        HabitApp().start()
    except EOFError:
        pass
