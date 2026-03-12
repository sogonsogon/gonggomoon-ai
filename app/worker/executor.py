from app.application.ports.ports import CallbackPort, JobQueuePort
from app.worker.handlers import JobHandler


class WorkerExecutor:
    def __init__(self, queue: JobQueuePort, handler: JobHandler, callback_client: CallbackPort) -> None:
        self.queue = queue
        self.handler = handler
        self.callback_client = callback_client

    # 워커가 한 번 작업을 처리하는 메서드입니다.
    # 큐에서 작업 메시지를 하나 가져와서 처리한 후, 콜백 URL로 결과를 전송합니다.
    # 처리할 메시지가 없으면 False를 반환하고, 처리했으면 True를 반환합니다.
    # 이 메서드는 WorkerConsumer에서 주기적으로 호출됩니다.
    def process_once(self) -> bool:
        message = self.queue.dequeue()
        if message is None:
            return False

        # 콜백 Body가 JobType마다 달라질 수 있지 않나 ?
        callback_body = self.handler.handle(message)
        self.callback_client.send(message.callback_url, callback_body)
        return True
