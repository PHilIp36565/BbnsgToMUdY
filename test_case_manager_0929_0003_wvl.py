# 代码生成时间: 2025-09-29 00:03:21
import tornado.ioloop
import tornado.web

"""
Test Case Manager Service

This service manages test cases using the Tornado framework. It provides API endpoints
to add, retrieve, update, and delete test cases.
"""

# Define the Test Case data model
class TestCase:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

# In-memory storage for test cases
test_cases = {}

# API handler for test cases
class TestCaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        """
        Override to provide JSON error responses.
        """
        self.finish({'error': 'An error occurred', 'status_code': status_code})

    # POST /test_cases - Add a new test case
    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            test_case = TestCase(id=len(test_cases) + 1, name=data['name'], description=data['description'])
            test_cases[test_case.id] = test_case
            self.write({'id': test_case.id, 'name': test_case.name, 'description': test_case.description})
        except Exception as e:
            self.write_error(400, message=str(e))

    # GET /test_cases/{id} - Retrieve a test case by ID
    def get(self, test_case_id):
        try:
            test_case = test_cases.get(int(test_case_id))
            if test_case:
                self.write({'id': test_case.id, 'name': test_case.name, 'description': test_case.description})
            else:
                self.write_error(404, message='Test case not found')
        except Exception as e:
            self.write_error(400, message=str(e))

    # PUT /test_cases/{id} - Update a test case
    def put(self, test_case_id):
        try:
            data = tornado.escape.json_decode(self.request.body)
            test_case = test_cases.get(int(test_case_id))
            if test_case:
                test_case.name = data.get('name', test_case.name)
                test_case.description = data.get('description', test_case.description)
                test_cases[test_case.id] = test_case
                self.write({'id': test_case.id, 'name': test_case.name, 'description': test_case.description})
            else:
                self.write_error(404, message='Test case not found')
        except Exception as e:
            self.write_error(400, message=str(e))

    # DELETE /test_cases/{id} - Delete a test case
    def delete(self, test_case_id):
        try:
            test_case = test_cases.pop(int(test_case_id), None)
            if test_case:
                self.write({'id': test_case.id, 'name': test_case.name, 'description': test_case.description})
            else:
                self.write_error(404, message='Test case not found')
        except Exception as e:
            self.write_error(400, message=str(e))

# Define the application settings
def make_app():
    return tornado.web.Application([
        (r"/test_cases/([^\/]+)?", TestCaseHandler),
    ])

# Start the application
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Test Case Manager Service started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()