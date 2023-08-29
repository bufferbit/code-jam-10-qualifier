from PIL import Image


def valid_input(
    image_size: tuple[int, int],
    tile_size: tuple[int, int],
    ordering: list[int],
) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    image_width, image_height = image_size
    width, height = tile_size

    # Check for proper image dimensions.
    if (image_width % width) | (image_height % height):
        return False

    # Check for valid input and correct ordering.
    if len(set(ordering)) ^ (image_width // width) * (image_height // height):
        return False

    return True


def rearrange_tiles(
    image_path: str,
    tile_size: tuple[int, int],
    ordering: list[int],
    out_path: str,
) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    width, height = tile_size

    with Image.open(image_path) as source_image:
        if not valid_input(source_image.size, tile_size, ordering):
            raise ValueError(
                "The tile size or ordering are not valid for the given image"
            )
        image_width, image_height = source_image.size
        tiles = [
            (x * width, y * height, (x + 1) * width, (y + 1) * height)
            for y in range(image_height // height)
            for x in range(image_width // width)
        ]
        images = (source_image.crop(tiles[i]) for i in ordering)
        with Image.new(source_image.mode, source_image.size) as image_out:
            for image, box in zip(images, tiles):
                image_out.paste(image, box)
                image.close()

            image_out.save(out_path, source_image.format)
