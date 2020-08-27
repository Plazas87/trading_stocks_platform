#! usr/bin/env python3

from configparser import ConfigParser
import logging
from trade_app.config import DataBaseConnection


class BuildConfiguration:
    """Esta clase se encarga de leer el archivo de configuración general, las parametros leidos son almacenados como
    propiedades del objeto que sera luego instanciado en la clase controller"""
    def __init__(self, section='postgresql'):
        # logging.info("Built main configuration object")
        self.config_obj = self._config()

    @staticmethod
    def _config(filename='./trade_app/config/configpostgres.ini', specific_section=None):
        """Configura los parámetros para la conexión con la base de datos a través de la lectura de un
                archivo de configuración de extención .ini"""

        conf = ConfigParser()
        try:
            conf.read(filename)
            config_file_dict = {}
            tmp = {}
            for sect in conf.sections():
                params = conf.items(sect)
                for param in params:
                    tmp[param[0]] = param[1]

                config_file_dict[sect] = tmp
                tmp = {}

            return config_file_dict

        except Exception as e:
            print(e)


if __name__ == '__main__':
    c = BuildConfiguration(section=['postgresql', 'portfolio'])
    print(c)


