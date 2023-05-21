from PIL import Image, ImageTk


def percent_value(percentage, value):
    return (percentage / 100) * value


def get_tk_image(file, size):
    if file is None:
        return ImageTk.PhotoImage(Image.new("RGBA", size, (0, 0, 0, 0)))
    with Image.open(file).resize(size) as image:
        return ImageTk.PhotoImage(image)
