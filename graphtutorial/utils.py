from enum import Enum
import configparser


class UserType(Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    MONITOR = "monitor"
    OPERLITE = "operatorlite"


class PermissionType(Enum):
    SYSTEM = "system"
    SP = "SP"
    Channel = "channel"
    Customer = "customer"


# Dictionary to assign UserType to PermissionType
permissions_mapping = {
    PermissionType.SYSTEM: [UserType.ADMIN, UserType.OPERATOR, UserType.MONITOR],
    PermissionType.SP: [UserType.ADMIN, UserType.OPERATOR, UserType.MONITOR],
    PermissionType.Channel: [UserType.ADMIN],
    PermissionType.Customer: [UserType.OPERATOR, UserType.OPERLITE, UserType.MONITOR]
}


class Roles(Enum):
    OVOCAdmin = "OVOCAdmin"
    OVOCOperator = "OVOCOperator"
    OVOCMonitor = "OVOCMonitor"
    OVOCOperatorLite = "OVOCOperatorLite"


class RoleId(Enum):
    OVL_ADMIN = "e2619b59-34a3-47bb-a1f2-84897fb3426b"
    OVL_OPERATOR = "0aa9c339-f85d-417c-8574-e16c33016700"
    OVL_MONITOR = "43f5bc50-a092-4e18-8e10-38b1fe63294b"
    OVL_OPERATORLITE = "64cde232-2402-452d-986a-1e28ba73863a"


class Utils:

    @staticmethod
    def get_config(config_file_path: str) -> dict:
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # Convert config sections to dictionaries
        settings = {}
        for section in config.sections():
            settings[section] = dict(config[section])
        return settings
