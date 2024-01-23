from Quote2Image import Convert
from image import generate_background_image, determine_text_color, apply_background_blur, save_picture_path
from quote import get_font, get_quote
from instagram import InstagramBot

def convert_image(quote, fg, bg, font, font_size = 36, font_size_author=28, width=1080, height=1080, watermark_text="", watermark_font_size=16, output_path="output/quote"):
    img=Convert(
        quote=quote["content"],
        author=quote["author"],
        fg=fg,
        bg=bg,
        font_size=font_size,
        font_type=font,
        font_size_author=font_size_author,
        width=width,
        height=height,
        watermark_text=watermark_text,
        watermark_font_size=watermark_font_size
    )
    img.save(output_path)
    return img

def generate_image(output_path):
    font = get_font()
    quote = get_quote()
    background_image = generate_background_image()
    fg = determine_text_color()
    apply_background_blur()
    
    image = convert_image(quote, fg, background_image, font, output_path=output_path)
    return quote

def generate_image_count(start=1, end=5):
    for i in range(start, end + 1):
        generate_image("output/quote" + str(i) + ".jpeg")
        
def generate_image_date_time():
    return generate_image(save_picture_path())
    
if __name__ == "__main__":
    quote = generate_image_date_time()
    bot = InstagramBot()
    bot.login()
    caption = bot.generate_caption(quote=quote)
    bot.upload_photo(caption)