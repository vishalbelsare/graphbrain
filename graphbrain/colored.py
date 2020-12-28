from termcolor import colored


TYPE_COLOR = {
    'C': 'blue',
    'P': 'red',
    'M': 'cyan',
    'B': 'green',
    'J': 'yellow',
    'T': 'magenta'
}


def colored_type(atom_type):
    if atom_type[0] in TYPE_COLOR:
        color = TYPE_COLOR[atom_type[0]]
        return colored(atom_type, color)
    else:
        return atom_type


def with_type_color(atom_type, text):
    if atom_type[0] in TYPE_COLOR:
        color = TYPE_COLOR[atom_type[0]]
        return colored(text, color)
    else:
        return text


def colored_role(atom):
    role = atom.role()
    crole = [colored_type(atom.type())]
    crole += role[1:]
    return '.'.join(crole)


def colored_atom(atom):
    parts = [with_type_color(atom.type(), atom.root()), colored_role(atom)]
    parts += atom.parts()[2:]
    return '/'.join(parts)


def colored_edge(edge):
    if edge is None:
        return None
    elif edge.is_atom():
        return colored_atom(edge)
    else:
        return '({})'.format(
            ' '.join([colored_edge(subedge) for subedge in edge]))


def colored_diff(edge1, edge2):
    if ((edge1.is_atom() != edge2.is_atom()) or
            (len(edge1) != len(edge2)) or
            (edge1.is_atom() and (edge1 != edge2))):
        dedge1 = colored(edge1.to_str(), 'red')
        dedge2 = colored(edge2.to_str(), 'red')
        return True, dedge1, dedge2

    if edge1.is_atom():
        return False, edge1.to_str(), edge2.to_str()

    dedge1 = []
    dedge2 = []
    diff = True
    for sedge1, sedge2 in zip(edge1, edge2):
        sdiff, dsedge1, dsedge2 = colored_diff(sedge1, sedge2)
        dedge1.append(dsedge1)
        dedge2.append(dsedge2)
        diff &= sdiff
    opar = colored('(', 'red') if diff else '('
    cpar = colored(')', 'red') if diff else ')'
    dedge1 = '{}{}{}'.format(opar, ' '.join(dedge1), cpar)
    dedge2 = '{}{}{}'.format(opar, ' '.join(dedge2), cpar)
    return False, dedge1, dedge2
