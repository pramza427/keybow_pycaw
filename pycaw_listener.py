import keyboard
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from win10toast import ToastNotifier

MAX_VOLUME = 1.0
MIN_VOLUME = 0.0

volume_step = 0.1

# Groups of apps that we want to control at one time
apps = [
    #media apps
    ["Spotify.exe",
    "chrome.exe"],
    #com apps
    ["Discord.exe"]
]

# Joins all apps into a 1D array. Used to adjust volume of all apps that are not in any app list
all_apps = [j for arr in apps for j in arr]

# Starting position for the channels
# These values will be set every time the script is started
# indeces correspond to the apps indeces
current_vol = [0.5, 1.0, 0.4]


def mute_apps(idx):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:   
        volume = session._ctl.QueryInterface(ISimpleAudioVolume) 
        if session.Process and session.Process.name() in apps[idx]:   
            volume.SetMute(not volume.GetMute(), None)
       
def mute_others():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:   
        volume = session._ctl.QueryInterface(ISimpleAudioVolume) 
        if session.Process and session.Process.name() not in all_apps:
            volume.SetMute(not volume.GetMute(), None)

# Set the volume for all apps in the provided list
# doing it this way makes sure that all the apps in the list are at the same volume
def set_volume(app_list, vol_percent):
    sessions = AudioUtilities.GetAllSessions()   
    for session in sessions:   
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() in app_list:
            volume.SetMasterVolume(vol_percent, None)

def set_volume_other(vol_percent):
    sessions = AudioUtilities.GetAllSessions()   
    for session in sessions:   
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() not in all_apps:
            volume.SetMasterVolume(vol_percent, None)

# Set all volume levels equal to current_vol values
def set_volume_all():
    for idx, app_list in enumerate(apps):
        set_volume(app_list, current_vol[idx])
    set_volume_other(current_vol[-1])

def volume_up(idx):
    current_vol[idx] = min(MAX_VOLUME, current_vol[idx] + volume_step)
    if idx >= len(apps):
        set_volume_other(current_vol[idx])
    else:
        set_volume(apps[idx], current_vol[idx])

def volume_down(idx): 
    current_vol[idx] = max(MIN_VOLUME, current_vol[idx] - volume_step)
    if idx >= len(apps):
        set_volume_other(current_vol[idx])
    else:
        set_volume(apps[idx], current_vol[idx])




"""
My keybow is set up with these buttons: 
       (L1) (L2) (L3)
 Layer  -    =    \
  F15  F18  F21  F24
  F14  F17  F20  F23
  F13  F16  F19  F22
  Each column will act as an audio channel 'dial'
"""

# Music Listeners
keyboard.on_press_key("F15", lambda e: volume_up(0))
keyboard.on_press_key("F14", lambda e: volume_down(0))
keyboard.on_press_key("F13", lambda e: mute_apps(0))

# Coms Listeners
keyboard.on_press_key("F18", lambda e: volume_up(1))
keyboard.on_press_key("F17", lambda e: volume_down(1))
keyboard.on_press_key("F16", lambda e: mute_apps(1))

# Other Listeners
keyboard.on_press_key("F21", lambda e: volume_up(2))
keyboard.on_press_key("F20", lambda e: volume_down(2))
keyboard.on_press_key("F19", lambda e: mute_others())

# Reset all volume to current_vol levels
keyboard.on_press_key("F22", lambda e: set_volume_all())



# On startup set all volume levels to current_vol values
set_volume_all()

# Notify the user that the script is running in the background
toast = ToastNotifier()
toast.show_toast("Audio Adjuster", "Listening for F13-F24 keys", duration=10)

# keep the program running so it is always checking for keyboard inputs
keyboard.wait("")
