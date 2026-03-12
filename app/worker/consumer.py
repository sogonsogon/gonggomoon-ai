from time import sleep

from app.core.config import get_settings
from app.worker.executor import WorkerExecutor

# WorkerConsumer는 워커 프로세스에서 큐를 지속적으로 모니터링하면서 작업을 처리하는 역할을 합니다.
class WorkerConsumer:
    def __init__(self, executor: WorkerExecutor) -> None:
        self.executor = executor
        self.settings = get_settings()

    def run_forever(self) -> None:
        while True:
            # process_once 메서드를 호출하여 큐에서 작업을 하나 처리합니다.
            has_processed = self.executor.process_once()
            if not has_processed:
                sleep(self.settings.worker_poll_interval_seconds)
