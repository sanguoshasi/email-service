from email_service.result import ErrorResult, SuccessResult, SUCCESS_MESSAGE
from email_service.submit import INVALID_SENDER_EMAIL, INVALID_RECIPIENT_EMAIL

def assert_error_result(result, message, status="error"):
    assert result.message == message
    assert result.status_code == 400
    assert result.status == status


def assert_success_result(result, message=SUCCESS_MESSAGE):
    assert result.message == message
    assert result.status_code == 200
    assert result.status == "success"

def success_response_side_effect():
    return [SuccessResult(SUCCESS_MESSAGE)]

def invalid_to_email_side_effect():
    return [ErrorResult(INVALID_RECIPIENT_EMAIL)]

def invalid_from_email_side_effect():
    return [ErrorResult(INVALID_SENDER_EMAIL)]

