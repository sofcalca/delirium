import unittest
from unittest.mock import patch, MagicMock

from text_generator.app import graphql_playgroud, graphql_server
from text_generator.query import schema


class GraphqlPlaygroudTest(unittest.TestCase):
    def test_returns_playground_page(self):
        # Given
        expected_content = """<!DOCTYPE html>
<html>

<head>
  <meta charset=utf-8/>
  <meta name="viewport" content="user-scalable=no, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, minimal-ui">
  <title>GraphQL Playground</title>
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
  <link rel="shortcut icon" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/favicon.png" />
  <script src="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
</head>

<body>
  <div id="root">
    <style>
      body {
        background-color: rgb(23, 42, 58);
        font-family: Open Sans, sans-serif;
        height: 90vh;
      }
      #root {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .loading {
        font-size: 32px;
        font-weight: 200;
        color: rgba(255, 255, 255, .6);
        margin-left: 20px;
      }
      img {
        width: 78px;
        height: 78px;
      }
      .title {
        font-weight: 400;
      }
    </style>
    <img src='//cdn.jsdelivr.net/npm/graphql-playground-react/build/logo.png' alt=''>
    <div class="loading"> Loading
      <span class="title">GraphQL Playground</span>
    </div>
  </div>
  <script>window.addEventListener('load', function (event) {
      GraphQLPlayground.init(document.getElementById('root'), {
        // options as 'endpoint' belong here
      })
    })</script>
</body>

</html>"""

        # When
        content, status_code = graphql_playgroud()

        # Then
        self.assertEqual(status_code, 200)
        self.assertEqual(content, expected_content)


class GraphqlServerTest(unittest.TestCase):
    query = "{\n  delire(text: \"Ceci est un test\", temperature: 0.1)\n}\n"
    json = {
        "operationName": None,
        "variables": {},
        "query": query
    }
    mocked_request = MagicMock()
    mocked_request.get_json = MagicMock(return_value=json)
    mocked_graph_sync = MagicMock(return_value=(True, {"data": b"test"}))
    mocked_jsonify = MagicMock(return_value=b"result")

    def refresh_mocks(self):
        GraphqlServerTest.mocked_request.reset_mock()
        GraphqlServerTest.mocked_graph_sync.reset_mock()
        GraphqlServerTest.mocked_jsonify.reset_mock()

    @patch("text_generator.app.request", mocked_request)
    @patch("text_generator.app.graphql_sync", mocked_graph_sync)
    @patch("text_generator.app.jsonify", mocked_jsonify)
    def test_should_return_result_if_graphql_sync_succeds(self):
        # When
        content, status_code = graphql_server()

        # Then
        GraphqlServerTest.mocked_graph_sync.assert_called_once_with(
            schema,
            GraphqlServerTest.json,
            context_value=GraphqlServerTest.mocked_request,
            debug=False
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(content, b"result")

    @patch("text_generator.app.request", mocked_request)
    @patch("text_generator.app.graphql_sync", mocked_graph_sync)
    @patch("text_generator.app.jsonify", mocked_jsonify)
    def test_should_return_status_code_400_if_graphql_sync_fails(self):
        # Given
        self.refresh_mocks()
        GraphqlServerTest.mocked_graph_sync.return_value = (False, "error message")
        # When
        content, status_code = graphql_server()

        # Then
        GraphqlServerTest.mocked_graph_sync.assert_called_once_with(
            schema,
            GraphqlServerTest.json,
            context_value=GraphqlServerTest.mocked_request,
            debug=False
        )
        self.assertEqual(status_code, 400)
        self.assertEqual(content, b"result")

