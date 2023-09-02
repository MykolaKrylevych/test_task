import unittest
from main import add_new_data
from unittest.mock import patch, Mock


class TestExternalServiceInteraction(unittest.TestCase):
    @patch('main.get')
    @patch('main.ActivityDatabase')
    def test_add_new_data(self, mock_db, mock_get):
        db_instance = Mock()
        mock_db.return_value = db_instance
        mock_response = Mock(status_code=200)
        mock_get.return_value = mock_response
        mock_response.json.return_value = {'activity': 'Sample Activity'}

        args = Mock(type=None, accessibility_min=None, accessibility_max=None, participants=None,
                    price_min=None, price_max=None)
        result = add_new_data(args)

        self.assertEqual(result, "Activity successfully added to database :)")

        db_instance.save_activity.assert_called_once_with({'activity': 'Sample Activity'})

        db_instance.close_connection.assert_called_once()


if __name__ == "__main__":
    unittest.main()
