from configparser import ConfigParser

class Config:
    def __init__(self, path: str):
        config = ConfigParser()
        config.read(path)
        section = 'qianka'
        self.ID = self.get(config, 'card', section=section)
        self.USER = self.get(config, 'user', section=section)
        self.PASSWORD = self.get(config, 'passwd', section=section)
        self.NAME = self.get(config, 'name', section=section)
        self.YEAR = int(self.get(config, 'year', section=section))
        self.MONTH = int(self.get(config, 'month', section=section))
        self.DRIVER = self.get(config, 'driver', section=section)
        self.DRIVER_PATH = self.get(config, 'driverPath', section=section)
        self.THRESHOLD = int(self.get(config, 'threshold', section=section))

    def get(self, conf: ConfigParser, option : str, section : str = ''):
        if conf is None:
            raise RuntimeError('conf NONE')
        if section == '':
            raise RuntimeError(f'option {option} not found')
        else:
            if not conf.has_section(section):
                raise RuntimeError(f'section {section} not found')
            else:
                if not conf.has_option(section, option):
                    raise RuntimeError(f'option {option} not found')
                return conf[section][option]

    @property
    def str(self):
        return f'ID: {self.ID}\nUSER: {self.USER}\nPASSWORD: {self.PASSWORD}\nNAME: {self.NAME}\nYEAR: {self.YEAR}\nMONTH: {self.MONTH}'