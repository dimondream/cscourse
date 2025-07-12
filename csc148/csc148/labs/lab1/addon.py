from typing import Any


def add_on(lst: list[tuple], new: Any) -> None:
    """Add new to the end of each tuple in lst.
    >>> things = [(), (1, 2), (1,)]
    >>> add_on(things, 99)
    >>> things
    [(99,), (1, 2, 99), (1, 99)]
    >>> things = []
    >>> add_on(things, 99)
    >>> things
    []
    >>> things = [(), (), ()]
    >>> add_on(things, 99)
    >>> things
    [(99,), (99,), (99,)]
    """
    '''
    for i in range(len(lst)):

        lst[i] = lst[i] + (new, )'''
    for item in lst:

        item = item + (new, )

if __name__ == '__main__':
    import doctest
    doctest.testmod()
