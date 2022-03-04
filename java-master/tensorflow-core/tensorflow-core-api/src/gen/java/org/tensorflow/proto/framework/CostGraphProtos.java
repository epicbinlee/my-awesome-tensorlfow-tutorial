// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/framework/cost_graph.proto

package org.tensorflow.proto.framework;

public final class CostGraphProtos {
  private CostGraphProtos() {}
  public static void registerAllExtensions(
      com.google.protobuf.ExtensionRegistryLite registry) {
  }

  public static void registerAllExtensions(
      com.google.protobuf.ExtensionRegistry registry) {
    registerAllExtensions(
        (com.google.protobuf.ExtensionRegistryLite) registry);
  }
  static final com.google.protobuf.Descriptors.Descriptor
    internal_static_tensorflow_CostGraphDef_descriptor;
  static final 
    com.google.protobuf.GeneratedMessageV3.FieldAccessorTable
      internal_static_tensorflow_CostGraphDef_fieldAccessorTable;
  static final com.google.protobuf.Descriptors.Descriptor
    internal_static_tensorflow_CostGraphDef_Node_descriptor;
  static final 
    com.google.protobuf.GeneratedMessageV3.FieldAccessorTable
      internal_static_tensorflow_CostGraphDef_Node_fieldAccessorTable;
  static final com.google.protobuf.Descriptors.Descriptor
    internal_static_tensorflow_CostGraphDef_Node_InputInfo_descriptor;
  static final 
    com.google.protobuf.GeneratedMessageV3.FieldAccessorTable
      internal_static_tensorflow_CostGraphDef_Node_InputInfo_fieldAccessorTable;
  static final com.google.protobuf.Descriptors.Descriptor
    internal_static_tensorflow_CostGraphDef_Node_OutputInfo_descriptor;
  static final 
    com.google.protobuf.GeneratedMessageV3.FieldAccessorTable
      internal_static_tensorflow_CostGraphDef_Node_OutputInfo_fieldAccessorTable;
  static final com.google.protobuf.Descriptors.Descriptor
    internal_static_tensorflow_CostGraphDef_AggregatedCost_descriptor;
  static final 
    com.google.protobuf.GeneratedMessageV3.FieldAccessorTable
      internal_static_tensorflow_CostGraphDef_AggregatedCost_fieldAccessorTable;

