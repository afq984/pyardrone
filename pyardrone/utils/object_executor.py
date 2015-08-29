import threading
import queue
import time


class Interrupt:

    def __init__(self, obj_exe, wait, discard):
        self.obj_exe = obj_exe
        self.wait = wait
        self.discard = discard

    def __enter__(self):
        self.obj_exe.pause(wait=self.wait)

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            if self.discard:
                q = self.obj_exe._queue
                with self.obj_exe._queue_lock:
                    with q.mutex:
                        q.queue.clear()
                        q.all_tasks_done.notify_all()
                        q.unfinished_tasks = 0
            self.obj_exe.resume()


class ObjectExecutor:

    def __init__(self, target, interval, default):
        self._target = target
        self.default = default
        self.interval = interval
        self._queue = queue.Queue()
        self._queue_lock = threading.Lock()
        self._thread = threading.Thread(target=self._job)
        self._stop_event = threading.Event()
        self._working_event = threading.Event()

    def start(self):
        self._stop_event.clear()
        self._working_event.set()
        self._thread.start()

    def stop(self, wait=False):
        if wait:
            self.join()
        self._stop_event.set()
        self.join()

    def pause(self, wait=False):
        if wait:
            self.join()
        self._working_event.clear()

    def resume(self):
        self._working_event.set()

    def interrupt(self, *, wait=False, discard=True):
        return Interrupt(self, wait=wait, discard=discard)

    def join(self):
        self._queue.join()

    def put(self, obj, with_event=True):
        if with_event:
            event = threading.Event()
        else:
            event = None
        self._queue.put((obj, event))
        return event

    def _process_object(self):
        with self._queue_lock:
            try:
                obj, event = self._queue.get_nowait()
                call_task_done = True
            except queue.Empty:
                obj, event = self.default, None
                call_task_done = False
            self._target(obj)
            if event is not None:
                event.set()
            if call_task_done:
                self._queue.task_done()

    def _job(self):
        while not self._stop_event.is_set():
            self._working_event.wait()
            self._process_object()
            time.sleep(self.interval)
