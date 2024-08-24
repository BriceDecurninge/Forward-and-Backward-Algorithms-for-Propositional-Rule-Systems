"""
AND-OR Graph Construction, Visualization, and Data Extraction Script

This Python script is designed to construct, visualize, and extract data from an AND-OR graph,
which is a type of decision tree commonly used in problem-solving and logic programming.
The script offers the ability to create both acyclic and cyclic AND-OR graphs, extract logical
rules and deducible base facts from these graphs, and save the resulting data in a JSON format.
Additionally, the script can visualize the constructed AND-OR graph and save it as a PNG image.

Usage:
------
To run the script, use the following command in your terminal:

    python3 and_or_graph.py <number_of_rules> <max_antecedents_per_rule> <output_filename>

Where:
- `<number_of_rules>`: Specifies the number of rules to generate in the AND-OR graph.
- `<max_antecedents_per_rule>`: Sets the maximum number of antecedents (variables) in each rule.
- `<output_filename>`: The base name for the output files (JSON and PNG).

"""

import random
import matplotlib.pyplot as plt
import networkx as nx
import copy
import python.classes_json as classes_json
import json
import sys
import os

class GraphNode:
    """
    Represents a node in an AND-OR graph. 
    Each node has a value and a list of children, which are organized into disjunctions.
    """
    def __init__(self, value):
        self.value = value
        self.children = []
        self.rule_count = 0

    def add_conjunction(self, child_node, rule_index):
        """
        Adds a child node under a specific rule (conjunction) in the AND-OR graph.
        
        Parameters:
        child_node (GraphNode): The child node to add.
        rule_index (int): The index of the rule to which the child will be added.
        """
        if rule_index < 0 or rule_index >= self.rule_count:
            print("Rule not found, choose correct index")
            return
        self.children[rule_index].append(child_node)

    def add_disjunction(self, child_node):
        """
        Adds a new disjunction (rule) with a single child node to the AND-OR graph.
        
        Parameters:
        child_node (GraphNode): The child node to add as a new disjunction.
        """
        self.children.append([child_node])
        self.rule_count += 1


class Queue:
    """
    A simple Queue implementation using a list, supporting basic enqueue, dequeue, and checking if empty.
    """
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """
        Adds an item to the end of the queue.
        
        Parameters:
        item: The item to be added to the queue.
        """
        self.items.append(item)

    def dequeue(self):
        """
        Removes and returns the item at the front of the queue.
        
        Returns:
        The item at the front of the queue.
        
        Raises:
        IndexError: If the queue is empty.
        """
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("Queue is empty")

    def is_empty(self):
        """
        Checks if the queue is empty.
        
        Returns:
        bool: True if the queue is empty, False otherwise.
        """
        return len(self.items) == 0


class NameGenerator:
    """
    Generates unique names in the format A1, A2, ..., Z20.
    """
    def __init__(self, n):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.counter = 0
        self.n = n  # number of variables with the same letter: A1...An

    def generate_name(self):
        """
        Generates a unique name based on the current counter value.
        
        Returns:
        str: The generated name.
        """
        letter_index = self.counter // self.n
        number_index = self.counter % self.n
        name = self.alphabet[letter_index] + str(number_index + 1)
        self.counter += 1
        return name


