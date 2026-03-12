from app.application.container import worker_executor
from app.worker.consumer import WorkerConsumer


def main() -> None:
    consumer = WorkerConsumer(executor=worker_executor)
    consumer.run_forever()


if __name__ == "__main__":
    main()
