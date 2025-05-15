class TabernaError(Exception):
    pass

class InsufficientGoldError(TabernaError):
    pass

class ItemNotFoundError(TabernaError):
    pass

class InvalidOptionError(TabernaError):
    pass

class AuthenticationError(TabernaError):
    pass

class ItemSoldOutError(TabernaError):
    pass 