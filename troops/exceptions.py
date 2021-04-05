class InvalidTroopsToRecruitException(BaseException):
    pass


class BarracksLevelTooLowException(BaseException):
    pass


class NotEnoughFarmCapacityException(BaseException):
    pass


class NotEnoughResourcesToRecruitException(BaseException):
    pass


class InvalidTroopsToDemoteException(BaseException):
    pass


class TooManyTroopsToDemoteException(BaseException):
    pass


class InvalidTroopsToSendOffException(BaseException):
    pass


class AttackWithNoArmyException(BaseException):
    pass
