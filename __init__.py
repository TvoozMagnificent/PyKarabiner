
from constants import *
from classes import *

mod = {
    one: one,
    two: three,
    e: four,
    w: two,
    tab: z,
    z: comma,
    x: period,
}

manipulators = []

for entry in mod:
    from_key, to_key = entry, mod[entry]

    from_event = FromEvent(
        from_key
    )

    to_events = ToEvents(
        ToEvent(
            to_key
        )
    )

    manipulators.append(
        Manipulator(from_event, to_events)
    )

result = Modification(Rule(*manipulators, description = f"Gradescope Mapping"), title = f"Gradescope Mapping")

result()
