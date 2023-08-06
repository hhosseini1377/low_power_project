import random
from task import task, backup_schedule
from UUnifast import UUniFastDiscard

def power(alpha, Alpha, f):
    return alpha*(f**3) + Alpha

def Static_Faster(task_set):
    backup_entities = backup_schedule(task_set, False).schedule_entities
    total_C_hp = 0
    for task in task_set:
        total_C_hp += task.hp_C
    scaling_factor = total_C_hp/100
    energy = 0
    start_time_p = 0
    end_time_p = 0
    for task in task_set:
        energy += power(1, 0.1, scaling_factor)*(task.hp_C/scaling_factor)
        end_time_p += task.hp_C/scaling_factor
        backup_entity = next(filter(lambda entity: entity.task == task, backup_entities), None)
        if backup_entity.start_time < end_time_p:
            overlap = min(end_time_p-backup_entity.start_time, backup_entity.end_time - backup_entity.start_time )
            print(overlap)
        else:
            print('na')
        start_time_p = end_time_p
    print(energy)

utilization_lp = random.uniform(0.3, 1)
n = 10
task_set = []

lp_utils = UUniFastDiscard(n, utilization_lp, 1)[0]

for util in lp_utils:
    new_task = task(util)
    task_set.append(new_task)


f_max_lp = random.uniform(0.7, 0.9)

Static_Faster(task_set)


