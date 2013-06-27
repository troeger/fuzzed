def extend(target, source, *others, **options):
    all_sources = (source,) + others
    deep = options.get('deep', False)

    for other in all_sources:
        if not deep:
            # perform classical dict update, since nested dicts are not used
            target.update(other)
            continue

        for key, value in other.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                target[key] = extend({}, target[key], other[key], deep=True)
            else:
                target[key] = value

    return target