def construct_and_or_graph(rule_count, length_r):
    """
    Constructs a random AND-OR graph with a specified number of rules and length of each rule.
    
    Parameters:
    rule_count (int): The total number of rules to create in the graph.
    length_r (int): The maximum length of each rule (number of variables).
    
    Returns:
    GraphNode: The root node of the constructed AND-OR graph.
    """
    name_gen = NameGenerator(20)
    nr = 0  # number of rules that have been created
    q = Queue()
    root = GraphNode("Q")
    q.enqueue(root)

    while not q.is_empty() and nr < rule_count:
        node = q.dequeue()
        nbr_node = random.randint(1, rule_count // 4)  # number of rules for node

        if nbr_node > rule_count - nr:
            nbr_node = rule_count - nr

        for i in range(nbr_node):
            rule = []
            nbr_var = random.randint(1, length_r)  # number of variables in the rule
            for j in range(nbr_var):
                p_node = GraphNode(name_gen.generate_name())
                rule.append(p_node)
                q.enqueue(p_node)
            node.children.append(rule)  # add the rule
            nr += 1

    return root


def construct_cyclic_and_or_graph(rule_count, length_r):
    """
    Constructs a random AND-OR graph with cycles.
    
    Parameters:
    rule_count (int): The total number of rules to create in the graph.
    length_r (int): The maximum length of each rule (number of variables).
    
    Returns:
    GraphNode: The root node of the constructed cyclic AND-OR graph.
    """
    name_gen = NameGenerator(20)
    nr = 0  # number of rules that have been created
    q = Queue()
    root = GraphNode("Q")
    q.enqueue(root)
    all_nodes = [root]

    while not q.is_empty() and nr < rule_count:
        node = q.dequeue()
        nbr_node = random.randint(1, rule_count // 4)

        if nbr_node > rule_count - nr:
            nbr_node = rule_count - nr

        for i in range(nbr_node):
            rule = []
            nbr_var = random.randint(1, length_r)

            for j in range(nbr_var):
                if random.random() < 0.4 and len(all_nodes) > 1:
                    p_node = random.choice(all_nodes)
                    while p_node == node:
                        p_node = random.choice(all_nodes)
                else:
                    p_node = GraphNode(name_gen.generate_name())
                    all_nodes.append(p_node)
                    q.enqueue(p_node)
                rule.append(p_node)
            node.children.append(rule)
            nr += 1

    return root


def extract_rules(root, rules):
    """
    Extracts rules from the AND-OR graph and adds them to the provided list.
    
    Parameters:
    root (GraphNode): The root node of the AND-OR graph.
    rules (list): A list to store the extracted rules.
    
    Returns:
    list: The list of extracted rules.
    """
    q = Queue()
    q.enqueue(root)
    visited = set()

    while not q.is_empty():
        node = q.dequeue()
        if node.value in visited:
            continue
        visited.add(node.value)

        head = node.value
        cons = classes_json.Variable(head, True)

        for rule in node.children:
            ant = []
            for variable in rule:
                ant.append(classes_json.Variable(variable.value, True))
                q.enqueue(variable)
            rules.append(classes_json.Rule(ant, cons))

    return rules


def print_and_or_graph(root):
    """
    Recursively prints the structure of the AND-OR graph.
    
    Parameters:
    root (GraphNode): The root node of the AND-OR graph.
    """
    print(root.value)
    if not root.children:
        return
    for rule in root.children:
        for variable in rule:
            print_and_or_graph(variable)


def draw_and_or_graph(root, output_filename):
    """
    Draws the AND-OR graph using Matplotlib and NetworkX, and saves it as a PNG file.
    
    Parameters:
    root (GraphNode): The root node of the AND-OR graph.
    output_filename (str): The filename (with path) to save the graph image as PNG.
    """
    G = nx.DiGraph()

    rule_colors = {
        "rule1": "blue",
        "rule2": "red",
        "rule3": "green",
        "rule4": "orange",
        "rule5": "purple"
    }

    def add_edges(node, visited):
        if node.value in visited:
            return
        visited.add(node.value)

        for rule_index, rule in enumerate(node.children):
            rule_color = rule_colors.get(f"rule{rule_index + 1}", "black")
            for child in rule:
                if child.value not in visited:
                    G.add_edge(node.value, child.value, color=rule_color)
                    add_edges(child, visited.copy())

    visited = set()
    add_edges(root, visited)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=900)
    for u, v, edge_attr in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=edge_attr['color'], arrows=True, arrowsize=30)
    nx.draw_networkx_labels(G, pos)

    plt.axis('off')
    plt.savefig(output_filename)
    plt.show()


