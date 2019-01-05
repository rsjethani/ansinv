import copy
import json


class AnsibleHost:
    def __init__(self, name, **hostvars):
        self.name = name
        self.hostvars = hostvars

    def __str__(self):
        pieces = [self.name]
        for var, val in self.hostvars.items():
            pieces.append("{}={}".format(var, val))
        return " ".join(pieces)


class AnsibleGroup:
    def __init__(self, name, **groupvars):
        self._hosts = []
        self.name = name
        self._children = []
        self.groupvars = groupvars
    
    @property
    def hosts(self):
        return self._hosts

    @property
    def children(self):
        return self._children

    def add_hosts(self, *hosts):
        for host in hosts:
            self._hosts.append(copy.deepcopy(host))

    def add_children(self, *children):
        for group in children:
            if group.name == self.name:
                raise ValueError("can't add group to itself.")
            
            if group.is_parent_of(self):
                raise ValueError("can't add parent as a child.")
            
            self._children.append(group.name)
        
    def host(self, hostname):
        for host in self._hosts:
            if host.name == hostname:
                return host
        return None

    def is_child_of(self, group):
        return self.name in group.children

    def is_parent_of(self, group):
        return group.name in self.children

    def __str__(self):
        pieces = []
        if self._hosts:
            pieces.append("\n[{}]".format(self.name))
            for host in self._hosts:
                pieces.append(str(host))

        if self.groupvars:
            pieces.append("\n[{}:vars]".format(self.name))
            for var, val in self.groupvars.items():
                pieces.append("{}={}".format(var,val))

        if self._children:
            pieces.append("\n[{}:children]".format(self.name))
            for child in self._children:
                pieces.append(str(child))

        return "\n".join(pieces)


class AnsibleInventory:
    def __init__(self, *ungrouped):
        self._ungrouped = list(ungrouped)
        self._groups = [AnsibleGroup("all")]

    def add_hosts(self, *hosts):
        for host in hosts:
            self._ungrouped.append(copy.deepcopy(host))

    def add_groups(self, *groups):
        for group in groups:
            self._groups.append(copy.deepcopy(group))

    def host(self, hostname):
        for host in self._ungrouped:
            if host.name == hostname:
                return host
        return None

    def group(self, groupname):
        for group in self._groups:
            if group.name == groupname:
                return group
        return None

    @property
    def groups(self):
        return self._groups

    def __str__(self):
        final = []

        # process ungrouped hosts
        for host in self._ungrouped:
            final.append(str(host))

        # process groups except 'all'
        for group in self._groups[1:]:
            final.append(str(group))

        # process group 'all'
        final.append(str(self._groups[0]))
        
        return "\n".join(final).strip()

