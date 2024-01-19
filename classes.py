
from functools import reduce
from import_modification import import_modification

def to_json(object): return object.to_json()
def link(x, y): return x | y
def parse_dict_options(dictionary):
    return Options(*[Option(_, dictionary[_]) for _ in dictionary])

class KeyEvent:
    def __init__(self, key_code = None, key_code_type = "key_code"):
        if key_code == None or key_code == all: key_code_type, key_code = "all", key_code_type
        self.value = {key_code_type: key_code}
    def to_json(self): return {_: self.value[_] for _ in self.value}

class Modifier:
    def __init__(self, modifier = 'any'): self.value = modifier
    def to_json(self): return {'modifier': self.value}

class Modifiers:
    def __init__(self, *modifiers):
        self.value = [_ if _.__class__ == Modifier else Modifier(_) for _ in modifiers]
    def to_json(self): return {'modifiers':
        list([_['modifier'] for _ in map(to_json, self.value)])}

class Option:
    def __init__(self, option, value): self.value = {option: value}
    def to_json(self): return {_: self.value[_] for _ in self.value}

class Options:
    def __init__(self, *options): self.value = options
    def to_json(self): return {'options': reduce(link, list(map(to_json, self.value)), {})}

class SimultaneousEvents:
    def __init__(self, *events):
        self.value = [_ if _.__class__ == KeyEvent else KeyEvent(_) for _ in events]
    def to_json(self): return {'simultaneous': list(map(to_json, self.value))}

class SimultaneousOptions:
    def __init__(self, options = None, to_after_key_up = None):
        if options == None: options = Options()
        if options.__class__ != Options: options = Options(options)
        self.value = {'options': options}
        if to_after_key_up != None: self.value['to_after_key_up'] = to_after_key_up
    def to_json(self): return {'simultaneous_options':
                                   self.value['options'].to_json()['options'] | \
                               ({'to_after_key_up': self.value['to_after_key_up'].to_json()}
                                if 'to_after_key_up' in self.value else {})}

class FromEvent:
    def __init__(self,
                 key_code = None,
                 mandatory_modifiers = None,
                 optional_modifiers = None,
                 simultaneous_events = None,
                 simultaneous_options = None):
        if simultaneous_options.__class__ == dict:
            simultaneous_options = parse_dict_options(simultaneous_options)
        if key_code.__class__ == str: key_code = KeyEvent(key_code)
        if mandatory_modifiers.__class__ == Modifier: mandatory_modifiers = Modifiers(mandatory_modifiers)
        if optional_modifiers .__class__ == Modifier: optional_modifiers  = Modifiers(optional_modifiers )
        if mandatory_modifiers.__class__ == str:
            mandatory_modifiers = Modifiers(Modifier(mandatory_modifiers))
        if optional_modifiers .__class__ == str:
            optional_modifiers  = Modifiers(Modifier(optional_modifiers))
        if mandatory_modifiers.__class__ == list:
            mandatory_modifiers = Modifiers(*mandatory_modifiers)
        if optional_modifiers .__class__ == list:
            optional_modifiers  = Modifiers(*optional_modifiers)
        if simultaneous_options .__class__ == Options: simultaneous_options = \
            SimultaneousOptions(simultaneous_options)
        if simultaneous_options .__class__ == Option : simultaneous_options = \
            SimultaneousOptions(simultaneous_options)
        self.value = {}
        if key_code == None and simultaneous_events == None: key_code = KeyCode()
        if key_code != None: self.value = key_code.to_json()
        modifiers = {}
        if mandatory_modifiers  != None: modifiers ['mandatory'] = mandatory_modifiers.to_json()['modifiers']
        if optional_modifiers   != None: modifiers ['optional']  = optional_modifiers .to_json()['modifiers']
        if modifiers            != {}:   self.value['modifiers']    = modifiers
        if simultaneous_events  != None: self.value |= simultaneous_events.to_json()
        if simultaneous_options != None: self.value |= simultaneous_options.to_json()
    def to_json(self): return {'from': self.value}

class ShellCommand:
    def __init__(self, command): self.value = command
    def to_json(self): return {'shell_command': self.value}

class Regex:
    def __init__(self, expression): self.expression = expression
    def to_json(self): return {'regex': self.expression}

