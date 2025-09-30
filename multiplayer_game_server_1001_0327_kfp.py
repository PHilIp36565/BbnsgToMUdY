# 代码生成时间: 2025-10-01 03:27:27
import tornado.ioloop
import tornado.web
import tornado.websocket
import json

"""
多人游戏网络服务器，使用Tornado框架实现。
本服务器允许多个客户端连接，并在他们之间进行通信。
"""

class GameWebSocket(tornado.websocket.WebSocketHandler):
    """
    游戏WebSocket处理类。
    负责处理客户端的连接、消息接收和发送。
    """
    clients = set()  # 存储所有连接的客户端

    def open(self):
        """
        当客户端打开连接时调用。
        """
        self.clients.add(self)
        print("客户端连接：", self)

    def on_close(self):
        """
        当客户端关闭连接时调用。
        """
        self.clients.remove(self)
        print("客户端断开连接：", self)

    def on_message(self, message):
        """
        当接收到客户端消息时调用。
        """
        try:
            data = json.loads(message)
            print("接收到消息：", data)
            # 将消息广播给所有客户端
            for client in self.clients:
                if client is not self:  # 不向发送者自身发送消息
                    client.write_message(message)
        except json.JSONDecodeError:
            print("无效的消息格式")

    def check_origin(self, origin):
        """
        允许所有跨域请求。
        """
        return True

class MainHandler(tornado.web.RequestHandler):
    """
    主页面请求处理类。
    """
    def get(self):
        """
        返回主页面。
        """
        self.write("<html><body>
"
                "<h1>多人游戏服务器</h1>
"
                "<script>
"
                "// WebSocket 客户端脚本
"
                "var socket = new WebSocket('ws://' + window.location.host + '/game');
"
                "socket.onmessage = function(event) {
"
                "    console.log('接收到消息：', event.data);
"
                "};
"
                "socket.onopen = function(event) {
"
                "    console.log('连接成功');
"
                "    socket.send('Hello Server');
"
                "};
"
                "</script>
"
                "</body></html>")

def make_app():
    """
    创建Tornado应用。
    """
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/game", GameWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # 监听8888端口
    print("服务器启动，监听8888端口...")
    tornado.ioloop.IOLoop.current().start()  # 启动事件循环