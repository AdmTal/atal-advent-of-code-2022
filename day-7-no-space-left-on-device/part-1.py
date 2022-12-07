system_output_lines = open('./example-input.txt').read().split('\n')

"""

Read through commands once ...

Each command give info - and must be processed immediatly

You either learn about this DIR - or another.

We need a Tree + a hash that points to nodes on the tree

When we add a child node - we need to update the size, and then propagate that to the root

"""


class FileTreeNode(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._size = 0
        self._parent = parent
        self._children = {}

    @property
    def name(self):
        return self._name

    @property
    def children(self):
        return self._children


executing_ls = False
PWD = None

FILE_TREE_ROOT = FileTreeNode('/')
NODE_LOOKUP = {
    FILE_TREE_ROOT.name: FILE_TREE_ROOT,
}

for line in system_output_lines:
    line_is_commmand = line[0] == '$'

    if executing_ls and not line_is_commmand:
        command_args = line.split(' ')
        if command_args[0] == 'dir':
            # Make new node - add it here
            new_dir = FileTreeNode(command_args[1], NODE_LOOKUP[PWD])
            new_dir.
            # This is tricky - I'm gonna finish it later tonight after work
        else:
            pass

    if line_is_commmand:
        command_args = line[2:].split(' ')
        print(f'COMMAND {command_args}')

        command = command_args[0]

        if command == 'cd':
            dest = command_args[1]
            if dest == '..':
                # TODO : Check if current node has a parent.  Raise exception if it does not
                dest = NODE_LOOKUP[PWD]
                if not dest:
                    raise Exception(f'Could not find parent for {PWD}')
            else:
                PWD = dest
        elif command == 'ls':
            executing_ls = True
