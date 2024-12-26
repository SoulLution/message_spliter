import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from bs4 import BeautifulSoup
from io import StringIO
from unittest import mock
from msg_split import soap_loop, split_message
from utils.is_too_long_string import is_too_long_string
from utils.reduce_elements import reduce_start_elements, reduce_last_elements


class TestMsgSplit(unittest.TestCase):

    def test_reduce_start_element(self):
        
        elements = ''
        self.assertRaises(ValueError, reduce_start_elements, elements)

        elements = []
        self.assertEqual(reduce_start_elements(elements), "")

        html = "<pre>Test</pre><a>Link</a>"
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find_all()
        self.assertEqual(reduce_start_elements(elements), "")
        
        html = "<div>Content</div><span>Test</span><p>Paragraph</p>"
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find_all()
        self.assertEqual(reduce_start_elements(elements), "<p><span><div>")

        
        html = "<div>Content<span>More Content</span></div>"
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.span.parents
        self.assertEqual(reduce_start_elements(elements), "<div>")

    def test_reduce_last_element(self):
        elements = ''
        self.assertRaises(ValueError, reduce_last_elements, elements)

        elements = []
        self.assertEqual(reduce_last_elements(elements), "")

        html = "<pre>Test</pre><a>Link</a>"
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find_all()
        self.assertEqual(reduce_last_elements(elements), "")

        html = "<div>Content</div><span>Test</span><p>Paragraph</p>"
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find_all()
        self.assertEqual(reduce_last_elements(elements), "</div></span></p>")


        html = "<div>Content<span>More Content</span></div>"
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.span.parents
        self.assertEqual(reduce_last_elements(elements), "</div>")

    def test_is_too_long_string(self):
        string = ''
        max_len = 10
        self.assertEqual(is_too_long_string(string, max_len), False)
        
        string = '0123456789'
        max_len = 10
        self.assertEqual(is_too_long_string(string, max_len), True)
        
        string = '0123456789'
        max_len = 11
        self.assertEqual(is_too_long_string(string, max_len), False)
        
        string = '  0123456789'
        max_len = 11
        self.assertEqual(is_too_long_string(string, max_len), True)


    def test_soap_loop(self):
        data_soup = BeautifulSoup('<div>foo!<span><a href="https://mockdata.atlassian.net/browse/ABC-11872"><code>ABC-11872</code></a>Etiam cursus nisi eget tortor feugiat.</span></div>', 'html.parser')
        div = data_soup.div
        self.assertEqual(soap_loop('<div>', div, 200), '<div>foo!<span><a href="https://mockdata.atlassian.net/browse/ABC-11872"><code>ABC-11872</code></a>Etiam cursus nisi eget tortor feugiat.</span>')
        
        data_soup = BeautifulSoup('<div>foo!<span><a href="https://mockdata.atlassian.net/browse/ABC-11872"><code>ABC-11872</code></a>Etiam cursus nisi eget tortor feugiat.</span></div>', 'html.parser')
        div = data_soup.div
        self.assertEqual(soap_loop('<div>', div, 120), '<div>foo!<span><a href="https://mockdata.atlassian.net/browse/ABC-11872"><code>ABC-11872</code></a></span>')



    def test_split_message(self):

        with open('./html/false_test.html', 'r', encoding='utf-8') as file:
            content = file.read()
        max_len = 80

        with mock.patch("sys.stdout", new_callable=StringIO):
            with self.assertRaises(SystemExit):
                for i, chunk in enumerate(split_message(content, max_len)):
                    continue



        with open('./html/false_test.html', 'r', encoding='utf-8') as file:
            content = file.read()
        max_len = 4096
        
        with mock.patch("sys.stdout", new_callable=StringIO):
            fragments = list(split_message(content, max_len))

        self.assertEqual(len(fragments), 1)
        self.assertEqual(fragments[0], content)



        with open('./html/min_test.html', 'r', encoding='utf-8') as file:
            content = file.read()
        max_len = 256
        with mock.patch("sys.stdout", new_callable=StringIO):
            fragments = list(split_message(content, max_len))
        
        self.assertGreater(len(fragments), 3)
        self.assertTrue(all(len(fragment) <= max_len for fragment in fragments)) 

        

        with open('./html/test.html', 'r', encoding='utf-8') as file:
            content = file.read()
        max_len = 4096
        with mock.patch("sys.stdout", new_callable=StringIO):
            fragments = list(split_message(content, max_len))
        
        self.assertGreater(len(fragments), 1)
        self.assertTrue(all(len(fragment) <= max_len for fragment in fragments)) 

if __name__ == "__main__":
    unittest.main()