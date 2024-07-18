from logger_br import logger
from abc import ABC, abstractmethod
from typing import List, Any, Dict


class ExecutionContext:
    """
    管理执行环境中的共享资源，如摄像头。
    """

    def __init__(self, **kwargs):
        self.resources: Dict[str, Any] = kwargs

    def __getitem__(self, key: str) -> Any:
        return self.resources.get(key)

    def __setitem__(self, key: str, value: Any):
        self.resources[key] = value


class Task(ABC):
    """
    抽象任务类，所有任务都应继承此类。
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, context: ExecutionContext) -> None:
        """
        执行任务具体操作。
        :param context: 包含执行任务所需的外部环境和状态。
        """
        pass

    def __str__(self) -> str:
        return f"Task: {self.name}"


class TaskManager:
    """
    任务管理器，负责任务流程的控制。
    """

    def __init__(self, execution_context: ExecutionContext):
        self.tasks: List[Task] = []
        self.context = execution_context

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def add_tasks(self, tasks: List[Task]) -> None:
        self.tasks.extend(tasks)

    def run(self) -> None:
        for task in self.tasks:
            try:
                logger.info(f"Executing task: {task}")
                task.execute(self.context)
            except Exception as e:
                logger.error(f"Error executing {task}: {e}")
                continue

# 示例使用
# context = ExecutionContext(camera="CameraInstance")
# task_manager = TaskManager(execution_context=context)
# 此处添加具体任务实现和添加任务
# task_manager.add_task(ConcreteTask("Example Task"))
# task_manager.run()
