import re

tokenRegx = '(\${[$a-zA-Z0-9_-]+})'
keyRegx = '\${([$a-zA-Z0-9_-]+)}{1}'


def parse(vars = {}, template = ''):
  """
  Inserts variables into template and returns template
  @return String
  """
  words = _get_words(template)

  for match in words:
    token = match.group(0)
    key   = _get_token_key(token)

    try:
      var = str(vars[key])
      template = template.replace(token, var)
    except KeyError:
      print 'Error: Variable ' + key + ' is required.'
      raise

  return template

def _get_words(template):
  """
  Splits the template on spaces and returns a dictionary of index:words
  @return Iter
  """
  return re.finditer(tokenRegx, template)

def _get_token_key(token):
  """
  Finds key within token string in template
  @return String
  """
  matches = re.match(keyRegx, token).groups()

  return matches[0]


if __name__ == '__main__':
    vars = {'name': 'Darrell', 'age': 26, 'occupation': 'javascript ninja'}
    template = 'Hi my name is ${name}! I am ${age} years old and I consider myself to be a ${occupation}.'

    sentence = parse(vars, template)
    print sentence
