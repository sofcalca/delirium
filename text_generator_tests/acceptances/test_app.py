import unittest
from text_generator.app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_returns_playground_page(self):
        # Given
        expected_content = b'<!DOCTYPE html>\n<html>\n\n<head>\n  <meta charset=utf-8/>\n  <meta name=' + \
        b'"viewport" content="user-scalable=no, initial-scale=1.0, minimum-scale=1.0, '  + \
        b'maximum-scale=1.0, minimal-ui">\n  <title>GraphQL Playground</title>\n  <l'  + \
        b'ink rel="stylesheet" href="//cdn.jsdelivr.net/npm/graphql-playground-react/b'  + \
        b'uild/static/css/index.css" />\n  <link rel="shortcut icon" href="//cdn.js'  + \
        b'delivr.net/npm/graphql-playground-react/build/favicon.png" />\n  <script '  + \
        b'src="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middlew'  + \
        b'are.js"></script>\n</head>\n\n<body>\n  <div id="root">\n    <style>\n    '  + \
        b'  body {\n        background-color: rgb(23, 42, 58);\n        font-family:'  + \
        b' Open Sans, sans-serif;\n        height: 90vh;\n      }\n      #root {\n    '  + \
        b'    height: 100%;\n        width: 100%;\n        display: flex;\n        al'  + \
        b'ign-items: center;\n        justify-content: center;\n      }\n      .loadi'  + \
        b'ng {\n        font-size: 32px;\n        font-weight: 200;\n        color: r'  + \
        b'gba(255, 255, 255, .6);\n        margin-left: 20px;\n      }\n      img {\n '  + \
        b'       width: 78px;\n        height: 78px;\n      }\n      .title {\n       ' + \
        b" font-weight: 400;\n      }\n    </style>\n    <img src='//cdn.jsdelivr.net" + \
        b'/npm/graphql-playground-react/build/logo.png\' alt=\'\'>\n    <div class="lo' + \
        b'ading"> Loading\n      <span class="title">GraphQL Playground</span>\n    ' + \
        b"</div>\n  </div>\n  <script>window.addEventListener('load', function (even" + \
        b"t) {\n      GraphQLPlayground.init(document.getElementById('root'), {\n   " + \
        b"     // options as 'endpoint' belong here\n      })\n    })</script>\n</bod" + \
        b'y>\n\n</html>'

        # When
        response = self.client.get('/graphql')

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_content, response.data)

    def test_graphql_server_should_return_text_generation(self):
        # Given
        query = "{\n  delire(text: \"Ceci est un test\", temperature: 0.1)\n}\n"
        json = {
            "operationName": None,
            "variables": {},
            "query": query
        }
        expected_content = b'{"data":{"delire":"b\'=== GENERATED SEQUENCE 1 ===\\\\nCeci est un test a p' + \
        b'ris totis\\\\xc3\\\\xa9elle et le la llales \\" - s (, je mais\\\\\'me\\\\' + \
        b'n\'"}}\n'

        # When
        response = self.client.post('/graphql', json=json)

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_content, response.data)
