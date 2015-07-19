#coding: utf-8

# with open('base.html', 'r') as f:
#     base = f.read()
#
# with open('to_render.html', 'r') as f:
#     to_render = f.read()

# with open('result.html', 'w') as f:
#     result = f.read()
import re
from HTMLParser import HTMLParser
from bottle import SimpleTemplate


token_reg = '(\{\{ [a-zA-Z0-9_$]+ \}\})'
key_reg = '\{\{ ([a-zA-Z0-9_$]+) \}\}'

if_reg = '(\{% if [a-zA-Z0-9_$]+ %\}.*?\{% endif %\})'
if_key_reg = '\{% if ([a-zA-Z0-9_$]+) %\}.*\{% endif %\}'
if_key_text = '\{% if [a-zA-Z0-9_$]+ %\}(.*)\{% endif %\}'

for_reg = '(\{% for [a-zA-Z0-9_$]+ in [a-zA-Z0-9_$]+ %\}.*?\{% endfor %\})'
for_first_key_reg = '\{% for ([a-zA-Z0-9_$]+) in [a-zA-Z0-9_$]+ %\}.*\{% endfor %\}'
for_second_key_reg = '\{% for [a-zA-Z0-9_$]+ in ([a-zA-Z0-9_$]+) %\}.*\{% endfor %\}'
for_key_text = '\{% for [a-zA-Z0-9_$]+ in [a-zA-Z0-9_$]+ %\}(.*)\{% endfor %\}'


def render_for(template, num='', **kwargs):
    tokens = _get_token_keys(template, for_reg)
    for match in tokens:
        token = match.group(0)
        first_key = _get_words(token, for_first_key_reg)
        # second_key = _get_words(token, for_second_key_reg)
        text = _get_words(token, for_key_text)
        if not num:
            template = template.replace(token, '')
            continue

        temp = ''
        for i in num:
            kwargs.update({first_key: str(i)})
            temp += render_keys(text, **kwargs)
        template = template.replace(token, temp)

    return template


def render_if(template, **kwargs):
    tokens = _get_token_keys(template, if_reg)
    for match in tokens:
        token = match.group(0)
        key = _get_words(token, if_key_reg)
        text = _get_words(token, if_key_text)
        if kwargs.get(key, ''):
            text = render_keys(text, **kwargs)
            template = template.replace(token, text)
        else:
            template = template.replace(token, '')

    return template


def render_keys(template, **kwargs):
    tokens = _get_token_keys(template, token_reg)
    for match in tokens:
        token = match.group(0)
        key = _get_words(token, key_reg)
        try:
            template = template.replace(token, kwargs[key])
        except KeyError:
            print 'Error: Variable ' + key + ' is required.'
            raise

    return template


def _get_token_keys(template, reg):
    return re.finditer(reg, template, re.S)


def _get_words(token, reg):
    matchs = re.match(reg, token, re.S).groups(0)
    return matchs[0]


if __name__ == '__main__':
    template_key = '''<html><body>
                <div>
                    <p>{{ name }}</p>
                    <p>{{ city }}</p>
                </div>
            </body></html>'''
    template_if = '''<html><body>
                    <div>
                        {% if asdf %}
                        <p>{{ name }}</p>
                        {% endif %}
                        {% if city %}
                        <p>{{ city }}</p>
                        {% endif %}
                    </div>
                </body></html>'''
    template_for = '''<html><body>
                    <div>
                        {% for i in num %}
                        <p>{{ i }}</p>
                        <p>{{ name }}</p>
                        <p>{{ city }}</p>
                        {% endfor %}
                    </div>
                </body></html>'''
    keys = {'name': 'leon', 'city': 'Beijing'}

    # print render_keys(template_key, **keys)
    # print render_if(template_if, **keys)
    # print render_for(template_for, num=range(10), **keys)
    # print render_for(template_for, num=range(3), **keys)

from bottle import SimpleTemplate

tpl = SimpleTemplate('''Hello
        %for i in range(3):
            %if True:
             {{name}}
            %end
            {{ city }}
        %end
            ''')

# tpl = SimpleTemplate('''<div>
#          %if True:
#         <span>content</span>
#          %end
#         </div>''')
print tpl.render(name='World', city='Beijing')
