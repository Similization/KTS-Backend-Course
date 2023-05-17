from typing import Any

__all__ = (
    'Node',
    'Graph'
)


class Node:
    def __init__(self, value: Any):
        self.value = value

        self.outbound = []
        self.inbound = []

    def point_to(self, other: 'Node'):
        self.outbound.append(other)
        other.inbound.append(self)

    def __str__(self):
        return f'Node({repr(self.value)})'

    __repr__ = __str__


class Graph:
    def __init__(self, root: Node):
        self._root = root

    def dfs(self) -> list[Node]:
        result = [self._root]
        queue: list[Node] = self._root.outbound
        while len(queue) != 0:
            if queue[0] not in result:
                result.append(queue[0])
            nodes = queue[0].outbound
            queue.remove(queue[0])
            if nodes:
                queue = nodes + queue
        return result

    def bfs(self) -> list[Node]:
        result = [self._root]
        queue: list[Node] = self._root.outbound[:]
        visited = []
        while len(queue) != 0:
            if queue[0] not in result:
                result.append(queue[0])
            nodes = queue[0].outbound
            visited.append(queue[0])
            queue.remove(queue[0])
            if nodes:
                queue = queue + nodes
            queue = [el for el in queue if el not in visited]
        return result
