from videalize import settings


def merge_parts(main_parts, other_parts):
    main_parts, other_parts = main_parts.copy(), other_parts.copy()
    parts = []
    last_part_start, last_part_end = (None, None)
    while main_parts or other_parts:
        main = main_parts.pop(0) if main_parts else None
        other = other_parts.pop(0) if other_parts else None

        if not main:
            part_start, part_end = other['start'], other['end']
        elif not other:
            part_start, part_end = main['start'], main['end']
        elif main['start'] < other['start'] < other['end'] < main['end']:
            part_start, part_end = main['start'], main['end']
        elif other['start'] < main['start'] < main['end'] < other['end']:
            part_start, part_end = other['start'], other['end']
        elif main['end'] < other['start']:
            part_start, part_end = main['start'], main['end']
            other_parts.insert(0, other)
        elif other['end'] < main['start']:
            part_start, part_end = other['start'], other['end']
            main_parts.insert(0, main)
        else:
            part_start = min(main['start'], other['start'])
            part_end = max(main['end'], other['end'])

        if not last_part_start:
            last_part_start, last_part_end = part_start, part_end
        elif last_part_end + settings.SPEECH_CUT_THRESHOLD <= part_start:
            parts.append({'start': last_part_start, 'end': last_part_end})
            last_part_start, last_part_end = part_start, part_end
        elif last_part_end > part_start:
            last_part_end = max(part_end, last_part_end)

    if last_part_start and last_part_end:
        parts.append({'start': last_part_start, 'end': last_part_end})

    return parts
