def get_transparent_color(color, factor):
    red, green, blue = color

    new_color = (
        int(red * factor),
        int(green * factor),
        int(blue * factor)
    )

    return new_color

def lerp_color(color, target, factor):
    red, green, blue = color
    target_red, target_green, target_blue = target

    new_color = (
        int(red + (target_red - red) * factor),
        int(green + (target_green - green) * factor),
        int(blue + (target_blue - blue) * factor)
    )

    return new_color

def get_scaled_size(size, scale):
    new_size = max(1, int(size * scale))

    return new_size