  public static com.google.protobuf.Descriptors.FileDescriptor
      getDescriptor() {
    return descriptor;
  }
  private static  com.google.protobuf.Descriptors.FileDescriptor
      descriptor;
  static {
    java.lang.String[] descriptorData = {
      "\n*tensorflow/core/framework/cost_graph.p" +
      "roto\022\ntensorflow\032,tensorflow/core/framew" +
      "ork/tensor_shape.proto\032%tensorflow/core/" +
      "framework/types.proto\"\312\006\n\014CostGraphDef\022+" +
      "\n\004node\030\001 \003(\0132\035.tensorflow.CostGraphDef.N" +
      "ode\0225\n\004cost\030\002 \003(\0132\'.tensorflow.CostGraph" +
      "Def.AggregatedCost\032\242\005\n\004Node\022\014\n\004name\030\001 \001(" +
      "\t\022\016\n\006device\030\002 \001(\t\022\n\n\002id\030\003 \001(\005\022;\n\ninput_i" +
      "nfo\030\004 \003(\0132\'.tensorflow.CostGraphDef.Node" +
      ".InputInfo\022=\n\013output_info\030\005 \003(\0132(.tensor" +
      "flow.CostGraphDef.Node.OutputInfo\022\035\n\025tem" +
      "porary_memory_size\030\006 \001(\003\022\036\n\026persistent_m" +
      "emory_size\030\014 \001(\003\022!\n\025host_temp_memory_siz" +
      "e\030\n \001(\003B\002\030\001\022#\n\027device_temp_memory_size\030\013" +
      " \001(\003B\002\030\001\022)\n\035device_persistent_memory_siz" +
      "e\030\020 \001(\003B\002\030\001\022\024\n\014compute_cost\030\t \001(\003\022\024\n\014com" +
      "pute_time\030\016 \001(\003\022\023\n\013memory_time\030\017 \001(\003\022\020\n\010" +
      "is_final\030\007 \001(\010\022\025\n\rcontrol_input\030\010 \003(\005\022\022\n" +
      "\ninaccurate\030\021 \001(\010\032;\n\tInputInfo\022\026\n\016preced" +
      "ing_node\030\001 \001(\005\022\026\n\016preceding_port\030\002 \001(\005\032\206" +
      "\001\n\nOutputInfo\022\014\n\004size\030\001 \001(\003\022\030\n\020alias_inp" +
      "ut_port\030\002 \001(\003\022+\n\005shape\030\003 \001(\0132\034.tensorflo" +
      "w.TensorShapeProto\022#\n\005dtype\030\004 \001(\0162\024.tens" +
      "orflow.DataType\0321\n\016AggregatedCost\022\014\n\004cos" +
      "t\030\001 \001(\002\022\021\n\tdimension\030\002 \001(\tB\211\001\n\036org.tenso" +
      "rflow.proto.frameworkB\017CostGraphProtosP\001" +
      "ZQgithub.com/tensorflow/tensorflow/tenso" +
      "rflow/go/core/framework/cost_graph_go_pr" +
      "oto\370\001\001b\006proto3"
    };
    descriptor = com.google.protobuf.Descriptors.FileDescriptor
      .internalBuildGeneratedFileFrom(descriptorData,
        new com.google.protobuf.Descriptors.FileDescriptor[] {
          org.tensorflow.proto.framework.TensorShapeProtos.getDescriptor(),
          org.tensorflow.proto.framework.TypesProtos.getDescriptor(),
        });
    internal_static_tensorflow_CostGraphDef_descriptor =
      getDescriptor().getMessageTypes().get(0);
    internal_static_tensorflow_CostGraphDef_fieldAccessorTable = new
      com.google.protobuf.GeneratedMessageV3.FieldAccessorTable(
        internal_static_tensorflow_CostGraphDef_descriptor,
        new java.lang.String[] { "Node", "Cost", });
    internal_static_tensorflow_CostGraphDef_Node_descriptor =
      internal_static_tensorflow_CostGraphDef_descriptor.getNestedTypes().get(0);
    internal_static_tensorflow_CostGraphDef_Node_fieldAccessorTable = new
      com.google.protobuf.GeneratedMessageV3.FieldAccessorTable(
        internal_static_tensorflow_CostGraphDef_Node_descriptor,
        new java.lang.String[] { "Name", "Device", "Id", "InputInfo", "OutputInfo", "TemporaryMemorySize", "PersistentMemorySize", "HostTempMemorySize", "DeviceTempMemorySize", "DevicePersistentMemorySize", "ComputeCost", "ComputeTime", "MemoryTime", "IsFinal", "ControlInput", "Inaccurate", });
    internal_static_tensorflow_CostGraphDef_Node_InputInfo_descriptor =
      internal_static_tensorflow_CostGraphDef_Node_descriptor.getNestedTypes().get(0);
    internal_static_tensorflow_CostGraphDef_Node_InputInfo_fieldAccessorTable = new
      com.google.protobuf.GeneratedMessageV3.FieldAccessorTable(
        internal_static_tensorflow_CostGraphDef_Node_InputInfo_descriptor,
        new java.lang.String[] { "PrecedingNode", "PrecedingPort", });
    internal_static_tensorflow_CostGraphDef_Node_OutputInfo_descriptor =
      internal_static_tensorflow_CostGraphDef_Node_descriptor.getNestedTypes().get(1);
    internal_static_tensorflow_CostGraphDef_Node_OutputInfo_fieldAccessorTable = new
      com.google.protobuf.GeneratedMessageV3.FieldAccessorTable(
        internal_static_tensorflow_CostGraphDef_Node_OutputInfo_descriptor,
        new java.lang.String[] { "Size", "AliasInputPort", "Shape", "Dtype", });
    internal_static_tensorflow_CostGraphDef_AggregatedCost_descriptor =
      internal_static_tensorflow_CostGraphDef_descriptor.getNestedTypes().get(1);
    internal_static_tensorflow_CostGraphDef_AggregatedCost_fieldAccessorTable = new
      com.google.protobuf.GeneratedMessageV3.FieldAccessorTable(
        internal_static_tensorflow_CostGraphDef_AggregatedCost_descriptor,
        new java.lang.String[] { "Cost", "Dimension", });
    org.tensorflow.proto.framework.TensorShapeProtos.getDescriptor();
    org.tensorflow.proto.framework.TypesProtos.getDescriptor();
  }

  // @@protoc_insertion_point(outer_class_scope)
}