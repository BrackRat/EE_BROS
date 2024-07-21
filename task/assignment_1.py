from task import Task
from logger_br import logger
from task import ExecutionContext
from .base.start_and_end import StartCommandTask, StopCommandTask
from .base.drive_to import FollowLineUntilTurnPoint, GoStraightTask, DriveToEndTask


class CarRunOuterCircleNoUltrasound(Task):
    def __init__(self, name):
        super().__init__(name)
        # 子任务列表
        self.tasks = [
            # StartCommandTask("Send Start Command"),
            FollowLineUntilTurnPoint("Drive to Intersection", base_speed=15, max_speed_dela=8, clear_pid=False),
            GoStraightTask("Go Straight"),
            DriveToEndTask("Drive to End"),
            StopCommandTask("Send Stop Command")
        ]

    def execute(self, context: ExecutionContext):
        for task in self.tasks:
            task.execute(context)
            if context['should_stop']:  # 假设这是一个检测是否中断任务的标志
                logger.info("Task interrupted.")
                break
        logger.info("Outer circle run task completed.")
