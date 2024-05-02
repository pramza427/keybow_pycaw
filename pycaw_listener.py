import keyboard
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# setting this to True will print all current Audio sessions then close the program on any keyboard input
# otherwise it will run the program and watch for F13-F24 inputs
PRINT_SESSIONS = True

MAX_VOLUME = 1.0
MIN_VOLUME = 0.0

# Groups of apps that we want to control at one time
music_apps = [
    "Spotify.exe",
    "chrome.exe"
]

com_apps = [
    "Discord.exe"
]


def mute_apps(apps = None):      
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:   
        volume = session._ctl.QueryInterface(ISimpleAudioVolume) 
        if apps:
            if session.Process and session.Process.name() in apps:   
                volume.SetMute(not volume.GetMute(), None)
        else:
            if session.Process and session.Process.name() not in music_apps + com_apps:
                volume.SetMute(not volume.GetMute(), None)


def volume_up(apps = None):   
    decibels = 0.1
    sessions = AudioUtilities.GetAllSessions()   
    for session in sessions:   
        volume = session.SimpleAudioVolume
        if apps:
            if session.Process and session.Process.name() in apps: 
                current_volume = volume.GetMasterVolume()
                new_volume = min(MAX_VOLUME, current_volume + decibels) 
                volume.SetMasterVolume(new_volume, None)
        else:
            if session.Process and session.Process.name() not in music_apps + com_apps:
                current_volume = volume.GetMasterVolume()
                new_volume = min(MAX_VOLUME, current_volume + decibels) 
                volume.SetMasterVolume(new_volume, None)


def volume_down(apps = None): 
    decibels = 0.1
    sessions = AudioUtilities.GetAllSessions()   
    for session in sessions:   
        volume = session.SimpleAudioVolume
        if apps:
            if session.Process and session.Process.name() in apps:
                current_volume = volume.GetMasterVolume()
                new_volume = max(MIN_VOLUME, current_volume - decibels) 
                volume.SetMasterVolume(new_volume, None)
        else:
            if session.Process and session.Process.name() not in music_apps + com_apps:
                current_volume = volume.GetMasterVolume()
                new_volume = max(MIN_VOLUME, current_volume - decibels) 
                volume.SetMasterVolume(new_volume, None)


def on_press(key):
    if keyboard.is_pressed("alt+F13"):  
        mute_apps(music_apps)  
    elif keyboard.is_pressed("alt+F14"):  
        volume_down(music_apps)  
    elif keyboard.is_pressed("alt+F15"):  
        volume_up(music_apps) 

    elif keyboard.is_pressed("alt+F16"):  
        mute_apps(com_apps)  
    elif keyboard.is_pressed("alt+F17"):  
        volume_down(com_apps)
    elif keyboard.is_pressed("alt+F18"):  
        volume_up(com_apps)   

    elif keyboard.is_pressed("alt+F19"):  
        mute_apps()
    elif keyboard.is_pressed("alt+F20"):
        volume_down() 
    elif keyboard.is_pressed("alt+F21"):  
        volume_up()

keyboard.on_press(on_press)  


if PRINT_SESSIONS:
    # Helper function to check the names of all current Audio Sessions
    print("List of audio session names:")
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            print(session.Process.name())
    keyboard.wait("")
else:
    # keep the program running so it is always checking for keyboard inputs
    while True:   
        pass  


