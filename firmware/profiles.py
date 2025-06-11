from kmk.keys import KC


class BaseProfile:
    def __init__(self):
        pass

    def get_name(self):
        """Return the name of the profile. Keep it as short as possible."""
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_keymap(self):
        """Return a 2D array of the macropad keymap, with top right being KC.NO."""
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_encoder_map(self):
        """Return a tuple of 2 values, one for left and right encoder turns."""
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_color(self):
        """Return a tuple of HSV values (0-255) for the profile color."""
        raise NotImplementedError("This method should be overridden by subclasses")


class OnShapeProfile(BaseProfile):
    def get_name(self):
        return "OnShape"

    def get_keymap(self):
        return = [
            [KC.LSFT(KC.X),  KC.LSFT(KC.N2), KC.NO],          # Section view, Rear view
            [KC.LSFT(KC.N3), KC.LSFT(KC.N7), KC.LSFT(KC.N4)], # Left view, Iso view, Right view
            [KC.LSFT(KC.N5), KC.LSFT(KC.N1), KC.LSFT(KC.N6)], # Top view, Front view, Bottom view
            [KC.LSFT(KC.E),  KC.LSFT(KC.T),  KC.LSFT(KC.S)]   # Extrude, Make transparent , New sketch
        ]

    def get_encoder_map(self):
        return (KC.Z, KC.LSFT(KC.Z)) # Zoom out, Zoom in

    def get_color(self):
        return (85, 255, 255)


class SlackProfile(BaseProfile):
    def get_name(self):
        return "Slack"

    def get_keymap(self):
        return = [
            [KC.LCTL(KC.LSFT(KC.TAB)), KC.LCTL(KC.TAB),          KC.NO],                      # Prev workspace, Next workspace
            [KC.LCTL(KC.LSFT(KC.N)),   KC.LCTL(KC.U),            KC.LCTL(KC.LSFT(KC.ENTER))], # New canvas, Upload file, New Snippet
            [KC.LCTL(KC.LSFT(KC.N1)),  KC.LCTL(KC.LSFT(KC.N2)),  KC.LCTL(KC.LSFT(KC.N3))],    # Home, DMs, Activity
            [KC.LCTL(KC.K),            KC.LCTL(KC.F),            KC.LCTL(KC.LSFT(KC.SPACE))]  # Quick actions, Search, Huddle mute
        ]

    def get_encoder_map(self):
        return (KC.DOWN, KC.UP) # Scroll down, Scroll up

    def get_color(self):
        return (209, 164, 133)
