""" модуль с контантами вынесен отдельно для избежания цикличности """
STATE_RANGE = ((0, "DRAFT"), (1, "PUBLISHED"), (2, "DENIED"), (3, "CANCELLED"))
STATE_BY_NAME = {v: k for k, v in STATE_RANGE}  # change key<->item


def get_state_by_name(name):
    """ возвращает код состояния по имени"""
    return STATE_BY_NAME[name]
