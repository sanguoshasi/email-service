SUCCESS_MESSAGE = "Email sent successfully!"

class Result(object):
    # standardize the results from Mandrill and Mailgun
    def __init__(self, status, message, status_code=400):
        self.status_code = status_code
        self.status = status
        self.message = message


class SuccessResult(Result):
    def __init__(self, message, status_code=200):
        super(type(self), self).__init__("success", message, status_code)


class ErrorResult(Result):
    def __init__(self, message, status_code=400):
        super(type(self), self).__init__("error", message, status_code)