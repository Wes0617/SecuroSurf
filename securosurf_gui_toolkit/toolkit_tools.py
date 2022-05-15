from __future__ import annotations

from typing import Callable, Any, TypedDict

import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

ElementKey = str

EventKey = str

EventHandlerCallable = Callable[[ElementKey, EventKey], Any]

########################################################################################################################

class EventHandler(TypedDict):
    element_key: ElementKey
    event_type_key: EventKey
    callback: EventHandlerCallable

########################################################################################################################

class EventTarget:
    def __init__(self, window: tk.Window):
        self.__window = window
        self.__handlers: dict[str, list[EventHandler]] = {}

    def add_event_listener(self, element_key: ElementKey, event_key: EventKey, callback: EventHandlerCallable):
        self.__window[element_key].bind(event_key, event_key)

        element_event_key = element_key + event_key

        if self.__handlers.get(element_event_key) is None:
            self.__handlers[element_event_key] = []

        self.__handlers[element_event_key].append({
            "element_key": element_key,
            "event_type_key": event_key,
            "callback": callback,
        })

    def run_event_listeners(self, element_event_key: str):
        event_handlers: list[EventHandler] = self.__handlers.get(element_event_key, [])

        for eh in event_handlers:
            cb = eh["callback"]
            cb(eh["element_key"], eh["event_type_key"])
