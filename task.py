import random

class task():
    def __init__(self, lp_utilization) -> None:
        self.lp_utilization = lp_utilization
        self.t_scale = random.uniform(1.4, 2.3)
        self.hp_utilization = lp_utilization/self.t_scale
        self.lp_C = 100*self.lp_utilization
        self.hp_C = 100*self.hp_utilization
        self.p_scale = 0.8

class backup_schedule():
    def __init__(self, task_set, primary) -> None:
        self.task_set = task_set
        self.schedule_entities = []
        time = 100
        for i in range(9, -1, -1):
            if primary:
                new_backup_schedule_entity = backup_schedule_entity(task_set[i], time-task_set[i].hp_C, time)
                self.schedule_entities.append(new_backup_schedule_entity)
                time = time-task_set[i].hp_C
            else:
                new_backup_schedule_entity = backup_schedule_entity(task_set[i], time-task_set[i].lp_C, time)
                self.schedule_entities.append(new_backup_schedule_entity)          
                time = time-task_set[i].lp_C

class backup_schedule_entity():
    def __init__(self, task, start_time, end_time) -> None:
        self.task = task
        self.start_time = start_time
        self.end_time = end_time