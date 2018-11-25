import json


class HostsNotFound(Exception):
    """Raised when a host does not exists in inventory

    Example: raise HostNotFound("host1")
    """
    pass


class GroupsNotFound(Exception):
    """Raised when a group does not exists in inventory

    Example: raise GroupNotFound("group1")
    """
    pass


class AnsibleInventory:
    def __init__(self, *hosts):
        self._inventory = {
            "_meta": {
                "hostvars": {}
            },
            "all": {
                "vars": {},
                "hosts": set(),
                "children": set(["ungrouped"])
            },
            "ungrouped": {
                "hosts": set()
            }
        }

        # internal attributes for easy access to parts of above inventory
        self._all_hosts = self._inventory["all"]["hosts"]
        self._all_children = self._inventory["all"]["children"]
        self._ungrouped_hosts = self._inventory["ungrouped"]["hosts"]
        self._hostvars = self._inventory["_meta"]["hostvars"]

        for host in hosts:
            self.add_host(host)

    def add_host(self, host, **hostvars):
        if host not in self._all_hosts:
            self._all_hosts.add(host)
            self._ungrouped_hosts.add(host)
            self._hostvars[host] = hostvars

    def get_hostvars(self, host):
        try:
            return self._hostvars[host]
        except KeyError:
            raise HostsNotFound(host)

    def update_hostvars(self, host, **hostvars):
        try:
            self._hostvars[host].update(hostvars)
        except KeyError:
            raise HostsNotFound(host)

    def add_group(self, group, **groupvars):
        if group in ("_meta", "ungrouped"):
            raise ValueError("a new group cannot use the reserved name '{}'".format(group))

        if group not in self.groups:
            self._inventory[group] = {
                "vars": groupvars,
                "hosts": set(),
                "children": set()
            }
            self._all_children.add(group)

    def get_groupvars(self, group):
        if group not in self.groups:
            raise GroupsNotFound(group)

        return self._inventory[group]["vars"]

    def update_groupvars(self, group, **groupvars):
        if group not in self.groups:
            raise GroupsNotFound(group)

        self._inventory[group]["vars"].update(groupvars)

    def add_hosts_to_group(self, group, *hosts):
        if group not in self.groups:
            raise GroupsNotFound(group)

        # Every host is always a member of 'all' hence do nothing
        if group == "all":
            return

        hosts = set(hosts)

        non_existing = hosts - self._all_hosts
        if non_existing:
            raise HostsNotFound(non_existing)

        self._ungrouped_hosts -= hosts
        self._inventory[group]["hosts"] |= hosts

    def add_children_to_group(self, parent, *children):
        # check all groups exists and they are allowed to be modified
        non_existing = set((parent,) + children) - set(self.groups)
        # FYI Python3 only syntax can be like:
        # non_existing = set([parent, *children]) - set(self.groups)
        if non_existing:
            raise GroupsNotFound(non_existing)

        # avoid circular dependency
        if parent in children:
                raise ValueError("group '{}' cannot be a child to itself".format(parent))

        # finally add all children to parent
        self._inventory[parent]["children"] |= set(children)

    def keep_hosts_ungrouped_also(self, *hosts):
        hosts = set(hosts)
        non_existing = hosts - self._all_hosts
        if non_existing:
            raise HostsNotFound(non_existing)

        self._ungrouped_hosts |= hosts

    @property
    def hosts(self):
        return list(self._all_hosts)

    @property
    def ungrouped(self):
        return list(self._ungrouped_hosts)

    @property
    def groups(self):
        grps = list(self._inventory)
        grps.remove("ungrouped")
        grps.remove("_meta")
        return grps

    def __str__(self):
        class SetJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, set):
                    return list(obj)
                # Let the base class default method raise the TypeError
                return json.JSONEncoder.default(self, obj)

        return json.dumps(self._inventory, indent=2, cls=SetJSONEncoder)

    def _host_as_ini(self, host):
        hostline = [host]
        for var, val in self._inventory["_meta"]["hostvars"][host].items():
            hostline.append("{}={}".format(var, val))

        return " ".join(hostline)

    def as_ini(self):
        final = []

        # process ungrouped hosts
        for host in self._inventory["ungrouped"]["hosts"]:
            final.append(self._host_as_ini(host))

        # process groups
        for group in set(self.groups) - {"all"}:
            data = self._inventory[group]

            if data["hosts"]:
                final.append("\n[{}]".format(group))
                for host in data["hosts"]:
                    final.append(self._host_as_ini(host))

            if data["vars"]:
                final.append("\n[{}:vars]".format(group))
                for var, val in data["vars"].items():
                    final.append("{}={}".format(var,val))

            if data["children"]:
                final.append("\n[{}:children]".format(group))
                for child in data["children"]:
                    final.append("{}".format(child))

        # process all:vars
        if self._inventory["all"]["vars"]:
            final.append("\n[{}:{}]".format("all","vars"))
            for var, val in self._inventory["all"]["vars"].items():
                final.append("{}={}".format(var,val))

        return "\n".join(final) + "\n"

