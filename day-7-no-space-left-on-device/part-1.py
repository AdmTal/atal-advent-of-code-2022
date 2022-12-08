system_output_lines = open('./input.txt').read().split('\n')


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
            self._parent.increase_size(more)

    @property
    def size(self):
        return self._size

    def print(self, level=0):
        marker = level * '    '
        xxx = self._name if self._name else '~'
        print(f'{marker}{xxx}  (size={self._size})')
        for child in self._files.values():
            print(f'{marker}{child}')
        for child in self._children.values():
            child.print(level + 1)


FILE_TREE_ROOT = FileTreeNode('~')
NODE_LOOKUP = {
    '~': FILE_TREE_ROOT,
}

executing_ls = False
PWD = '~'

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
                PWD = '~'
            else:
                PWD = f'{PWD}/{dest}'

        elif command == 'ls':
            executing_ls = True

    elif executing_ls:
        parent = NODE_LOOKUP[PWD]
        command_args = line.split(' ')
        if command_args[0] == 'dir':
            child_name = f'{parent.name}/{command_args[1]}'
            child = FileTreeNode(child_name, parent)
            parent.add_child(child.name, child)
            NODE_LOOKUP[child.name] = child
        else:
            size, filename = command_args
            parent.increase_size(int(size))

# FILE_TREE_ROOT.print()

print(
    sum(
        [i.size for i in NODE_LOOKUP.values() if i.size <= 100000]
    )
)
