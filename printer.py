colors = {
    'default': '\033[0m',
    'success': '\033[92m',
    'error': '\033[91m',
    'info': '\033[94m'
}


def printer(message, status):
    print(f'{colors.get(status)}{message}{colors.get("default")}')
