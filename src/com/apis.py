# encoding=utf-8
from src.com.docker.machine import VMachine, VMStatus, LMachine
from mycroft.packages.old.framework.command.factory import SmartCommandFactory



def filter_machines(machine_groups, match):
    if not machine_groups:
        return []
    vms = {}
    for i, match in enumerate(match.split(',')):
        match = match.strip()
        ms = match.split(':', 1)
        if len(ms) == 2:
            t, m = ms
        else:
            t, m = 'id', ms[-1]
        gs = m.split('.', 1)
        if len(gs) == 2:
            g, m = gs
        else:
            g, m = None, gs[-1]
        machines = machine_groups.get(g, [])
        if m == "*":
            for j, v in enumerate(machines):
                key = (g, v.id)
                if key not in vms:
                    vms[key] = ((i, j), v)
            break
        elif t == 'id':
            for j, v in enumerate(machines):
                if v.name == m:
                    key = (g, v.id)
                    if key not in vms:
                        vms[key] = ((i, j), v)
                    break
        elif t == 'group':
            for j, v in enumerate(machines):
                if v.group == m:
                    key = (g, v.id)
                    if key not in vms:
                        vms[key] = ((i, j), v)
        else:
            raise Exception("invalid match type %s" % t)
    return [v for i, v in sorted(vms.values(), key=lambda x: x[0])]



def has_command(name, kwargs):
    try:
        SmartCommandFactory.get_cmd(name)
        return True
    except ValueError:
        return False


def default_machines():
    return [LMachine(), ]


def run(name, kwargs, machines=None):
    if machines is None:
        machines = default_machines()
    results = {}
    for m in machines:
        cmd = SmartCommandFactory(m, type=name, **kwargs).gen_cmd()
        result = cmd.run()
        results[m.name] = result
    if len(results) == 1:
        return results.values()[0]
    else:
        return results


def create_docker(kwargs, safe=False, create=True):
    vm_info = {
        'name': kwargs['id'],
        'ip': kwargs['ip'] + '/24',
        'project': kwargs['project'],
        'desc': kwargs['desc'],
        'gateway': kwargs['gateway'],
        '': kwargs['dockerflyd'],
        'group': kwargs.get('group', 'default'),
        'veths': kwargs.get('veths')
    }
    vm = VMachine(**vm_info)
    if create:
        if safe:
            if vm.status == VMStatus.NOPRESENT:
                vm.create()
        elif not safe:
            if vm.status != VMStatus.NOPRESENT:
                vm.delete()
            vm.create()
    return vm
