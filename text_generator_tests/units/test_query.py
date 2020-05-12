import os
import unittest
from unittest.mock import MagicMock, patch

from text_generator.query import resolve_delire


class ResolveDelireTest(unittest.TestCase):
    mocked_check_output = MagicMock(return_value="text generated")
    @patch("text_generator.query.subprocess.check_output", mocked_check_output)
    def test_should_call_text_generation_script_with(self):
        # Given
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '../../..'))
        expected_command = f'''python {SCRIPT_DIR}/text_generator/run_generation.py \
    --model_type="flaubert-base-cased" \
    --length=20 \
    --model_name_or_path="flaubert-base-cased" \
    --temperature=0.1 \
    --repetition_penalty=2 \
    --prompt "text"'''

        # When
        response = resolve_delire(MagicMock(), MagicMock(), "text", temperature=0.1)

        # Then
        ResolveDelireTest.mocked_check_output.assert_called_once_with(expected_command, shell=True)
        self.assertEqual("text generated", response)
