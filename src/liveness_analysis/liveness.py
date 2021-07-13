from typing import Tuple, List

from dataclasses import dataclass

from activation_records.temp import Temp
from liveness_analysis.flow_graph import AssemblerInformation
from liveness_analysis.graph import Graph


@dataclass
class InterferenceResults:
    graph: Graph[Temp]
    move_pairs: List[Tuple[Temp, Temp]]


def liveness(
    flow_graph: Graph[AssemblerInformation],
) -> InterferenceResults:
    live_graph = Graph[Temp]()
    move_pairs = []

    temporaries = set()
    for flow_node in flow_graph.get_nodes():
        temporaries = temporaries.union(
            flow_node.information.definitions, flow_node.information.uses
        )

    temporary_to_node = {
        temporary: live_graph.add_node(temporary) for temporary in temporaries
    }

    for flow_node in flow_graph.get_nodes():
        if flow_node.information.is_move():
            if len(flow_node.information.definitions == 1):
                move_destination = flow_node.information.definitions[0]
                move_source = (
                    flow_node.information.uses[0]
                    if len(flow_node.information.uses == 1)
                    else None
                )
                for live_out_temporary in flow_node.information.live_out:
                    if live_out_temporary != move_source:
                        live_graph.add_edge(
                            temporary_to_node[move_destination],
                            temporary_to_node[live_out_temporary],
                        )
                        live_graph.add_edge(
                            temporary_to_node[live_out_temporary],
                            temporary_to_node[move_destination],
                        )
                if move_source is not None:
                    move_pairs.append((move_source, move_destination))
        else:
            for defined_temporary in flow_node.information.definitions:
                for live_out_temporary in flow_node.information.live_out:
                    live_graph.add_edge(
                        temporary_to_node[defined_temporary],
                        temporary_to_node[live_out_temporary],
                    )
                    live_graph.add_edge(
                        temporary_to_node[live_out_temporary],
                        temporary_to_node[defined_temporary],
                    )

    return InterferenceResults(live_graph, move_pairs)
