# Vanilla-Dance-Dance-Revolution

While most of us are glued to our seats to complete an assignment or project and thus most of us dismiss the idea of exercising due to laziness or tiredness. Moreover, it is important for us – youths to build a strong connection with our peers as a form of moral support. Hence, to encourage some light exercise during our spare time and to foster bonds with our fellow peers, we created a vanilla version of Dance Dance Revolution (DDR). 

It is simple and quick to install, perfect for creating a recreational corner in Think Tank Rooms. This game requires mainly 3 components: (1) an external input device and (2) an external monitor screen – both of which are connected to (3) a raspberry pi. The external input device can be either pressure plates or buttons placed on the floor to act as a dance platform for the players. The external input device is then connected to a raspberry pi which runs our python programme. For greater immersion, the larger the external monitor screen, the better. 

**To play the game**
Download the assets file and download either keyboard_controlled_game.py to play the game with only keyboard or download raspberry_game.py for an external buttons input.


**Current problems**
1. Hitboxes of arrow can be quite janky.
2. Scaling of Tkinter window is not dynamic and thus the hitboxes can be quite off with larger screens.
3. There is no replaybility - could not implement a replay button.
