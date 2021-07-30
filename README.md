# LoadStar
> Load removal tool designed for speedruns of Cooking Mama Cookstar

## Getting started

### First time quick setup

1. Setup the requirements below

- Livesplit
- [Livesplit.Server](https://github.com/LiveSplit/LiveSplit.Server) added to your layout.
- A console connected via a capture card to a PC
- OBS VirtualCam added as a filter to a scene containing just your capture card and running
- Python 3.8 or higher


Detailed instructions for Livesplit.Server and VirtualCam are below the quick setup.


2. Open PowerShell (Windows) or the Terminal (Mac/Linux) and type `pip install loadstar`

3. Type `python -m loadstar` to start the program!

### Running in future

1. Make sure VirtualCam and Livesplit.Server are both running - details below on how to do this.

2. Open PowerShell (Windows) or the Terminal (Mac/Linux)

3. Type `python -m loadstar` to start the program!

### Detailed

#### Setting up Livesplit.Server

The latest dev builds of Livesplit come with LiveSplit server pre-packaged. Otherwise, follow the instructions [here](https://github.com/LiveSplit/LiveSplit.Server) to install LiveSplit server.

Once it's installed, add it to your Livesplit layout, and right click LiveSplit, go to "Control" and click "Start Server". You'll have to do this last little step every time

#### Setting up OBS

OBS isn't *technically* required, but, helps a ton as you'll likely be recording / streaming while speedrunning, and Windows has weird times with one video device being used by two processes at once. VirtualCam lets us take the input of your capture card into OBS, and then pipe it back out again as another virtual device.

Simply: Capture Card -> OBS -> VirtualCam -> Loadstar

First up, install OBS, and add your capture card to **a scene on it's own**. If you already have OBS setup and installed, add your capture card on a scene just by itself - you can embed scenes in other scenes in OBS, so you can still have it inside your pretty overlay.

Then, close OBS, and install [OBS VirtualCam](https://obsproject.com/forum/resources/obs-VirtualCam.949/) - the built in Virtual Camera, while functional, will always output the active scene. VirtualCam allows us to output a specific scene always to a virtual camera. During setup, click one camera - we don't need anymore.

Once installed, right click the scene you just made in the "Scenes" list, and click  "Filters".

Navigate to the plus at the bottom, and click "VirtualCam". Click OK to add it as a filter.

Click onto the new filter in the sidebar if it isn't selected, then click "Start" to start up VirtualCam.

You can now close the filters panel, and navigate to other scenes - VirtualCam will always be outputting *this* specific scene. If you want to include your capture card on other scenes, embed this scene instead of adding a new video device - adding a duplicate video device source may cause OBS to conflict with itself.

## How does this work?

Cooking Mama cookstar fades to black on the PlayStation version of the game (used for speedrunning) during loads. As such, if the captured video feed is entirely black, we know the game is loading, and we can send a command to Livesplit via Livesplit.server to pause the in-game time!

## Libraries used

- `livesplit-python` by a certain Vallerie Knight (me!)
- `opencv-python` - for image capture and analysis
- `click` - for command line output

## Credits

- The contributors to Livesplit, Livesplit.Server, OBS, opencv, click, and the Python project - without all of these amazing open source projects, this wouldn't exist
- The Cooking Mama Speedrunning Discord and Speedrunning.com mod team
- I guess the people who worked on Cookstar, bless them, for making such a silly (if kinda bad) game to speedrun
- Laura Kate Date (LauraKBuzz in all the places - [twitch](twitch.tv/laurakbuzz), [twitter](twitter.com/laurakbuzz), [patreon](patreon.com/laurakbuzz)) for being such a wonderful anime rival in speedrunning