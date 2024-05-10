import keyboard
from pycaw.pycaw import AudioUtilities

# Helper function to check the names of all current Audio Sessions
print("List of audio session names:")
sessions = AudioUtilities.GetAllSessions()
for session in sessions:
    if session.Process:
        print(session.Process.name())
# Wait for input before closing
keyboard.read_event()