from lark import Transformer
from metovlogs import get_log

log = get_log(__name__)


class TreeToDict(Transformer):
    """
    Converts a raw Lark AST of Songs of Syx data to a Python dictionary. See also: [[1]]

    [1]: https://lark-parser.readthedocs.io/en/latest/json_tutorial.html#part-4-evaluating-the-tree
    """

    dict = dict

    def key_value_pair(self, s):
        key = str(s[0])
        value = s[1]
        return key, value

    array = list

    def string(self, s):
        return str(s[0])

    def integer(self, s):
        return int(s[0])