class InputSource:
    def __init__(self, language = None, input_source = None, input_mode = None):
        if language    .__class__ == str: language     = Regex(language)
        if input_source.__class__ == str: input_source = Regex(input_source)
        if input_mode  .__class__ == str: input_mode   = Regex(input_mode)
        self.value = {}
        if language     != None: self.value['language'       ] = language
        if input_source != None: self.value['input_source_id'] = input_source
        if input_mode   != None: self.value['input_mode_id'  ] = input_mode
        if self.value == {}:     self.value['language'       ] = Regex("^en$")
    def to_json(self): return {'select_input_source':
        {_: self.value[_].to_json['regex'] for _ in self.value}}

class InputSources:
    def __init__(self, *input_sources): self.value = input_sources
    def to_json(self): return {'input_sources':
        list([_['select_input_source'] for _ in map(to_json, self.value)])}

class SetVariable:
    def __init__(self, name = "flag", value = 1): self.value = {'name': name, 'value': value}
    def to_json(self): return {'set_variable': self.value}

class MouseKey:
    def __init__(self,
                 x = None,
                 y = None,
                 vertical_wheel = None,
                 horizontal_wheel = None,
                 speed_multiplier = None):
        self.value = {}
        if x != None: self.value['x'] = x
        if y != None: self.value['y'] = y
        if vertical_wheel   != None: self.value['vertical_wheel'  ] = vertical_wheel
        if horizontal_wheel != None: self.value['horizontal_wheel'] = horizontal_wheel
        if speed_multiplier != None: self.value['speed_multiplier'] = speed_multiplier
    def to_json(self): return {'mouse_key': self.value}

class StickyModifier:
    def __init__(self, modifier = None, mode = 'toggle'):
        if modifier == None: modifier = Modifier()
        self.value = {modifier: mode}
    def to_json(self): return {'sticky_modifier':
        {_.to_json(): self.value[_] for _ in self.value}}

class CgEventDoubleClick:
    def __init__(self, button = 0): self.value = button
    def to_json(self): return {'cg_event_double_click': {'button': self.value}}

class SetMoveCursorPosition:
    def __init__(self, x = 0, y = 0, screen = None):
        self.value = {'x': x, 'y': y}
        if screen != None: self.value['screen'] = screen
    def to_json(self): return {'set_move_cursor_position': self.value}

class IokitPowerManagementSleepSystem:
    def __init__(self, delay = 500): self.value = delay
    def to_json(self): return {'iokit_power_management_sleep_system':
                                   {'delay_milliseconds': self.value}}

class SoftwareFunction:
    def __init__(self, *objects): self.value = objects
    def to_json(self): return {'software_function':
        reduce(link, list(map(to_json, self.value)), {})}

class ToEvent:
    def __init__(self,
                 key_code = None,
                 shell_command = None,
                 input_source = None,
                 set_variable = None,
                 mouse_key = None,
                 sticky_modifier = None,
                 software_function = None,
                 modifiers = None,
                 options = None):
        if options.__class__ == dict: options = parse_dict_options(options)
        if key_code.__class__ == str: key_code = KeyEvent(key_code)
        if software_function != None and software_function.__class__ != SoftwareFunction:
            software_function = SoftwareFunction(software_function)
        if modifiers.__class__ == Modifier: modifiers = Modifiers(modifiers)
        if modifiers.__class__ == list: modifiers = Modifiers(*modifiers)
        if key_code.__class__ == str: key_code = KeyCode(key_code)
        if modifiers.__class__ == str: modifiers = Modifiers(Modifier(modifiers))
        if options  .__class__ == Option: options   = Options  (options  )
        parameters = [key_code, shell_command, input_source, set_variable, mouse_key,
                      software_function, modifiers]
        self.value = [parameter for parameter in parameters if parameter != None]
        if self.value == []: self.value.append(SetVariable('flag', 1))
        self.options = options
    def to_json(self): return reduce(link, list(map(to_json, self.value)), {}) | \
        (self.options.to_json()['options'] if self.options != None else {})

class ToEvents:
    def __init__(self, *to_events): self.value = to_events
    def to_json(self): return list(map(to_json, self.value))

