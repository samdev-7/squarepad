import board
import neopixel
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.macros import Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306

from config import Config
from profiles import OnShapeProfile, SlackProfile

rgb_max_val = 32
screen_width = 128
screen_height = 32
profiles = [OnShapeProfile(), SlackProfile()]
config = Config(num_profiles=len(profiles))

keyboard = KMKKeyboard()
macros = Macros()
encoder_handler = EncoderHandler()
keyboard.modules = [encoder_handler, macros]

initial_color = profiles[config.get_profile_index()].get_color()
rgb = RGB(
    board.GP2,
    pixels=(neopixel.NeoPixel(board.GP2, 12, pixel_order="GRB"),),
    hue_default=initial_color[0],
    sat_default=initial_color[1],
    val_default=initial_color[2] if initial_color[2] < rgb_max_val else rgb_max_val,
    val_limit=rgb_max_val,
    val_step=1,
    animation_speed=10,
)
name = profiles[config.get_profile_index()].get_name()
text_entry = TextEntry(
    text=name,
    x=screen_width // 2,
    y=screen_height // 2,
    x_anchor="M",
    y_anchor="M",
)
display = Display(
    display=SSD1306(
        i2c=board.I2C,
    ),
    entries=[text_entry],
    width=screen_width,
    height=screen_height,
)
keyboard.extensions = [rgb, display]

keyboard.col_pins = (board.GP1, board.GP29, board.GP0)
keyboard.row_pins = (board.GP26, board.GP3, board.GP4)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

encoder_handler.pins = ((board.GP27, board.GP28, None),)


def enc_click_handler(keyboard):
    configuring = config.toggle_configuring()
    update(configuring=configuring)


def enc_left_handler(keyboard):
    if config.is_configuring():
        index = config.inc_profile_index(1)
        update(index)
    else:
        profile = profiles[config.get_profile_index()]
        profile.get_encoder_map()[0].on_press(keyboard)
        yield
        profile.get_encoder_map()[0].on_release(keyboard)


def enc_right_handler(keyboard):
    if config.is_configuring():
        index = config.inc_profile_index(-1)
        update(index)
    else:
        profile = profiles[config.get_profile_index()]
        profile.get_encoder_map()[1].on_press(keyboard)
        yield
        profile.get_encoder_map()[1].on_release(keyboard)


def update(profile_index=None, configuring=None):
    if profile_index is None:
        profile_index = config.get_profile_index()
    if configuring is None:
        configuring = config.is_configuring()

    if not (0 <= profile_index < len(profiles)):
        raise ValueError("Profile index out of bounds.")
    print(f"Profile index: {profile_index}")

    if configuring:
        rgb.animation_mode = AnimationModes.BREATHING
    else:
        rgb.animation_mode = AnimationModes.STATIC

    color = profiles[profile_index].get_color()
    rgb.hue = color[0]
    rgb.sat = color[1]
    rgb.val = color[2] if color[2] < rgb.val_limit else rgb.val_limit

    text_entry = TextEntry(
        text=name,
        x=screen_width // 2,
        y=screen_height // 2,
        x_anchor="M",
        y_anchor="M",
    )
    display.entries = [text_entry]

    new_keymap = profiles[profile_index].get_keymap()
    new_keymap[0][-1] = KC.MACRO(enc_click_handler)
    keyboard.keymap = new_keymap


ENC_CLICK = KC.MACRO(enc_click_handler)
ENC_LEFT = KC.MACRO(enc_left_handler)
ENC_RIGHT = KC.MACRO(enc_right_handler)

new_keymap = profiles[config.get_profile_index()].get_keymap()
new_keymap[0][-1] = KC.MACRO(enc_click_handler)
keyboard.keymap = new_keymap

encoder_handler.map = [((ENC_LEFT, ENC_RIGHT, KC.NO),)]

if __name__ == "__main__":
    keyboard.go()
