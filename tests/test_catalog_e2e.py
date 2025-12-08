import unittest
from unittest.mock import patch, MagicMock
from catalog import search_movie

class TestCatalogE2E(unittest.TestCase):
    @patch('db.movies_repository.search_movies')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_flow_e2e(self, mock_print, mock_input, mock_repo):
        
        mock_input.return_value = "Inception"
        mock_repo.return_value = [{"id": 1, "title": "Inception", "rating": 8.8}]
        

        search_movie()
        

        mock_print.assert_any_call("1.Inception-⭐8.8")

if __name__ == '__main__':
    unittest.main()