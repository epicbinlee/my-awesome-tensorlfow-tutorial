// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/framework/dataset_options.proto

package org.tensorflow.proto.data;

public interface AutotuneOptionsOrBuilder extends
    // @@protoc_insertion_point(interface_extends:tensorflow.data.AutotuneOptions)
    com.google.protobuf.MessageOrBuilder {

  /**
   * <code>bool enabled = 1;</code>
   */
  boolean getEnabled();

  /**
   * <code>int32 cpu_budget = 2;</code>
   */
  int getCpuBudget();

  /**
   * <code>int64 ram_budget = 3;</code>
   */
  long getRamBudget();

  public org.tensorflow.proto.data.AutotuneOptions.OptionalEnabledCase getOptionalEnabledCase();

  public org.tensorflow.proto.data.AutotuneOptions.OptionalCpuBudgetCase getOptionalCpuBudgetCase();

  public org.tensorflow.proto.data.AutotuneOptions.OptionalRamBudgetCase getOptionalRamBudgetCase();
}