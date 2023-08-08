import random
from task import task, backup_schedule
from UUnifast import UUniFastDiscard

def power(alpha, Alpha, f):
    return alpha*(f**3) + Alpha

def Static_Faster(task_set, alpha, Alpha):
    backup_entities = backup_schedule(task_set, False).schedule_entities
    total_C_hp = 0
    for task in task_set:
        total_C_hp += task.hp_C
    scaling_factor = total_C_hp/100
    energy = 0
    end_time_p = 0
    for task in task_set:
        energy += power(alpha, Alpha, scaling_factor)*(task.hp_C/scaling_factor)
        end_time_p += task.hp_C/scaling_factor
        backup_entity = next(filter(lambda entity: entity.task == task, backup_entities), None)
        if backup_entity.start_time < end_time_p:
            overlap = min(end_time_p-backup_entity.start_time, backup_entity.end_time - backup_entity.start_time )
            energy += power(alpha, Alpha, 1)*overlap*task.p_scale
    return energy

def Static_Slower(task_set, alpha, Alpha):
    backup_entities = backup_schedule(task_set, True).schedule_entities
    total_C_lp = 0
    for task in task_set:
        total_C_lp += task.lp_C
    scaling_factor = total_C_lp/100
    energy = 0
    end_time_p = 0
    for task in task_set:
        energy += power(alpha, Alpha, scaling_factor)*(task.lp_C/scaling_factor)*task.p_scale
        end_time_p += task.lp_C/scaling_factor
        backup_entity = next(filter(lambda entity: entity.task == task, backup_entities), None)
        if backup_entity.start_time < end_time_p:
            overlap = min(end_time_p-backup_entity.start_time, backup_entity.end_time - backup_entity.start_time )
            energy += power(alpha, Alpha, 1)*overlap
    return energy

def MO_faster(task_set, alpha, Alpha):
    f_ee = (Alpha/alpha)**(1/3)
    backup_entities = backup_schedule(task_set, False).schedule_entities
    energy = 0
    start_time_p = 0
    for task in task_set:
        backup_entity = next(filter(lambda entity: entity.task == task, backup_entities), None)
        f_u = task.hp_C/(backup_entity.start_time-start_time_p)
        f_u = min(1, f_u)
        f_u = max(f_u, f_ee)
        print(backup_entity.start_time, backup_entity.end_time, start_time_p, f_u)
        start_time_p += task.hp_C/f_u
    return energy   

def main():
    utilization_lp = random.uniform(0.3, 1)
    utilization_lp = 0.9
    n = 10
    task_set = []
    alpha, Alpha = 1, 0.1
    lp_utils = UUniFastDiscard(n, utilization_lp, 1)[0]

    for util in lp_utils:
        new_task = task(util)
        task_set.append(new_task)

    f_max_lp = random.uniform(0.7, 0.9)
    print(MO_faster(task_set, alpha, Alpha))

if __name__ == "__main__":
    main()

