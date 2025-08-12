import board
import neopixel
import displayio
import adafruit_displayio_ssd1306
import i2cdisplaybus
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.macros import Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB, AnimationModes

from config import Config
from profiles import get_profiles
rgb_max_val = 64
screen_width = 128
screen_height = 32
profiles = get_profiles()
config = Config(num_profiles=len(profiles))

keyboard = KMKKeyboard()
# keyboard.debug_enabled = True  # Enable KMK debug logging
macros = Macros()
encoder_handler = EncoderHandler()
keyboard.modules = [encoder_handler, macros]

initial_color = profiles[config.get_profile_index()].get_color()
rgb = RGB(
    board.D8,
    pixels=(neopixel.NeoPixel(board.D8, 12, pixel_order="GRB"),),
    hue_default=initial_color[0],
    sat_default=initial_color[1],
    val_default=initial_color[2] if initial_color[2] < rgb_max_val else rgb_max_val,
    val_limit=rgb_max_val,
    val_step=1,
    animation_speed=10,
)
keyboard.extensions = [rgb]

displayio.release_displays()
display = adafruit_displayio_ssd1306.SSD1306(
    i2cdisplaybus.I2CDisplayBus(board.I2C(), device_address=0x3C),
    width=screen_width,
    height=screen_height
)
group = displayio.Group()

icon_bitmap = profiles[config.get_profile_index()].get_icon()
icon_palette = displayio.Palette(2)
icon_palette[0] = 0x000000  # Black
icon_palette[1] = 0xFFFFFF  # White

icon_sprite = displayio.TileGrid(
    icon_bitmap,
    pixel_shader=icon_palette,
    x=(screen_width // 2) - 16, 
    y=(screen_height // 2) - 16 
)
group.append(icon_sprite)

display.root_group = group

keyboard.col_pins = (board.D7, board.D3, board.D6)
keyboard.row_pins = (board.D0, board.D10, board.D9)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
encoder_handler.pins = ((board.D2, board.D1, None),)


def enc_click_handler(keyboard):
    configuring = config.toggle_configuring()
    update(configuring=configuring)


def enc_left_handler(keyboard):
    index = config.inc_profile_index(1)
    update(index)


def enc_right_handler(keyboard):
    index = config.inc_profile_index(-1)
    update(index)


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

    icon_bitmap = profiles[profile_index].get_icon()
    group.pop() 
    icon_palette = displayio.Palette(2)
    icon_palette[0] = 0x000000
    icon_palette[1] = 0xFFFFFF

    icon_sprite = displayio.TileGrid(
        icon_bitmap,
        pixel_shader=icon_palette,
        x=(screen_width // 2) - 16, 
        y=(screen_height // 2) - 16
    )
    group.append(icon_sprite)

    new_keymap = profiles[profile_index].get_keymap()
    new_keymap[0][2] = KC.MACRO(enc_click_handler)

    new_encoder_map = profiles[profile_index].get_encoder_map()
    if config.is_configuring():
        new_encoder_map = (ENC_LEFT, ENC_RIGHT)
    encoder_handler.map = [((new_encoder_map[0], new_encoder_map[1], KC.NO),)]

    keyboard.keymap = new_keymap


ENC_CLICK = KC.MACRO(enc_click_handler)
ENC_LEFT = KC.MACRO(enc_left_handler)
ENC_RIGHT = KC.MACRO(enc_right_handler)

new_keymap = profiles[config.get_profile_index()].get_keymap()
new_keymap[0][2] = KC.MACRO(enc_click_handler)
keyboard.keymap = new_keymap

new_encoder_map = profiles[config.get_profile_index()].get_encoder_map()
encoder_handler.map = [((new_encoder_map[0], new_encoder_map[1], KC.NO),)]

if __name__ == "__main__":
    keyboard.go()
