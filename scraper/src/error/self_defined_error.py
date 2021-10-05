class SelfDefinedError(Exception):
    pass


class UnexpectedOutcomeError(SelfDefinedError):
    """
        Raise this error when the output is valid but may be problematic, ie.,
        job scrapper found no jobs with given conditions, this is possible
        but may also due to the changes in the id or class name of some elements which lead to this outcome
    """
    pass
