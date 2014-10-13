from os import path
import re
import tree

def parse(fname):
    data = []
    with open(fname, 'r') as f:
        for line in f:
            data.append(line)
    data = map(lambda x: x.strip(), data)
    data = filter(lambda x: not x.startswith('-'), data)
    opening_pairs = []
    current_opening = []
    for line in data:
        if re.match('^[A-E][\d]+', line):
            if current_opening:
                opening_pairs.append(current_opening)
            current_opening = [line]
        elif line.startswith("("):
            current_opening[-1] += " " + line
        elif len(current_opening) == 1:
            current_opening.append(line)
        elif current_opening:
            current_opening[-1] += " " + line
    opening_pairs.append(current_opening)
    openings = []
    for opening in opening_pairs:
        assert opening[1].startswith("1.")
        code, name = opening[0].split(" ", 1)
        openings.append(tree.Opening(code, name, opening[1][2:].split()))
    return openings

def make_tree(openings):
    root = tree.EcoNode()
    for opening in openings:
        root.insert(opening)
    return root

def load_default():
    openings = parse(path.join(path.dirname(__file__), "eco.raw"))
    tree = make_tree(openings)
    return tree

if __name__ == '__main__':
    import pprint
    tree = load_default()
    pprint.pprint(tree.all_submoves())
