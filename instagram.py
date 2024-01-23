from instabot import Bot
from image import save_picture_path
from constants import INSTA_USERNAME, INSTA_PASSWORD
import glob
import os

class InstagramBot():
  def __init__(self):
    self.bot = Bot()
    self.image_path = save_picture_path()
    
  def login(self):
    try:
      cookie_del = glob.glob("config/*cookie.json")
      os.remove(cookie_del[0])
    except Exception as e:
      print(e)
      
    self.bot.login(username=INSTA_USERNAME, password=INSTA_PASSWORD)
    
  def generate_caption(self, quote):
    caption = f"Beautiful words by {quote['author']} ✨❤\n\n#quoteoftheday #wisdom #knowledge #wordsofwisdom #knowledgeispower #generalknowledge #wisdomquotes #motivationalquoteoftheday #innerwisdom #quoteoftheday #knowledgeable #dailywisdom #knowledgeispower #wisdomquote #wisdomoftheday #quote #quotes #enlightenment #meditation #positive #motivationalquotes #believe #mindset #motivationquotes #success #education #positivity #fact #motivational #motivation"
    return caption
    
  def upload_photo(self, caption):
    self.bot.upload_photo(photo=self.image_path, caption=caption)
    
  