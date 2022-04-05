def reset_to_defaults():
    GameParameters.volume = GameParameters.default_volume
    GameParameters.brightness = GameParameters.default_brightness


def set_brightness(new_brightness):
    if GameParameters.max_brightness >= new_brightness >= 0:
        GameParameters.brightness = new_brightness
    else:
        print('Error: illegal brightness value')


def set_volume(new_volume):
    if GameParameters.max_volume >= new_volume >= 0:
        GameParameters.volume = new_volume
    else:
        print('Error: illegal brightness value')


class GameParameters:
    volume = 10
    brightness = 200
    max_brightness = 255
    max_volume = 100

    # Default settings:
    default_volume = 50
    default_brightness = 200


