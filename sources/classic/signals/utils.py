import inspect

from .signal import is_signal


def validate_signature_length(signature: inspect.Signature) -> bool:
    """
    Проверяет, что сигнатура функции имеет длину 1.
    :param signature: сигнатура функции
    """
    # TODO: Needed another, more stable way for detecting methods and functions
    #       inspect.ismethod works only on instances, not on class functions
    needed_len = 2 if 'self' in signature.parameters else 1

    params_len = len(signature.parameters)
    return params_len == needed_len


def get_last_param(signature: inspect.Signature):
    """
    Нам нужно взять последний ключ в словаре,
    но мы не можем сделать:
    >>> dict.keys()[-1]
    """
    name = next(reversed(signature.parameters.keys()))
    return signature.parameters[name]


def get_signal_type(handler):
    """
    Возвращает тип сигнала, на который реагирует функция.
    :param handler: функция реакции
    :return: тип сигнала
    """
    signature = inspect.signature(handler)
    assert validate_signature_length(signature), \
        f'Reaction for event, must have only 1 parameter!'

    argument = get_last_param(signature)
    assert is_signal(argument.annotation)

    return argument.annotation