class DelayedActionToEvents:
    def __init__(self, to_if_invoked_events = None, to_if_canceled_events = None):
        if to_if_invoked_events.__class__ == list:
            to_if_invoked_events = ToEvents(*to_if_invoked_events)
        if to_if_canceled_events  .__class__ == list:
            to_if_canceled_events = ToEvents(*to_if_canceled_events)
        if to_if_invoked_events.__class__ == ToEvent:
            to_if_invoked_events = ToEvents(to_if_invoked_events)
        if to_if_canceled_events  .__class__ == ToEvent:
            to_if_canceled_events = ToEvents(to_if_canceled_events)
        self.value = {}
        if to_if_invoked_events  != None: self.value['to_if_invoked'  ] = to_if_invoked_events
        if to_if_canceled_events != None: self.value['to_if_canceled'] = to_if_canceled_events
    def to_json(self): return {_: self.value[_].to_json() for _ in self.value}

class FrontmostApplicationIf:
    def __init__(self, identifiers = None, paths = None):
        if identifiers.__class__ == str: identifiers = [identifiers]
        if paths      .__class__ == str: paths       = [paths      ]
        self.value = {}
        if identifiers != None: self.value["bundle_identifiers"] = identifiers
        if paths       != None: self.value["files_paths"]        = paths
    def to_json(self): return self.value | {"type": "frontmost_application_if"}

class FrontmostApplicationUnless:
    def __init__(self, identifiers = None, paths = None):
        if identifiers.__class__ == str: identifiers = [identifiers]
        if paths      .__class__ == str: paths       = [paths      ]
        self.value = {}
        if identifiers != None: self.value["bundle_identifiers"] = identifiers
        if paths       != None: self.value["files_paths"]        = paths
    def to_json(self): return self.value | {"type": "frontmost_application_unless"}

class DeviceIdentifier:
    def __init__(self,
                 vendor_id = None,
                 product_id = None,
                 location_id = None,
                 is_keyboard = None,
                 is_pointing_device = None,
                 is_touch_bar = None,
                 is_built_in_keyboard = None):
        self.value = {}
        if vendor_id            != None: self.value["vendor_id"           ] = vendor_id
        if product_id           != None: self.value["product_id"          ] = product_id
        if location_id          != None: self.value["location_id"         ] = location_id
        if is_keyboard          != None: self.value["is_keyboard"         ] = is_keyboard
        if is_pointing_device   != None: self.value["is_pointing_device"  ] = is_pointing_device
        if is_touch_bar         != None: self.value["is_touch_bar"        ] = is_touch_bar
        if is_built_in_keyboard != None: self.value["is_built_in_keyboard"] = is_built_in_keyboard
        if self.value == {}:             self.value["is_keyboard"         ] = True
    def to_json(self): return self.value

class DeviceIf:
    def __init__(self, identifiers = None):
        if identifiers.__class__ == DeviceIdentifier: identifiers = [identifiers]
        if identifiers == None: identifiers = []
        self.value = identifiers
    def to_json(self): return {"type": "device_if",
        "identifiers": list(map(to_json, modifiers))}

class DeviceUnless:
    def __init__(self, identifiers = None):
        if identifiers.__class__ == DeviceIdentifier: identifiers = [identifiers]
        if identifiers == None: identifiers = []
        self.value = identifiers
    def to_json(self): return {"type": "device_unless",
        "identifiers": list(map(to_json, modifiers))}

class DeviceExistsIf:
    def __init__(self, identifiers = None):
        if identifiers.__class__ == DeviceIdentifier: identifiers = [identifiers]
        if identifiers == None: identifiers = []
        self.value = identifiers
    def to_json(self): return {"type": "device_exists_if",
        "identifiers": list(map(to_json, modifiers))}

class DeviceExistsUnless:
    def __init__(self, identifiers = None):
        if identifiers.__class__ == DeviceIdentifier: identifiers = [identifiers]
        if identifiers == None: identifiers = []
        self.value = identifiers
    def to_json(self): return {"type": "device_exists_unless",
        "identifiers": list(map(to_json, modifiers))}

class KeyboardTypeIf:
    def __init__(self, keyboard_types = None):
        if keyboard_types.__class__ == str: keyboard_types = [keyboard_types]
        if keyboard_types == None: keyboard_types == []
        self.value = keyboard_types
    def to_json(self): return {"type": "keyboard_type_if",
        "keyboard_types": self.value}

class KeyboardTypeUnless:
    def __init__(self, keyboard_types = None):
        if keyboard_types.__class__ == str: keyboard_types = [keyboard_types]
        if keyboard_types == None: keyboard_types == []
        self.value = keyboard_types
    def to_json(self): return {"type": "keyboard_type_unless",
        "keyboard_types": self.value}

