<h1>
    <img src="md_images/logo.png" align="left" height="108">
    SecuroSurf
</h1>

<p><b>A GTA Online PC Firewall</b></p>

------------------------------------------------------------------------------------------------------------------------

[**Downloads**](./) 🔹
[User Manual](README.md#user-manual) 🔹
[FAQs](README.md#faqs) 🔹
[TODO](README.md#todo) 🔹
[Credits & Thanks](README.md#todo)

------------------------------------------------------------------------------------------------------------------------

### 🔹 Is this a mod menu?

No it's not! ___SecuroSurf___ simply blocks traffic from IPs you don't know, which is well within your rights,
especially considering how vulnerable and poorly maintained this (P2P!) game is. _SecuroSurf_ does not decrypt the
game's traffic, and it doesn't interact with the game in any way. It does not contain any reverse-engineered code, nor
any code that would violate the game developer's _EULA_. Furthermore, no decompilation or decryption was necessary to
create the program. The firewall simply blocks traffic by IP and simple heuristics.  

------------------------------------------------------------------------------------------------------------------------

### 🔹 Should I trust this?

You should never trust random code from the internet! However, in this case the code is open source and free for anyone
to review. Furthermore, the binaries are built by _GitHub_, whose parent company is _Microsoft_, which should give you
the peace of mind of running safe code.

------------------------------------------------------------------------------------------------------------------------

### 🔹 Is this effective?

Only if used correctly! That is, __all the players you are playing with must use it__. Otherwise, hackers can still
connect through the people that aren't running the firewall. How this works is illustrated by diagram below; if the
_Assistant_ and _Lester_ are running the firewall, but _Rickie_ is not, hackers can connect to _Rickie_, _Lester_ and
the _Assistant_ ___through___ _Rickie_:  

<p align="center"><img src="md_images/tunneling_diagram.png"></p>

------------------------------------------------------------------------------------------------------------------------

## User Manual

------------------------------------------------------------------------------------------------------------------------

### 🔹 Using the basic functionality of the firewall

The ___Normal___ mode will allow GTA Online traffic without interfering. This is the default.

The ___Solo___ mode, unsurprisingly, will immediately block all the active connections and take you to a protected empty
lobby.

The ___Lan___ mode, instead, will allow only people from your own _Local Area Network_ to connect to your lobbies. This
is useful if you want to play with just your family members, or roommates, etc. Remember that this is only effective if
also the other players are using _SecuroSurf_ with this exact mode enabled.

<p align="center"><img src="md_images/main_options.png"></p>

------------------------------------------------------------------------------------------------------------------------

### 🔹 Using the Dynamic session mode

This mode is the best for most of the players, because it works out of the box with no configuration necessary. Simply
create a _Solo_ lobby, then switch to _Normal_. Wait a few seconds, and invite your friends (while they are on _Normal_
as well). Once everybody has joined, everybody should enable the ___Dynamic___ mode. This will ensure that only the
people currently in the session will be allowed to stay in the session. In other words, no one else can join after
enabling the _Dynamic_ mode.

------------------------------------------------------------------------------------------------------------------------

### 🔹 Crew sessions

___Crews___ are 100%-customizable session configuration definitions. They are the safest mode, given that with them, the
firewall can be kept active all the time, thus offering more protection than the ___Dynamic___ session mode, which
instead requires the firewall to be turned off occasionally for your friends to join. ___Crews___ are meant for large
crews that are looking for a more definitive, stronger solution against frequent attacks from modders. You can find an
example of a crew definition [here](session.crew.Example Crew.json_EXAMPLE), and
[here](session_configuration_json_schema.md) the full documentation.

------------------------------------------------------------------------------------------------------------------------

#### 🔹 Local Crews

___Crews___ can be saved in simple _JSON_ files to keep alongside the program's executable. Each member of the crew
should have a copy of this file and use it to run the firewall. For example, you can use Google Docs to distribute the
file to all your crew members. The local crew file should be in the same folder as `SecuroSurf.exe`, and be named
`session.crew.name.json`, where "name" can be replaced with any name consisting in ASCII letters, numbers, and spaces
(e.g. `session.crew.My Amazing Crew.json`).

------------------------------------------------------------------------------------------------------------------------

#### 🔹 Remote Crews

TODO

------------------------------------------------------------------------------------------------------------------------

## FAQs

------------------------------------------------------------------------------------------------------------------------

### 🔹 How to update?

This project follows _SemVer_ versioning. Meaning that, __for example, if you own the firewall version 2.x you can
use your configuration files on any other 2.x, but not 3.x.__. However, you should try to keep your configuration files
updated, rather than blindly copying them from one directory to another. Important to know also, is that the presets
that ship with the firewall (_Normal, Solo, Lan, Dynamic_) are not meant to be user-configurable, so you should always
replace them with the respective newer versions.

------------------------------------------------------------------------------------------------------------------------

### 🔹 Why can't I connect sometimes (1)? 

It is completely normal to get "__Unable to connect to game session__" or "__Player is no longer in session__"
sometimes, even if everything looks fine. These errors happen when you could not complete the connection within the
allowed traffic limits, probably because other people or strangers were trying to connect at the same time. __Should
this happen, don't press _Continue_; open your friends list, and try again by clicking _Join Game___:

<p align="center"><img src="md_images/player_no_longer_in_session_fix.gif"></p>

------------------------------------------------------------------------------------------------------------------------

### 🔹 Why can't I connect sometimes (2)? 

Instead, if you see a lot of traffic being blocked by the firewall, it means that __you tried to connect to your
friends before the firewall could be updated on their end__ to allow you inside. Unfortunately your connection will be
permanently glitched when this happens, and the only way to fix it is to __switch to single player__ before trying
again. This problem will be solved in a future version, where the app will tell you explicitly when it's ok to join your
friends.

------------------------------------------------------------------------------------------------------------------------

## TODO

------------------------------------------------------------------------------------------------------------------------

## 🔹 SecuroSurf 2.0

- Set up GitHub actions to build releases automatically.
- The remote crews should stop updating themselves if the game is turned off.
- Add timestamps in the telemetry window. And maybe also the transfer rate, etc.
- Implement session lock and Dynamic mode.
- Complete README.

------------------------------------------------------------------------------------------------------------------------

## 🔹 SecuroSurf 2.+

- User setting for custom refresh rate (to apply when maximized -- minimized should reduce refresh rate already).
- Custom enable-telemetry setting (always enabled, disabled if minimized, always disabled).
- Notifications, e.g. play bell sound when people join or leave.
- Save settings to local files automatically, such as refresh rate, or window position.
- Add timestamps in the telemetry window. And maybe also the transfer rate, etc.
- Add "please wait N seconds before joining the crew" message.
- Determine whether it is necessary to implement the "mandatory packet detection" heuristics.
- Consider whether to introduce the "Firewall Cooldown" option.
- Implement manual kick of non-firewalled users. 

------------------------------------------------------------------------------------------------------------------------

## 🔹 SecuroSurf >2

- Switch to a better GUI toolkit. Possibly [libui](https://github.com/libui-ng/libui-ng). Any suggestions?
- Maybe port the project to Rust, for performance and for the updated WinDivert bindings.

------------------------------------------------------------------------------------------------------------------------

## Credits & Thanks

This program was inspired by [_Guardian_](https://gitlab.com/digitalarc/guardian) (and [_Guardian by
Speyedr_](https://gitlab.com/Speyedr/guardian-fastload-fix)). Many thanks to them, as they provided the initial input
and code I needed to start this project. _Guardian_ is still developed, and I try to contribute to it as well. Also
thanks to my friend Robert B. for helping me out with _Python_. 
