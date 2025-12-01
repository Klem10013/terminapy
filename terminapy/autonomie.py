import threading as th

def start_worker(target, *args, **kwargs) -> th.Thread:
    worker = th.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    worker.start()
    return worker