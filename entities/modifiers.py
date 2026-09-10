def get_transparent_color(color, factor):
    red, green, blue = color

    new_color = (
        int(red * factor),
        int(green * factor),
        int(blue * factor)
    )

    return new_color

def get_scaled_size(size, scale):
    new_size = max(1, int(size * scale))

    return new_size