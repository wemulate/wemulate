VERSION = (2, 0, 4, "final", "0")


def get_version(version=VERSION):
    main: str = ".".join(str(x) for x in version[:3])
    if version[3] == "final":
        return main
    return main + str(version[4])
