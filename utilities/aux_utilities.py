import base64
import re


def audio_to_b64(audio):
      encodedStr = base64.b64encode(audio)
      audio_str = encodedStr.decode('ascii')
      return audio_str

def remove_double_whitespaces(phrase):
      return re.sub(' +', ' ', phrase)

def clean_end_vocals(phrase):
      regex = r"\s[aeiou]$"

      matches = re.search(regex,phrase)

      if matches:
            return phrase + " "
      else:
            return phrase