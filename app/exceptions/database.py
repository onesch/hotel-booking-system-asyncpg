class GuestAlreadyExistsError(Exception):
    pass

class GuestNotFoundError(Exception):
    pass

class InvalidRoomTypeError(Exception):
    pass

class RoomTypeInUseError(Exception):
    pass

class RelatedEntityNotFoundError(Exception):
    pass

class RoomAlreadyBookedError(Exception):
    pass
