class UnableToRenderPage(Exception):
    msg = "Unable to render the page."


class UnableToLocateSearchBox(Exception):
    msg = "Unable to locate the search box."


class UnableToInteractWithSearchBox(Exception):
    msg = "Unable to interact with the search box."


class UnableToLoginException(Exception):
    msg = "Unable to login."

    def __init__(self, msg=None):
        if msg: self.msg = msg
