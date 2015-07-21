# coding: utf-8
import re
import Queue


token_reg = '(\{\{\s*\w+\s*\}\})'  # 提取匹配变量语句块
key_reg = '\{\{\s*(\w+)\s*\}\}'  # 提取匹配变量语句块中的关键字

if_reg = '(\{%\s*if\s+\w+\s*%\}.*\{%\s*endif\s*%\})'  # 提取匹配if语句块
if_key_reg = '\{%\s*if\s+(\w+)\s*%\}.*\{%\s*endif\s*%\}'  # 提取匹配if语句块中的关键字
if_key_text = '\{%\s*if\s+\w+\s*%\}(.*)\{%\s*endif\s*%\}'  # 提取匹配if语句块中的正文

for_reg = '(\{%\s*for\s+\w+\s+in\s+\w+\s*%\}.*\{%\s*endfor\s*%\})'  # 提取匹配for语句块
for_first_key_reg = '\{%\s*for\s+(\w+)\s+in\s+\w+\s*%\}.*\{%\s*endfor\s*%\}'  # 提取匹配for语句块中的第一个关键字
for_second_key_reg = '\{%\s*for\s+\w+\s+in\s+(\w+)\s*%\}.*\{%\s*endfor\s*%\}'  # 提取匹配for语句块中的第二个关键字
for_key_text = '\{%\s*for\s+\w+\s+in\s+\w+\s*%\}(.*)\{%\s*endfor\s*%\}'  # 提取匹配for语句块中的正文

if_tag = '\{%\s*if\s+\w+\s*%\}|\{%\s*endif\s*%\}'  # 提取匹配的if开始或者结束的标志语句(如{% if name %}或{% endif %})
if_match = re.compile(r'{%\s*endif\s*%}')  # 匹配{% endif %}
for_tag = '\{%\s*for\s+\w+\s+in\s+\w+\s*%\}|\{%\s*endfor\s*%\}'  # 提取匹配的for开始或者结束的标志语句(如{% for i in name %}或{% endfor %})
for_match = re.compile(r'{%\s*endfor\s*%}')  # 匹配{% endfor %}




queue = Queue.LifoQueue(10)  # 最大嵌套深度


def render(template, **kwargs):
    '''渲染整个模板'''

    for_tem = render_for(template, **keys)
    if_tem = parse_if(for_tem, **keys)
    key_tem = render_key(if_tem, **keys)

    return key_tem


def render_for(template, **kwargs):
    '''
    渲染for语句块
    遇到endfor则从栈中取出对应的for
    '''

    text = template[:]
    start, end = 0, 0
    while True:
        token = re.search(for_tag, text)
        if token:
            if for_match.match(token.group(0)):
                tag = queue.get()
                text = parse_for(template[tag[1]:end+token.end()], **kwargs)
                template = template.replace(template[tag[1]:end+token.end()], text)

                end = len(text) - len(template[tag[1]:token.end()]) + tag[1]
                text = template[end:]
            else:
                start, end = map(lambda x, y: x + y, (end, end), token.span())
                queue.put((token.group(0), start, end))
                text = template[end:]
        else:
            break

    return template


def parse_for(template, **kwargs):
    '''
    解析for语句块
    因为if语句中可能会用到for中的变量，同时需要渲染if语句块
    '''

    tokens = _get_token_keys(template, for_reg)
    if not tokens:
        return ''
    for token in tokens:
        first_key = _get_words(token, for_first_key_reg)
        second_key = _get_words(token, for_second_key_reg)
        text = _get_words(token, for_key_text)

        if not kwargs[second_key]:
            template = template.replace(token, '')
            continue

        result_text = ''
        for i in kwargs[second_key]:
            kwargs.update({first_key: i})
            render_if_text = render_if(text, **kwargs)
            result_text += render_key(render_if_text, **kwargs)

        template = template.replace(token, result_text)

    return template


def render_if(template, **kwargs):
    '''渲染if语句块'''

    text = template[:]
    start, end = 0, 0
    while True:
        token = re.search(if_tag, text)
        if token:
            if if_match.match(token.group(0)):
                tag = queue.get()
                text = parse_if(template[tag[1]:end+token.end()], **kwargs)
                template = template.replace(template[tag[1]:end+token.end()], text)

                end = len(text) - len(template[tag[1]:token.end()]) + tag[1]
                text = template[end:]
            else:
                start, end = map(lambda x, y: x + y, (end, end), token.span())
                queue.put((token.group(0), start, end))
                text = template[end:]
        else:
            break

    return template


def parse_if(template, **kwargs):
    '''解析if语句块'''

    tokens = _get_token_keys(template, if_reg)
    for token in tokens:
        key = _get_words(token, if_key_reg)
        text = _get_words(token, if_key_text)
        if kwargs.get(key):
            template = template.replace(token, text)
        else:
            template = template.replace(token, '')

        # template = parse_if(template, **kwargs)  # 递归的渲染if

    return template


def render_key(template, **kwargs):
    '''渲染并解析模板中的变量'''

    tokens = _get_token_keys(template, token_reg)
    for token in tokens:
        key = _get_words(token, key_reg)
        try:
            template = template.replace(token, str(kwargs[key]))
        except KeyError:
            pass

    return template


def _get_token_keys(template, reg):
    '''获取匹配的语句块'''

    return re.findall(reg, template, re.S)


def _get_words(token, reg):
    '''获取匹配的语句块中的变量'''

    matchs = re.match(reg, token, re.S).groups(0)
    return matchs[0]


if __name__ == '__main__':
    template_key = '''<html><body>
                        <div>
                            <p>{{name }}</p>
                            <p>{{ city}}</p>
                        </div>
                    </body></html>'''

    template_if = '''<html><body>
                        <div>
                            {% if asdf %}
                            <p>{{ name }}</p>
                            {% endif %}
                            {%if city %}
                                <p>{{ city }}</p>
                                {% if time %}
                                    <p>{{ time }}</p>
                                {% endif%}
                            {%endif %}
                        </div>
                    </body></html>'''

    template_for = '''<html><body>
                        <div>
                            {%for i in num%}
                                <p>{{ i }}</p>
                                <p>{{ name }}</p>
                                    {% for j in num %}
                                        <p>{{ city }}</p>
                                    {%endfor %}
                                    {% for z in num %}
                                        {% for j in num %}
                                            <p>{{ time }}</p>
                                        {% endfor %}
                                    {%endfor %}
                            {% endfor %}
                        </div>
                    </body></html>'''

    template = '''<html><body>
                    <div>
                        {{ time2 }}
                        {%for i in num %}
                            <p>{{ i }}</p>
                            <p>{{ name }}</p>
                                {%for j in num %}
                                    <p>{{ city }}</p>
                                {% endfor %}
                                {% if i %}
                                    {%if time2 %}
                                        <p>{{ i }}</p>
                                        <p>{{ time2 }}</p>
                                    {% endif %}
                                    {% if time3%}
                                        <p>{{ time3 }}</p>
                                    {%endif %}
                                    <p>{{time }}</p>
                                {% endif %}
                        {% endfor %}
                    </div>
                </body></html>'''

    keys = {'name': 'leon', 'city': 'Beijing', 'time': '0030', 'time2': '1449', 'time3': '1517', 'num': list('asdf')}

    # print render_key(template_key, **keys)
    # print render_if(template_if, **keys)
    # print render_for(template_for, **keys)
    # print render(template, **keys)

    with open('to_render.html', 'r') as to_render:
        template = to_render.read()

    with open('result.html', 'w') as result:
        result.write(render(template, **keys))
