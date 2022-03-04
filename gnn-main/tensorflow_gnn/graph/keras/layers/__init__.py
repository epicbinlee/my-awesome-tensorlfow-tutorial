"""The tfgnn.keras.layers package."""

from tensorflow_gnn.graph.keras.layers import convolutions
from tensorflow_gnn.graph.keras.layers import gat_v2
from tensorflow_gnn.graph.keras.layers import graph_ops
from tensorflow_gnn.graph.keras.layers import graph_update
from tensorflow_gnn.graph.keras.layers import map_features
from tensorflow_gnn.graph.keras.layers import next_state
from tensorflow_gnn.graph.keras.layers import parse_example

ParseExample = parse_example.ParseExample
ParseSingleExample = parse_example.ParseSingleExample

MapFeatures = map_features.MapFeatures
TotalSize = map_features.TotalSize

Broadcast = graph_ops.Broadcast
Pool = graph_ops.Pool
Readout = graph_ops.Readout
ReadoutFirstNode = graph_ops.ReadoutFirstNode

ConvolutionFromEdgeSetUpdate = convolutions.ConvolutionFromEdgeSetUpdate
SimpleConvolution = convolutions.SimpleConvolution

NextStateFromConcat = next_state.NextStateFromConcat
ResidualNextState = next_state.ResidualNextState

EdgeSetUpdate = graph_update.EdgeSetUpdate
NodeSetUpdate = graph_update.NodeSetUpdate
ContextUpdate = graph_update.ContextUpdate
GraphUpdate = graph_update.GraphUpdate

GATv2Convolution = gat_v2.GATv2Convolution
GATv2EdgePool = gat_v2.GATv2EdgePool
GATv2GraphUpdate = gat_v2.GATv2GraphUpdate

# Prune imported module symbols so they're not accessible implicitly.
del convolutions
del graph_ops
del graph_update
del map_features
del next_state
del parse_example
del gat_v2
