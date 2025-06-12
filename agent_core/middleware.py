import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

def middleware_chain(*middlewares):
    def chain(func):
        for middleware in reversed(middlewares):
            func = middleware(func)
        return func
    return chain

def log_question_middleware(func):
    def wrapper(question, *args, **kwargs):
        print(f"[MIDDLEWARE] Pergunta recebida: {question}")
        return func(question, *args, **kwargs)
    return wrapper

def validate_question_middleware(func):
    def wrapper(question, *args, **kwargs):
        if not question or len(question.strip()) < 5:
            raise ValueError("Pergunta muito curta ou vazia.")
        return func(question, *args, **kwargs)
    return wrapper 