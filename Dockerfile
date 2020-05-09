FROM python:3.8-buster
EXPOSE 5000
ADD . /app
WORKDIR /app
RUN pip install .
RUN python ./text_generator/run_generation.py \
    --model_type=flaubert-base-cased \
    --length=20 \
    --model_name_or_path=flaubert-base-cased \
    --temperature=0.1 --repetition_penalty=20 --num_return_sequences=1 --prompt a

ENTRYPOINT ["python", "-m", "text_generator.app"]