def construct_bf_deducible2(root, bf, visited=None):
    """
    Constructs a list of deducible base facts (BF) from the AND-OR graph.
    
    Parameters:
    root (GraphNode): The root node of the AND-OR graph.
    bf (list): A list to store the deducible base facts.
    visited (set): A set to track visited nodes (used to avoid cycles).
    
    Returns:
    list: The list of deducible base facts.
    """
    if visited is None:
        visited = set()

    if root.value in visited:
        return bf

    visited.add(root.value)

    if not root.children:
        bf.append(classes_json.Variable(root.value, True))
        
    else:
        rule = root.children[0]
        for variable in rule:
            construct_bf_deducible(variable, bf, visited)

    return bf

def construct_bf_deducible(root, bf, visited=None, stack=None, question=None):
    """
    Constructs a list of deducible base facts (BF) from the AND-OR graph, handling cycles,
    and prioritizing alternative facts over the question itself.

    Parameters:
    root (GraphNode): The root node of the AND-OR graph.
    bf (list): A list to store the deducible base facts.
    visited (set): A set to track visited nodes (used to avoid cycles).
    stack (set): A set to track the current path (used to detect cycles).
    question (str): The question being deduced; avoid using this as a base fact if possible.

    Returns:
    list: The list of deducible base facts.
    """
    if visited is None:
        visited = set()
    if stack is None:
        stack = set()

    if root.value in visited:
        return bf

    # Detect a cycle
    if root.value in stack:
        if not bf and root.value != question:
            bf.append(classes_json.Variable(root.value, True))
        return bf

    stack.add(root.value)

    if not root.children:
        if root.value != question:
            bf.append(classes_json.Variable(root.value, True))
    else:
        for rule in root.children:
            for variable in rule:
                # Recursively try to deduce from children
                construct_bf_deducible(variable, bf, visited, stack, question)

    stack.remove(root.value)
    visited.add(root.value)

    # After exploring all children, if no facts were added and this is not the question itself
    if not bf and root.value != question:
        bf.append(classes_json.Variable(root.value, True))

    return bf



def find_all_bf_deducible(root, bf):
    """
    Recursively finds all deducible base facts (BF) from the AND-OR graph.
    
    Parameters:
    root (GraphNode): The root node of the AND-OR graph.
    bf (list): A list to store the deducible base facts.
    """
    if not root.children:
        bf.append(root.value)
    else:
        for rule in root.children:
            L = copy.copy(bf)
            for variable in rule:
                find_all_bf_deducible(variable, L)


def remove_whitespace(s):
    """
    Removes all whitespace from the provided string.
    
    Parameters:
    s (str): The string from which to remove whitespace.
    
    Returns:
    str: The string without whitespace.
    """
    return ''.join(s.split())

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 and_or_graph.py <number_of_rules> <max_antecedents_per_rule> <output_filename>")
        sys.exit(1)

    number_of_rules = int(sys.argv[1])
    max_antecedents_per_rule = int(sys.argv[2])
    output_filename = sys.argv[3]

    # Set the output directory
    output_folder = "../json_andor/"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Prepare full paths for JSON and PNG files
    json_output_path = os.path.join(output_folder, output_filename + '.json')
    png_output_path = os.path.join(output_folder, output_filename + '.png')

    r = []
    root = construct_cyclic_and_or_graph(number_of_rules, max_antecedents_per_rule)

    rules = extract_rules(root, r)
    bf = []
    bf = construct_bf_deducible(root, bf)

    br = []
    bf_list = []
    q = ""

    for rule in rules:
        rule_name = remove_whitespace(rule.name)
        br.append(rule_name)

    for fact in bf:
        fact_name = remove_whitespace(fact.name)
        bf_list.append(fact_name)

    q = classes_json.Variable("Q", True).name

    json_data = {
        "base_of_rules": br,
        "base_of_facts": bf_list,
        "question": q
    }

    # Save JSON file
    with open(json_output_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    print(f"JSON file '{json_output_path}' created successfully.")

    # Save the AND-OR graph as PNG
    draw_and_or_graph(root, png_output_path)
    print(f"PNG file '{png_output_path}' created successfully.")