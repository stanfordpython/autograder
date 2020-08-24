import sys
import io

class StatusMessage:
    """
    A class designed to create colorful messages to output during the
    execution of the autograder. This object is designed to be printed
    immediately.
    """

    def __init__(self, message, status=None):
        """
        Usage:
            print(StatusMessage("Passed all tests!", "success"))

        status -- The available statuses are
                'success'
                'fail'
                'warning'
                'info'
                'bold'
                'underline'
        """
        self._setup_color_support()

        self._plain_status = status
        self._plain_message = message
        self.message = self._get_color(message, status)


    def __str__(self):
        return self.message


    def __repr__(self):
        color_flag = self._color if self._colorized else 'NO_COLOR_SUPPORT'

        return (f'<StatusMessage: "{self._plain_message}", {self._plain_status}'
                f' / {color_flag}>')


    def _supports_color(self):
        """
        Returns True if the terminal supports color printing, False
        otherwise. Creds to Stack Overflow.
        """
        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (
            plat != 'win32' or 'ANSICON' in os.environ)

        # isatty is not always implemented, #6223.
        is_a_tty = (hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()) \
                   or isinstance(sys.stdout, io.IOBase)

        if not supported_platform or not is_a_tty:
            return False

        return True


    def _setup_color_support(self):
        """
        Sets up the class based on whether the terminal suppports
        colorized printing and which modules can be used to do that.
        """
        # color support?
        self._colorized = self._supports_color()

        # termcolor?
        try:
            from termcolor import colored
        except ModuleNotFoundError:
            # the module does not exist
            self._use_termcolor = False
        else:
            self._use_termcolor = True


    def _get_color(self, message, status):
        """
        Converts the status to a color hex
        """
        # set up color / status maps
        COLOR_HEX = {
            'header': '\033[95m',
            'blue': '\033[94m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'end': '\033[0m',
            'bold': '\033[1m',
            'underline': '\033[4m',
        }

        STATUS_COLORS = {
            'success': 'green',
            'fail': 'red',
            'warning': 'yellow',
            'info': 'blue',
            'bold': 'bold',
            'underline': 'underline',
        }

        # Neutral status option
        if status is None:
            return message

        # colorize the text
        if self._colorized:
            try:
                self._color = STATUS_COLORS[status]
            except KeyError:
                raise KeyError(f"'{status}' is not a valid status.") from None

            if self._use_termcolor:
                # termcolor... way more reliable than the hack below
                from termcolor import colored
                return colored(message, self._color)

            else:
                # colored ascii printing
                return COLOR_HEX[self._color] + message + COLOR_HEX['end']
        else:
            # plaintext
            return message

class HeaderMessage(StatusMessage):
    """
    Extends StatusMessage with a border around the message
    """

    def __init__(self, message, status=None):
        horiz_lines = max(len(message) + 10, 80)

        # new_message = [
        #     '┌' + '─' * horiz_lines + '┐',
        #     '│ {:^{spacing}} │'.format(message, spacing=horiz_lines-2),
        #     '└' + '─' * horiz_lines + '┘',
        # ]
        # new_message = '\n'.join(new_message)

        new_message = (
            "{:^{spacing}}\n".format(message, spacing=horiz_lines)
            + '–' * horiz_lines
        )

        super().__init__(new_message, status)

class SuperHeaderMessage(StatusMessage):
    """
    Extends StatusMessage with a thicc border around the message
    """

    def __init__(self, message, status=None):
        horiz_lines = max(len(message) + 10, 78)

        # new_message = [
        #     '╔' + '═' * horiz_lines + '╗',
        #     '║ {:^{spacing}} ║'.format(message, spacing=horiz_lines-2),
        #     '╚' + '═' * horiz_lines + '╝',
        # ]
        # new_message = '\n'.join(new_message)

        new_message = [
            '┌' + '─' * horiz_lines + '┐',
            '│ {:^{spacing}} │'.format(message, spacing=horiz_lines-2),
            '└' + '─' * horiz_lines + '┘',
        ]
        new_message = '\n'.join(new_message)

        super().__init__(new_message, status)
