# 代码生成时间: 2025-09-20 07:44:56
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import re

# 定义配置项
define("port", default=8888, help="run on the given port", type=int)

# XSS过滤白名单
ALLOWED_TAGS = ['b', 'i', 'u', 'p', 'strong', 'em']
ALLOWED_ATTR = ['style']

def escape(text):
    """ 转义XSS特殊字符 """
    if text is None:
        return ''
    return (text
             .replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace("", "&quot;")
             .replace("'", "&apos;"))

def xss_filter(html):
    """ 简单的XSS过滤函数，移除不安全的标签和属性 """
    clean_html = ''
    inside_tag = False
    tag_name = ''
    attr_name = ''
    for char in html:
        if char == '<':
            inside_tag = True
            tag_name = ''
            attr_name = ''
        elif char == '>':
            inside_tag = False
            if tag_name.lower() in ALLOWED_TAGS:
                if attr_name:
                    # 允许的属性
                    if attr_name.lower() in ALLOWED_ATTR:
                        clean_html += f'<{tag_name} {attr_name}="{escape(re.sub(r"[^a-zA-Z0-9-_#]+", "", attr_value))}">\
'
                    else:
                        clean_html += f'<{tag_name}">
'
                else:
                    clean_html += f'<{tag_name}>\
'
        elif inside_tag:
            if char == ' ':
                # 开始属性部分
                attr_name = ''
                attr_value = ''
            elif char == '=':
                # 获取属性值
                attr_name = attr_name.strip()
                if attr_name.lower() in ALLOWED_ATTR:
                    attr_value = ''
            elif char in '"\'':
                # 属性值结束，检查是否允许
                attr_value = attr_value.strip()
                if attr_name.lower() in ALLOWED_ATTR:
                    if char == attr_value[0]:
                        clean_html += f' {attr_name}="{escape(re.sub(r"[^a-zA-Z0-9-_#]+", "", attr_value))}'
            else:
                if inside_tag and not attr_name:
                    tag_name += char
                elif attr_name:
                    attr_value += char
        else:
            if not inside_tag:
                clean_html += escape(char)
    return clean_html

class MainHandler(tornado.web.RequestHandler):
    """ 首页处理器 """
    def get(self):
        self.write("Welcome to the XSS Protection Server!")

    def post(self):
        user_input = self.get_argument('user_input')
        # 应用XSS过滤器
        safe_input = xss_filter(user_input)
        self.write(f"Filtered Input: {safe_input}")

def make_app():
    """ 创建Tornado应用 """
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print(f"Server is running on http://localhost:{options.port}")
    tornado.ioloop.IOLoop.current().start()