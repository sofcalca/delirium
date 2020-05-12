# Generate text using Huggingface's Transformers

[![Build Status](https://travis-ci.org/sofcalca/delirium.svg?branch=master)](https://travis-ci.org/sofcalca/delirium)

Generation based on on https://github.com/huggingface/transformers/blob/master/examples/run_generation.py

## Requirements
Needs rust
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Start API
```
python -m text_generator.app
```

## Request API
Go to `http://localhost:5000/graphql` and enter your query.
