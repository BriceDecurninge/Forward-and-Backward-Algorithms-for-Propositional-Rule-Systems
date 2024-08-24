'''Description : This file provides multiple functions that draws graphs for conception purposes
'''

import graphviz
import os
import objgraph


relative_path = "compare/"
data_path = os.path.join(os.getcwd(), relative_path)



def draw_benchmark_load() :
    

    # Create a new directed graph
    dot = graphviz.Digraph(comment='Function Call Graph for data loading part')

    # Define node colors based on modules
    colors = {
        "load_data": "lightcoral",  # Red
        "classes": "lightblue"      # Blue
    }

    # Add nodes with colors
    dot.node('load_benchmark', 'load_benchmark\n', style='filled', fillcolor=colors["load_data"])
    dot.node('create_set', 'create_set\n', style='filled', fillcolor=colors["classes"])
    dot.node('list_to_rule', 'list_to_rule\n', style='filled', fillcolor=colors["classes"])
    dot.node('create_fb_object', 'create_fb_object\n', style='filled', fillcolor=colors["classes"])
    dot.node('create_q_object', 'create_q_object\n', style='filled', fillcolor=colors["classes"])
    dot.node('parse_rule', 'parse_rule\n', style='filled', fillcolor=colors["classes"])
    dot.node('create_ant_object', 'create_ant_object\n', style='filled', fillcolor=colors["classes"])
    dot.node('parse_connector', 'parse_connector\n', style='filled', fillcolor=colors["classes"])
    dot.node('create_csq_object', 'create_csq_object\n', style='filled', fillcolor=colors["classes"])

    # Add edges to represent function calls
    dot.edge('load_benchmark', 'create_set')
    dot.edge('create_set', 'list_to_rule')
    dot.edge('create_set', 'create_fb_object')
    dot.edge('create_set', 'create_q_object')
    dot.edge('list_to_rule', 'parse_rule')
    dot.edge('list_to_rule', 'create_ant_object')
    dot.edge('list_to_rule', 'parse_connector')
    dot.edge('list_to_rule', 'create_csq_object')

    # Add legend
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(style='filled', color='lightgrey')
        c.node_attr.update(style='filled')
        c.node('load_data_module', 'load_data module', fillcolor='lightcoral')
        c.node('classes_module', 'classes module', fillcolor='lightblue')
        c.attr(label='Legend')

    # Save and render the graph
    dot.render('data_loading_graph', format='png', view=True)

    
    '''
    # Create a new directed graph
    
    dot = graphviz.Digraph(comment='Load Data Graph')

    # Define the nodes (functions) with colors for different modules
    dot.node('A', 'load_benchmark\n', style='filled', fillcolor='lightcoral')
    dot.node('B', 'create_set\n', style='filled', fillcolor='lightblue')
    dot.node('C', 'list_to_rule\n', style='filled', fillcolor='lightblue')
    dot.node('D', 'create_fb_object\n', style='filled', fillcolor='lightblue')
    dot.node('E', 'create_q_object\n', style='filled', fillcolor='lightblue')

    # Define the edges (function calls)
    dot.edge('A', 'B', label='calls')
    dot.edge('B', 'C', label='calls')
    dot.edge('B', 'D', label='calls')
    dot.edge('B', 'E', label='calls')

    # Add a legend
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Legend', style='filled', color='lightgrey', fontsize='20')
        c.node('L1', 'load_data module', style='filled', fillcolor='lightcoral')
        c.node('L2', 'classes module', style='filled', fillcolor='lightblue')
        c.edge('L1', 'L2', style='invis')

    # Render and display the graph
    dot.render('function_call_graph_with_legend', format='png', view=True)

    '''
    
    
def draw_benchmark_creation():

    # Create a new directed graph
    dot = graphviz.Digraph(comment='Function Call Graph')

    # Define the nodes (functions) with colors for different modules
    dot.node('A', 'create_benchmark\n', style='filled', fillcolor='lightblue')
    dot.node('B', 'generate_benchmark\n', style='filled', fillcolor='lightgreen')
    dot.node('C', 'generate_rules_benchmark\n', style='filled', fillcolor='lightgreen')
    dot.node('D', 'generate_fb_benchmark\n', style='filled', fillcolor='lightgreen')

    # Define the edges (function calls)
    dot.edge('A', 'B', label='calls')
    dot.edge('B', 'C', label='calls')
    dot.edge('B', 'D', label='calls')

    # Add a legend
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Legend', style='filled', color='lightgrey', fontsize='20')
        c.node('L1', 'benchmark module', style='filled', fillcolor='lightblue')
        c.node('L2', 'generate_data module', style='filled', fillcolor='lightgreen')
        c.edge('L1', 'L2', style='invis')

    # Render and display the graph
    dot.render('benchmark_creation_graph', format='png', view=True)



'''Descritpion : Creates the graph object of a variable and a rule'''
def create_graph_objects(facts_base, rules):

    for rule in rules :
        for antecedent in rule.antecedents :
            rule.counter += 1
            antecedent.addRule(rule)
    for variable in facts_base :
        variable.value=True

    
    output_path = data_path + "/object_graph.png"

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Visualize object references
    
    #objgraph.show_refs([facts_base[0]], filename=output_path)
    objgraph.show_refs([rules[0]], filename=output_path, max_depth=3, refcounts=True, extra_info=lambda x: "size: {}".format(sys.getsizeof(x)))



if __name__ == "__main__":
    draw_benchmark_load()
    