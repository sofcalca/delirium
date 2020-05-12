import os
import subprocess

from ariadne import make_executable_schema, QueryType, gql

type_defs = gql('''
  type Query {
    """
    Génére un delire
    """
    delire(text: String!, temperature: Float): String
  }
  '''
)

query = QueryType()


@query.field("delire")
def resolve_delire(_, info, text, temperature=0.1):
    model = 'flaubert-base-cased'
    length = 20
    repetition_penalty = 2

    SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
    command = f'''python {SCRIPT_DIR}/run_generation.py \
    --model_type="{model}" \
    --length={length} \
    --model_name_or_path="{model}" \
    --temperature={temperature} \
    --repetition_penalty={repetition_penalty} \
    --prompt "{text}"'''

    result = str(subprocess.check_output(command, shell=True))
    return result


schema = make_executable_schema(type_defs, query)
