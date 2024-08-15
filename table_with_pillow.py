from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance
import textwrap

font = ImageFont.truetype(font="fonts/Roboto-Medium.ttf", size=10, layout_engine=ImageFont.Layout.BASIC)
warning_icon = Image.open("fonts/icons/warning.png").resize((10, 10))
print(warning_icon.size)
release_icon = Image.open("fonts/icons/releases.png").resize((10, 10))

def add_corners(im, rad): 
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def join_images(*images):
    # width,height = images[0].size
    widths, heights = zip(*(i.size for i in images))
    # print(widths, heights)
    # widths, heights = zip(*(i.size for i in images.values()))
    total_width = max(widths)
    max_height = sum(heights)
    new_image = Image.new('RGBA', (total_width, max_height),color=(225,0,0,255))
    x_offset = 0
    for i, image in enumerate(images):
        # print(heights[i])
        new_image.paste(image, (0, x_offset))
        x_offset = x_offset + heights[i]
    # new_image.show()
    return new_image
    # return new_image


def check_for_recon(data: list):
    pass


def join_image(image1, image2):
    width1, height1 = image1.size
    width2, height2 = image2.size

    # Create a new image with the combined width and the height of the tallest image
    # new_width = width1 + width2
    # new_height = max(height1, height2)
    # new_image = Image.new("RGB", (new_width, new_height))
    new_width = max(width1, width2)
    new_height = height1 + height2
    new_image = Image.new("RGB", (new_width, new_height))

    # Paste the two images onto the new image
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (0, height1))
    new_image.show()
    # new_image.paste(imag3, (width1+width2, 0))

# def generate_table_image(data: list):



def create_comment_image(lines, colors, width: int,notice):
    list_image = []
    if len(lines) != len(colors) or len(lines) != len(notice):
        raise ValueError("lines and colors must have the same length")
    text_wraps = []
    for no,line in enumerate(lines):
        image = Image.new("RGB", (width, 15), "white")
        draw = ImageDraw.Draw(im=image)
        text_wrap = textwrap.TextWrapper(width=100, drop_whitespace=True).wrap(line)
        for text_wrap_line in text_wrap:
            if notice[no]:  # If notice is True
                draw.bitmap((0, 0), warning_icon, fill='red')
            else:
                draw.bitmap((0, 0), release_icon, fill='green')
            # draw.bitmap((0, 0), warning_icon,fill='red')
            draw.text((20, 0), text_wrap_line, fill="black",spacing=5,embedded_color=True, align="center", font=font)
        list_image.append(image)
    new_image = join_images(*list_image)
    return new_image
    # image.show()


def generate_image_chunk1(data: list = ('Not Found', 'Not Found', 'Not Found'),
                          text_colors: list = ("black", "black", "black"),
                          background_colors: list = ((255, 244, 225), (255, 244, 225), (255, 244, 225)),
                          is_title: bool = False):
    if len(data) != 3 or len(text_colors) != 3 or len(background_colors) != 3:
        raise ValueError("Data must contain 3 elements")
    title = Image.new("RGBA", (180, 15), background_colors[0])
    a_image = Image.new("RGBA", (120, 15), background_colors[1])
    b_image = Image.new("RGBA", (120, 15), background_colors[2])
    title_draw = ImageDraw.Draw(im=title)
    a_draw = ImageDraw.Draw(im=a_image)
    b_draw = ImageDraw.Draw(im=b_image)
    title_text_wrap = textwrap.TextWrapper(width=100, drop_whitespace=True, max_lines=1).wrap(text=data[0])
    if len(title_text_wrap) == 0:
        title_text_wrap.append("Not Found")
    a_text_wrap = textwrap.TextWrapper(width=100, drop_whitespace=True, max_lines=1).wrap(text=data[1])
    if len(a_text_wrap) == 0:
        a_text_wrap.append("Not Found")
    b_text_wrap = textwrap.TextWrapper(width=100, drop_whitespace=True, max_lines=1).wrap(text=data[2])
    if len(b_text_wrap) == 0:
        b_text_wrap.append("Not Found")
    left, top, right, bottom = title_draw.textbbox((10, 0), title_text_wrap[0].strip(), align="center", font=font)
    left1, top1, right1, bottom1 = a_draw.textbbox((10, 0), a_text_wrap[0].strip(), align="center", font=font)
    left2, top2, right2, bottom2 = b_draw.textbbox((10, 0), b_text_wrap[0].strip(), align="center", font=font)
    title_draw.text((left, top - 1), title_text_wrap[0], fill=text_colors[0], align="center", font=font)
    a_draw.text((left1, top1 - 1), a_text_wrap[0], fill=text_colors[1], align="center", font=font)
    b_draw.text((left2, top2 - 1), b_text_wrap[0], fill=text_colors[2], align="center", font=font)
    title = ImageOps.expand(title, border=(1, 1, 0, 0), fill='black')
    a_image = ImageOps.expand(a_image, border=1, fill='black')
    b_image = ImageOps.expand(b_image, border=1, fill='black')
    width1, height1 = title.size
    width2, height2 = a_image.size
    width3, height3 = b_image.size
    new_width = width1 + width2 + width3
    new_height = max(height1, height2, height3)
    new_image = Image.new("RGBA", (new_width, new_height))
    new_image.paste(title, (0, 0))
    new_image.paste(a_image, (width1, 0))
    new_image.paste(b_image, (width1 + width2, 0))
    return new_image


