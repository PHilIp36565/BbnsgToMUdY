# 代码生成时间: 2025-10-09 21:42:56
import os
import hashlib
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

"""
重复文件检测器的Tornado实现。
"""

class DuplicateFileDetectorHandler(RequestHandler):
# 改进用户体验
    """
    处理HTTP请求的Handler，用于检测重复文件。
    """
    def get(self):
        # 显示使用方法
        self.write("Please POST to this endpoint with a JSON body containing the directory path.")

    def post(self):
        """
# NOTE: 重要实现细节
        POST请求处理函数，接收包含目录路径的JSON数据。
        """
        data = self.get_json_body()
        if 'directory' not in data:
            self.set_status(400)
            self.write("Missing 'directory' in JSON body.")
            return

        directory = data['directory']
# 添加错误处理
        if not os.path.isdir(directory):
            self.set_status(400)
            self.write("The provided directory does not exist.")
            return

        try:
            duplicates = find_duplicates(directory)
            self.write({'duplicates': duplicates})
        except Exception as e:
            self.set_status(500)
            self.write(f"An error occurred: {e}")

def find_duplicates(directory):
    """
    在给定目录下查找重复文件。
    """
    hashes = {}
    duplicates = []
# 增强安全性
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_hash = _hash_file(filepath)
                if file_hash in hashes:
                    duplicates.append((filepath, hashes[file_hash]))
                else:
                    hashes[file_hash] = filepath
            except IOError:
                print(f"Cannot read file {filepath}, skipping.")
    return duplicates

def _hash_file(filepath):
    """
    计算文件的SHA-256哈希值。
    """
    hash_sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def make_app():
    """
    创建Tornado应用程序。
# 扩展功能模块
    """
    return Application([
        (r"/", DuplicateFileDetectorHandler),
    ])
# 改进用户体验

if __name__ == "__main__":
# 改进用户体验
    app = make_app()
    app.listen(8888)
    print("Server is running on port 8888...")
    IOLoop.current().start()