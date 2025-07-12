import datetime
import pytest

from application import create_customers, process_event_history
from customer import Customer

def test_process_event_history():
    process_event_history(test_dict)


if __name__ == '__main__':
    pytest.main(['sample_tests.py'])
