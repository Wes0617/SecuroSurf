<h1>
    <img src="md_images/logo.png" align="left" height="108">
    SecuroSurf
</h1>

<p><b>A _GTA Online_ PC Firewall</b></p>

------------------------------------------------------------------------------------------------------------------------

**Jump to:** 🔹 [**Downloads**](https://github.com/Wes0617/SecuroSurf/releases) 🔹
[Quick Guide](#quick-guide) 🔹
[FAQs](#faqs) 🔹
[Credits & Thanks](#credits--thanks) 🔹
[Wiki](https://github.com/Wes0617/SecuroSurf/wiki)

------------------------------------------------------------------------------------------------------------------------

### 🔹 Is this a mod menu?

No it's not! ___SecuroSurf___ is a firewall software whose only duty is blocking traffic from IPs you don't know, which
is well within your rights, especially considering how insecure this game is. _SecuroSurf_ does not decrypt the game's
traffic, and it doesn't interact with the game in any way. It does not contain any reverse-engineered code, nor any code
that would violate the game developer's _EULA_. Furthermore, no decompilation or decryption was necessary to create the
program. If all this doesn't convince you how trivial this program is, consider that the whole thing can be created by
anyone with just [Windows Firewall](https://en.wikipedia.org/wiki/Windows_Firewall) (except it would be very cumbersome
to use). However, the usual warning applies because I am not a lawyer… I just want to play in peace: use this at your
own risk.

------------------------------------------------------------------------------------------------------------------------

### 🔹 Should I trust this?

You should never trust random code from the internet! However, in this case __the code is open source and free for
anyone to review__. Furthermore, the binaries are built via _GitHub_, whose parent company is _Microsoft_, which should
give you the peace of mind of running safe code.

<p align="center"><img src="md_images/trust.png"></p>

------------------------------------------------------------------------------------------------------------------------

### 🔹 Is this effective?

As of today (v1.60) it is, but only if used correctly! That is, __all the people you are playing with must use it__.
Otherwise, hackers can still connect through the people that aren't protected by the firewall. How this works
(tunneling) is illustrated by the diagram below; if the _Assistant_ and _Lester_ are running the firewall, but _Rickie_
is not, hackers can connect to _Rickie_, _Lester_ and the _Assistant_ _through_ _Rickie_:  

<p align="center"><img src="md_images/tunneling_diagram.png"></p>

Will the firewall continue to work in future? It most probably will, because changing the game's network architecture
now, at the end of its life, would be a huge waste of money. GTA Online will continue to be a P2P game, unfortunately.

------------------------------------------------------------------------------------------------------------------------

## Quick Guide

___SecuroSurf___ is easy to use! The most important functionality is just one click away.

------------------------------------------------------------------------------------------------------------------------

### 🔹 Download and run the app

___SecuroSurf___ is a portable application that requires zero configuration for most users. All you need to do is to
download the [latest release](https://github.com/Wes0617/SecuroSurf/releases) (only win10/x64 is currently
supported), unzip it somewhere, and then run `SecuroSurf.exe` as _Administrator_ (Right-click on the executable and
press _Run as administrator_). If you use a _VPN_ for _GTA_, make sure _SecuroSurf_ connects through it as well.

------------------------------------------------------------------------------------------------------------------------

### 🔹 Using the basic functionality of the firewall

The ___Normal___ mode will allow GTA Online traffic without interfering. This is the default at the startup.

The ___Solo___ mode, unsurprisingly, will immediately block all the traffic and take you to a protected empty lobby.

The ___Lan___ mode, instead, will allow only people from your own _Local Area Network_ to connect to your lobbies. This
is useful if you want to play with just your family members, or roommates, etc. Remember that this is only effective if
also the other players are using _SecuroSurf_ with this exact mode enabled.

<p align="center"><img src="md_images/main_options.png"></p>

------------------------------------------------------------------------------------------------------------------------

### 🔹 Using Dynamic sessions (best for most users)

This mode is the best for most players, because it works right out of the box with no configuration necessary. Simply
create a _Solo_ lobby, then switch to _Normal_. Wait a few seconds, and invite your friends (while they are on _Normal_
as well). Once everybody has joined, everybody should enable the ___Dynamic___ mode. This will ensure that only the
people currently in the session will be allowed to stay in the session. In other words, no one else can join after
enabling the _Dynamic_ mode. **Note: this mode is currently not available, but it will be when the version 2.0 of the
app is released.**

------------------------------------------------------------------------------------------------------------------------

### 🔹 Crew sessions (for advanced users and groups)

___Crews___ are totally customizable session configurations. They are the safest mode, given that with them, the
firewall can be kept active all the time, thus offering more protection than the _Dynamic_ session mode, which instead
requires the firewall to be turned off occasionally for your friends to join. Crew sessions are meant for established
groups of people that are looking for a more definitive, stronger solution against frequent attacks from modders. You
can find an example of a crew definition [here](configs/session.crew.Example%20Crew.json_EXAMPLE), and
[here](configs/session_configuration_json_schema.md) the full documentation.

__[Local Crews]__ A _crew_ can be defined with a simple _JSON_ file. Then, each member of the crew should have an
identical copy of this file and use it to run the firewall. For example, you can use _Google Drive_ to distribute the
file to all your crew members. The file should be placed in the "configs" folder, and be named `session.crew.name.json`,
where "name" can be replaced with any name consisting in ASCII letters, numbers, and spaces (e.g.
`session.crew.My Amazing Crew.json`).

__[Remote Crews]__ Sharing configuration files with your friends can be annoying, so it is possible to host the crew
definitions on the web, and have _SecuroSurf_ fetch them automatically. If your crew provided you with an URL to use
with _SecuroSurf_, you must create a `session.crews-remote.json` file containing a _JSON_ object whose keys are the crew
names, and the values are the respective URLs you've been given. See an example [here](
configs/session.crews-remote.json_EXAMPLE). The format used for the remote configurations is the same as the local
crews, except the data is obfuscated. If you are the leader of a crew, have a look at the source code to learn how to
implement this, or ask for help in the [discussions](https://github.com/Wes0617/SecuroSurf/discussions) section. 

------------------------------------------------------------------------------------------------------------------------

## FAQs

Frequently Asked Questions.

------------------------------------------------------------------------------------------------------------------------

### 🔹 How to update?

This project follows _SemVer_ versioning. Meaning that, __for example, if you own the firewall version 2.x you can
use your configuration files on any other 2.x, but not 3.x.__. However, you should try to keep your configuration files
updated, rather than blindly copying them from one directory to another. Important to know also, is that the presets
that ship with the firewall (_Normal, Solo, Lan, Dynamic_) are not meant to be user-configurable, so you should always
replace them with the respective newer versions.

------------------------------------------------------------------------------------------------------------------------

### 🔹 Why can't I connect sometimes? 

It is completely normal to get "__Unable to connect to game session__" or "__Player is no longer in session__"
sometimes, even if everything looks fine. These errors happen when you could not complete the connection within the
allowed traffic limits, probably because other people or strangers were trying to connect at the same time. __Should
this happen, don't press _Continue_; open your friends list, and try again by clicking _Join Game___:

<p align="center"><img src="md_images/player_no_longer_in_session_fix.gif"></p>

------------------------------------------------------------------------------------------------------------------------

## Credits & Thanks

This program is inspired by [_Guardian_](https://gitlab.com/digitalarc/guardian), and [_Guardian by Speyedr_](
https://gitlab.com/Speyedr/guardian-fastload-fix). Many thanks to them, as they provided the initial input and info
necessary to start this project. In particular to [_Speyedr_](https://github.com/Speyedr), which figured out the first
proof of concept. Also, thanks to my friend Robert B. for helping me out with _Python_, and many thanks to the guinea
pigs (B. and B.) that helped to test this application.
