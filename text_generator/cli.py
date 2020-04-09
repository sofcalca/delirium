#!/usr/bin/python
# coding=utf-8

from __future__ import print_function

import os

import click


@click.command('start_delirium_from')
@click.argument('text', nargs=-1)
def start_delirium_from(text: [str]):
    concatenated_text = ' '.join(text)
    SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
    _system(f'''python {SCRIPT_DIR}/run_generation.py \
    --model_type=flaubert-base-cased \
    --length=20 \
    --model_name_or_path=flaubert-base-cased \
    --temperature=0.1 \
    --repetition_penalty=20 \
    --num_return_sequences=1 \
    --prompt "{concatenated_text}"''', False)


def _system(cmd: str, logged: bool = True):
  if logged:
    print('$ {0}'.format(cmd))
  output = os.system(cmd)
  # see : https://stackoverflow.com/a/6466753
  error_code = output >> 8
  if error_code > 0:
    raise OSError(error_code)

if __name__ == '__main__':
    start_delirium_from()
