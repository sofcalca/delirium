Based on https://github.com/huggingface/transformers/blob/master/examples/run_generation.py

## Start API
```
python -m text_generator.app
```

## Request API
```
curl -X POST --header "Content-Type: application/json" --data '{"text":"Je commence ma phrase, mais", "model": "flaubert-base-cased", "length": 20, "temperature": 0.5, "repetition_penalty": 1.8}' http://localhost:5000/
```

## Run with CLI
```
python -m text_generator.cli
```
