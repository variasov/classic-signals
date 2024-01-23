import inspect

from .signal import is_signal


def validate_signature_length(signature: inspect.Signature) -> bool:
    # TODO: Needed another, more stable way for detecting methods and functions
    #       inspect.ismethod works only on instances, not on class functions
    needed_len = 2 if 'self' in signature.parameters else 1

    params_len = len(signature.parameters)
    return params_len == needed_len


def get_last_param(signature: inspect.Signature):
    """
    We need to take last key in dict,
    but can't do:
    >>> dict.keys()[-1]
    """
    name = next(reversed(signature.parameters.keys()))
    return signature.parameters[name]


def get_signal_type(handler):
    signature = inspect.signature(handler)
    assert validate_signature_length(signature), \
        f'Reaction for event, must have only 1 parameter!'

    argument = get_last_param(signature)
    assert is_signal(argument.annotation)

    return argument.annotation
