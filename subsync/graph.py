import gizmo
import pydot
import os

import logging
logger = logging.getLogger(__name__)


_initialized = False

def init():
    global _initialized
    if _initialized:
        return

    def addOutputsGetter(type):
        def getter(self):
            if hasattr(self, '_connectedOutputs'):
                return self._connectedOutputs
            else:
                return []
        setattr(type, 'getConnectedOutputs', getter)


    def addCallbackWrapper(type, methodName, edgeName):
        orgCb = getattr(type, methodName)

        def wrapper(self, cb, dst=None):
            if not hasattr(self, '_connectedOutputs'):
                self._connectedOutputs = []

            if cb:
                if hasattr(cb, '__func__') and hasattr(cb.__func__, '__name__'):
                    name = cb.__func__.__name__
                    self._connectedOutputs.append((edgeName, dst, name))
                else:
                    self._connectedOutputs.append((edgeName, dst))

            else:
                for out in self._connectedOutputs:
                    if out[0] == edgeName:
                        self._connectedOutputs.remove(out)
                        break

            orgCb(self, cb)

        setattr(type, methodName, wrapper)

    addOutputsGetter(gizmo.SubtitleDec)
    addCallbackWrapper(gizmo.SubtitleDec, 'connectWordsCallback', 'words')
    addCallbackWrapper(gizmo.SubtitleDec, 'connectSubsCallback', 'subtitles')

    addOutputsGetter(gizmo.SpeechRecognition)
    addCallbackWrapper(gizmo.SpeechRecognition, 'connectWordsCallback', 'words')

    addOutputsGetter(gizmo.Translator)
    addCallbackWrapper(gizmo.Translator, 'connectWordsCallback', 'words')

    _initialized = True


def drawNode(graph, node, names={}):
    srcName = getNodeName(graph, node, names)

    if hasattr(node, 'getConnectedOutputs'):
        outputs = node.getConnectedOutputs()
        for output in outputs:
            dst = output[1]
            newDst = dst not in names
            dstName = getNodeName(graph, dst, names)

            labels = {}
            if output[0]:
                labels['label'] = output[0]
            if len(output) >= 3 and output[2]:
                labels['headlabel'] = output[2]

            graph.add_edge(pydot.Edge(srcName, dstName, **labels))

            if newDst:
                drawNode(graph, dst, names)


def getNodeName(graph, node, names={}):
    if node not in names:
        i = 0
        prefix = node.__class__.__name__
        while True:
            name = prefix + str(i)
            if name not in names.values():
                names[node] = name
                graph.add_node(pydot.Node(name))
                return name
            i += 1
    return names[node]


def saveGraph(path, nodes, format=None):
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')
    graph.set_node_defaults(shape='box')

    for node in nodes:
        drawNode(graph, node)

    if format == None:
        format = os.path.splitext(path)[1][1:]
        if format == 'dot':
            format = 'raw'

    logger.info('saving pipeline graph to %s', path)
    graph.write(path, format=format)

