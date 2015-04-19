"""Config parser for AtamaTracker

See config/defaults.ini for all of available options and default values.
"""

import ConfigParser
import os.path


class Config(object):
    """Read-only config object for AtamaTracker.

    Public properties:
    section -- [str] Ini file's section name to be read
    """

    section = 'tracking'

    def __init__(self, parser):
        self.__parser = parser

    @property
    def time_step(self):
        """Time step in second.
        """
        return self.__parser.getfloat(self.section, 'time_step')

    @property
    def pattern_size(self):
        """Size of tracking pattern.
        """
        return self.__parser.getint(self.section, 'pattern_size')

    @property
    def find_buffer(self):
        """Buffer length to find the pattern in the next frame.
        """
        return self.__parser.getint(self.section, 'find_buffer')


class ConfigManager(object):
    """Create parsed ini data.

    Constants:
    DEFAULT_FILENAME -- [str] File name in which the default values are written
    FILENAME -- [str] File name of the config file

    Public properties:
    config -- Config object with parsed data.
    """

    DEFAULT_FILENAME = 'DEFAULTS.ini'
    FILENAME = 'config.ini'

    def __init__(self):
        self.parser = ConfigParser.SafeConfigParser()
        self.__read_defaults()

    @property
    def config(self):
        """Config object with parsed data.
        """
        return Config(self.parser)

    def load_config(self, source_path):
        """Read config file.

        source_path -- path to the source movie file.
        """
        config_path = self.__find_config_file(source_path)
        if config_path:
            self.parser.read(config_path)

    def __find_config_file(self, source_path):
        """Returns path of found local config file or None if not exists.
        """
        path = source_path

        # find config file in the parent directories upto 3 levels
        for _ in range(3):
            path = os.path.dirname(path)
            filepath = os.path.join(path, ConfigManager.FILENAME)
            if os.path.isfile(filepath):
                return filepath

        return None

    def __read_defaults(self):
        """Set default settings.
        """
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'config', ConfigManager.DEFAULT_FILENAME)
        self.parser.readfp(open(filepath))


# shared singleton instance  -> Python module is loaded only once.
manager = ConfigManager()
