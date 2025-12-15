import keyboard
import time
import random
KEYS = ["l", "t", "f1"]
print("Pressing F1 key at random intervals between 5 to 10 minutes. Press Ctrl+C to stop.")

def keep_alive():
    """Simulates pressing F1 twice with a short delay."""
    for key in KEYS:
        keyboard.press_and_release(key)
        time.sleep(1)  # Slight delay to simulate a real press
        keyboard.press_and_release(key)

try:
    time.sleep(5)  # Initial delay before first key press
    keep_alive()  # First F1 key press
    while True:
        interval = random.randint(10 * 60, 14 * 60)  # Random interval between 5-10 minutes
        print(f"Pressing in {interval // 60} minutes.")
        time.sleep(interval)  # Wait for the randomized interval
        keep_alive()  # Execute the F1 key press
        print(f"{KEYS} key pressed.")

except KeyboardInterrupt:
    print("\nScript stopped by user.")
