system_output_lines = open('./example-input.txt').read().split('\n')


class FileTreeNode(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._size = 0
        self._parent = parent
        self._children = {}

    @property
    def name(self):
        return self._name

    def add_child(self, name, value):
        self._children[name] = value

    def increase_size(self, more):
        self._size += more
        if self._parent:
            self._parent.increase_size(self._size)

    @property
    def size(self):
        return self._size


FILE_TREE_ROOT = FileTreeNode('')
PWD = FILE_TREE_ROOT.name
NODE_LOOKUP = {
    FILE_TREE_ROOT.name: FILE_TREE_ROOT,
}

for line in system_output_lines:
    this_line_is_a_command = line[0] == '$'

    if this_line_is_a_command:
        command_args = line[2:].split(' ')
        command = command_args[0]
        if command == 'cd':
            dest = command_args[1]
            if dest == '..':
                PWD = '/'.join(PWD.split('/')[:-1])
                dest = NODE_LOOKUP[PWD]
            elif dest == '/':
                PWD = ''
            else:
                PWD = f'{PWD}/{dest}'

        elif command == 'ls':
            executing_ls = True

    elif executing_ls:
        command_args = line.split(' ')
        parent = NODE_LOOKUP[PWD]
        if command_args[0] == 'dir':
            child = FileTreeNode(f'{parent.name}/{command_args[1]}', parent)
            parent.add_child(child.name, child)
            NODE_LOOKUP[child.name] = child
        else:
            size, filename = command_args
            parent.increase_size(int(size))

print(
    sum(
        [i.size for i in NODE_LOOKUP.values() if i.size <= 100_000]
    )
)
