class BufferFalloffError(IndexError):
    """
    Error that is raised when someone tries to read an element from a buffer
    that doesn't exist.
    """
    pass


class RedirectStdin:
    """
    Serves as a dummy stdin object that you can write to and read from. 
    This object will then output from its self-stored data.
    """

    def __init__(self, to_output=None):
        # Build the list of things to output
        self.to_output = []
        if to_output:
            # Write initial buffer
            for e in to_output:
                self.write(e)

        # Initialize location to output from
        self.num_written = 0


    def write(self, s):
        """
        Writes s to self.to_output
        """
        # Kind of gross, but we need to make sure that it's readable
        if not isinstance(s, str):
            raise ValueError(
                f"Can't write a {type(s)} object to stdin (expected a string)."
            )

        self.to_output.append(s)


    def reset_buffer(self):
        """
        Resets the position from which the buffer is being read.
        """
        self.num_written = 0


    def clear(self):
        """
        Clears the buffer.
        """
        self.to_output = []
        self.num_written = 0


    def readline(self):
        """Returns the next element to_output"""
        if self.num_written >= len(self.to_output):
            raise BufferFalloffError(
                f"Cannot read element {self.num_written}. Has it been written?"
            )

        # Capture the element to output and return it
        out = self.to_output[self.num_written]
        self.num_written += 1

        # Print out to stdout for formatting
        print(out)
        
        return out