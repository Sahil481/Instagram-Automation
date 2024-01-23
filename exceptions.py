class ImageAPIException(Exception):
  def __init__(self, message):            
    super().__init__(message)
            
    self.message = message
    
class QuoteAPIException(Exception):
  def __init__(self, message):
    super().__init__(message)
    
    self.message = message