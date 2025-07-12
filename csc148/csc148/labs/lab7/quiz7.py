def semi_(obj):
    """
    >>> semi_([])
    True
    >>> semi_(5)
    True
    >>> semi_([[],['1','2'],['123']])
    True
    >>> semi_(['1',['2']])
    False
    """
    if isinstance(obj, int):
        return True
    else:
        typ = type(obj[0])
        for i in obj:
            if typ != type(i):






