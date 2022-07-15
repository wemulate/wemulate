from cement.utils.version import get_version as cement_get_version

VERSION = (1, 0, 3, "final", "0")


def get_version(version=VERSION):
    main: str = ".".join(str(x) for x in version[:3])
    if version[3] == "final":
        return main
    return main + str(version[4])