class InputSourceIf:
    def __init__(self, input_sources):
        if input_sources.__class__ == InputSource: input_sources = InputSources(input_sources)
        self.value = input_sources
    def to_json(self): return {"type": "input_source_if",
        "input_sources": self.value.to_json}

class InputSourceUnless:
    def __init__(self, input_sources):
        if input_sources.__class__ == InputSource: input_sources = InputSources(input_sources)
        self.value = input_sources
    def to_json(self): return {"type": "input_source_unless",
        "input_sources": self.value.to_json}

class VariableIf:
    def __init__(self, name = "flag", value = 1): self.value = {'name': name, 'value': value}
    def to_json(self): return self.value | {'type': "variable_if"}

class VariableUnless:
    def __init__(self, name = "flag", value = 1): self.value = {'name': name, 'value': value}
    def to_json(self): return self.value | {'type': "variable_unless"}

class EventChangedIf:
    def __init__(self, value = True): self.value = value
    def to_json(self): return {"type": "event_changed_if", "value": self.value}

class EventChangedUnless:
    def __init__(self, value = True): self.value = value
    def to_json(self): return {"type": "event_changed_unless", "value": self.value}

class Conditions:
    def __init__(self, *conditions): self.value = conditions
    def to_json(self): return list(map(to_json, self.value))

class Parameter:
    def __init__(self, parameter, value): self.value = {parameter: value}
    def to_json(self): return self.value

class Parameters:
    def __init__(self, *parameters): self.value = parameters
    def to_json(self): return reduce(link, list(map(to_json, self.value)), {})

class Manipulator:
    def __init__(self,
                 from_event = None,
                 to_events = None,
                 to_if_alone = None,
                 to_if_held_down = None,
                 to_after_key_up = None,
                 to_delayed_action = None,
                 conditions = None,
                 parameters = None):
        if to_events.__class__ == ToEvent: to_events = ToEvents(to_events)
        if to_if_alone.__class__ == ToEvent: to_if_alone = ToEvents(to_if_alone)
        if to_if_held_down.__class__ == ToEvent: to_if_held_down = ToEvents(to_if_held_down)
        if to_after_key_up.__class__ == ToEvent: to_after_key_up = ToEvents(to_after_key_up)
        if to_events.__class__ == list: to_events = ToEvents(*to_events)
        if to_if_alone.__class__ == list: to_if_alone = ToEvents(*to_if_alone)
        if to_if_held_down.__class__ == list: to_if_held_down = ToEvents(*to_if_held_down)
        if to_after_key_up.__class__ == list: to_after_key_up = ToEvents(*to_after_key_up)
        if conditions != None and conditions.__class__ != Conditions:
            conditions = Conditions(conditions)
        if parameters.__class__ == Parameter: parameters = Parameters(parameters)

        if from_event == None: from_event = FromEvent()
        self.value = from_event.to_json()
        if to_events          != None: self.value['to'] = to_events         .to_json()
        if to_if_alone       != None: self.value['to_if_alone'      ] = to_if_alone      .to_json()
        if to_if_held_down   != None: self.value['to_if_held_down'  ] = to_if_held_down  .to_json()
        if to_after_key_up   != None: self.value['to_after_key_up'  ] = to_after_key_up  .to_json()
        if to_delayed_action != None: self.value['to_delayed_action'] = to_delayed_action.to_json()
        if conditions        != None: self.value['conditions'       ] = conditions       .to_json()
        if parameters        != None: self.value['parameters'       ] = parameters       .to_json()
    def to_json(self): return {'type': 'basic'} | self.value

class MouseMotionToScrollManipulator:
    def __init__(self, from_event = None, conditions = None, momentum = None, speed = None):
        self.json = {'type': 'mouse_motion_to_scroll'}
        options = {}
        if momentum != None: options['momentum'] = momentum
        if speed    != None: options['speed'   ] = speed
        if options != {}:      self.json['options'   ] = options
        if from_event != None: self.json['from'      ] = from_event.to_json()
        if conditions != None: self.json['conditions'] = conditions.to_json()
    def to_json(self): return self.json

class Rule:
    def __init__(self, *manipulators, description = "No Description Available"):
        self.json = {'description': description, 'manipulators': list(map(to_json, manipulators))}
    def to_json(self): return self.json

class Modification:
    def __init__(self, *rules, title = "No Title Available"):
        self.json = {'title': title, 'rules': list(map(to_json, rules))}
    def __call__(self): import_modification(self)
    def to_json(self): return self.json