def generate_image_chunk_old(a: str, b: str, title: str, background_a: str = (255, 244, 225),
                         background_b: str = (255, 244, 225), background_title=(255, 244, 225),
                         font_color_a: str = "black", font_color_b: str = "black", font_color_title: str = "black",
                         is_title: bool = False):
    image = Image.new("RGB", (140, 15), background_title)
    imag2 = Image.new("RGB", (140, 15), background_a)
    imag3 = Image.new("RGB", (140, 15), background_b)
    draw = ImageDraw.Draw(im=image)
    draw2 = ImageDraw.Draw(im=imag2)
    draw3 = ImageDraw.Draw(im=imag3)
    text_color = (255, 255, 255)  # white
    tw = textwrap.TextWrapper(width=100, drop_whitespace=True, max_lines=1).wrap(text=title)
    tw2 = textwrap.TextWrapper(width=100, drop_whitespace=True, max_lines=1).wrap(text=a)
    tw3 = textwrap.TextWrapper(width=100, drop_whitespace=True, max_lines=1).wrap(text=b)
    left, top, right, bottom = draw.textbbox((10, 0), tw[0].strip(), align="center", font=font)
    left1, top1, right1, bottom1 = draw2.textbbox((10, 0), tw2[0].strip(), align="center", font=font)
    left2, top2, right2, bottom2 = draw3.textbbox((10, 0), tw3[0].strip(), align="center", font=font,anchor='mm')

    # draw.rectangle((left-2, top-2, right+2, bottom+2), fill=(255, 255, 255), width=1,outline=a_color)
    draw.text((left, top - 1), tw[0], fill=font_color_title, align="center", font=font)
    # image.show()

    # draw.rectangle((left-2, top-2, right+2, bottom+2), fill=(255, 255, 255), width=1,outline=a_color)

    draw2.text((left1, top1 - 1), tw2[0], fill=font_color_a, align="center", font=font)
    draw3.text((left2, top2 - 1), tw3[0], fill=font_color_b, align="center", font=font)
    imag2 = ImageOps.expand(imag2, border=(1, 1, 0, 0), fill='black')
    image = ImageOps.expand(image, border=1, fill='black')
    imag3 = ImageOps.expand(imag3, border=1, fill='black')
    # imag2.show()
    width1, height1 = image.size
    width2, height2 = imag2.size
    width3, height3 = imag3.size

    # Create a new image with the combined width and the height of the tallest image
    new_width = width1 + width2 + width3
    new_height = max(height1, height2, height3)
    new_image = Image.new("RGB", (new_width, new_height))

    # Paste the two images onto the new image
    new_image.paste(image, (0, 0))
    new_image.paste(imag2, (width1, 0))
    new_image.paste(imag3, (width1 + width2, 0))
    return new_image
    # new_image.show()


def main():
    lines = ['Increase in Cost of Employees', 'Benfits', 'Increase in Cost of Employees', 'Benfits',]
    colors = ['black', 'black', 'black', 'black']
    # image_multi_line = generate_image_chunk(lines, colors)
    image1 = generate_image_chunk1(data=["Transaction Details", "Jul", "June"],
                                   background_colors=["black", "black", "black"],
                                   text_colors=["white", "white", "white"], is_title=True)
    image2 = generate_image_chunk1(data=["Total Employee Cost", "$2555.0", "$3543.00"],
                                   background_colors=["white", "aquamarine", "white"],
                                   text_colors=["black", "black", "black"], is_title=False)
    image3 = generate_image_chunk1(data=["Count of Employees", "24", "36"],
                                   background_colors=["white", "aquamarine", "white"],
                                   text_colors=["black", "black", "black"], is_title=False)
    image4 = generate_image_chunk1(data=["Total Employee Addition", "0", "12"],
                                   background_colors=["white", "aquamarine", "white"],
                                   text_colors=["black", "black", "black"], is_title=False)
    image5 = generate_image_chunk1(data=["Total Employee Subtraction ", "0", "0"],
                                   background_colors=["white", "aquamarine", "white"],
                                   text_colors=["black", "black", "black"], is_title=False)
    table_image = join_images(image1, image2, image3, image4, image5)
    size_of_table_width, size_of_table_height = table_image.size
    print(size_of_table_height, size_of_table_width)
    notice=[True, False, True, False]
    comment_image = create_comment_image(lines, colors, width=size_of_table_width,notice=notice)

    final_image = join_images(comment_image, table_image)
    final_image_width, final_image_height = final_image.size
    r, l = 20, 20
    b, t = 20, 20
    new_width = final_image_width + r + l
    new_height = final_image_height + b + t

    result = Image.new(final_image.mode, (new_width, new_height), ( 255, 255, 255 ))
    result.paste(final_image, (l, t))
    # Enhancing Image

    result = result.filter(ImageFilter.SHARPEN)
    # Adjust brightness
    result = ImageEnhance.Color(result).enhance(3.0)
    result = ImageEnhance.Brightness(result).enhance(1.5)
    # result = ImageEnhance.Sharpness(result).enhance(1.2)
    result = add_corners(result, 10)
    # line_image = Image.new("RGB", (new_width, 5), "black")
    # draw_line = ImageDraw.Draw(im=line_image)
    # draw_line.line((0, 0,0, 0), fill="black", width=5)
    # result = result.resize((1080, 720), resample=Image.Resampling.BOX)
    result.show()
    # result.save('output.png', quality=95, format="PNG",subsampling=5, dpi=(1920, 1200))
    # result.show()
    # print(final_image_width, final_image_height)

    # final_image.show()
    # image_multi_line.show()
    # generate_image_chunk("123", "345", "Hello", "Blue", "Yellow")


if __name__ == '__main__':
    main()
