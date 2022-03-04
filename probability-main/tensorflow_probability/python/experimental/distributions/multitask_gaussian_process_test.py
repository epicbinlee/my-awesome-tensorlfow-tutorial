# Copyright 2021 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Tests for MultiTaskGaussianProcess."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Dependency imports

import numpy as np

import tensorflow.compat.v2 as tf

import tensorflow_probability as tfp
from tensorflow_probability.python import experimental as tfe
from tensorflow_probability.python.internal import test_util

tfd = tfp.distributions
tfk = tfp.math.psd_kernels


@test_util.test_all_tf_execution_regimes
class MultiTaskGaussianProcessTest(test_util.TestCase):

  def testShapes(self):
    # 5x5 grid of index points in R^2 and flatten to 25x2
    index_points = np.linspace(-4., 4., 5, dtype=np.float32)
    index_points = np.stack(np.meshgrid(index_points, index_points), axis=-1)
    index_points = np.reshape(index_points, [-1, 2])
    # ==> shape = [25, 2]

    # Kernel with batch_shape [2, 4, 3, 1]
    amplitude = np.array([1., 2.], np.float32).reshape([2, 1, 1, 1])
    length_scale = np.array([1., 2., 3., 4.], np.float32).reshape([1, 4, 1, 1])
    observation_noise_variance = np.array(
        [1e-5, 1e-6, 1e-5], np.float32).reshape([1, 1, 3, 1])
    batched_index_points = np.stack([index_points]*6)
    # ==> shape = [6, 25, 2]
    kernel = tfk.ExponentiatedQuadratic(amplitude, length_scale)
    multi_task_kernel = tfe.psd_kernels.Independent(
        num_tasks=3, base_kernel=kernel)
    gp = tfe.distributions.MultiTaskGaussianProcess(
        multi_task_kernel,
        batched_index_points,
        observation_noise_variance=observation_noise_variance,
        validate_args=True)

    batch_shape = [2, 4, 3, 6]
    event_shape = [25, 3]
    sample_shape = [5, 3]

    samples = gp.sample(sample_shape, seed=test_util.test_seed())

    self.assertAllEqual(gp.batch_shape, batch_shape)
    self.assertAllEqual(self.evaluate(gp.batch_shape_tensor()), batch_shape)
    self.assertAllEqual(gp.event_shape, event_shape)
    self.assertAllEqual(self.evaluate(gp.event_shape_tensor()), event_shape)
    self.assertAllEqual(
        self.evaluate(samples).shape,
        sample_shape + batch_shape + event_shape)
    self.assertAllEqual(
        self.evaluate(tf.shape(gp.mean())), batch_shape + event_shape)

  def testBindingIndexPoints(self):
    amplitude = np.float64(0.5)
    length_scale = np.float64(2.)
    kernel = tfk.ExponentiatedQuadratic(amplitude, length_scale)
    num_tasks = 3
    multi_task_kernel = tfe.psd_kernels.Independent(
        num_tasks=num_tasks, base_kernel=kernel)
    mean_fn = lambda x: tf.stack([x[..., 0]] * num_tasks, axis=-1)
    observation_noise_variance = np.float64(1e-3)
    mtgp = tfe.distributions.MultiTaskGaussianProcess(
        kernel=multi_task_kernel,
        mean_fn=mean_fn,
        observation_noise_variance=observation_noise_variance,
        validate_args=True)
    gp = tfd.GaussianProcess(
        kernel=kernel,
        mean_fn=lambda x: x[..., 0],
        observation_noise_variance=observation_noise_variance,
        validate_args=True)

    index_points = np.random.uniform(-1., 1., [10, 4])
    observations = np.random.uniform(-1., 1., [10, num_tasks])

    multi_task_log_prob = mtgp.log_prob(
        observations, index_points=index_points)
    single_task_log_prob = sum(
        gp.log_prob(
            observations[..., i], index_points=index_points)
        for i in range(num_tasks))
    self.assertAllClose(
        self.evaluate(single_task_log_prob),
        self.evaluate(multi_task_log_prob), rtol=4e-3)

    multi_task_mean_ = self.evaluate(mtgp.mean(index_points=index_points))
    single_task_mean_ = self.evaluate(gp.mean(index_points=index_points))
    for i in range(3):
      self.assertAllClose(
          single_task_mean_, multi_task_mean_[..., i], rtol=1e-3)

  def testConstantMeanFunction(self):
    # 5x5 grid of index points in R^2 and flatten to 25x2
    index_points = np.linspace(-4., 4., 5, dtype=np.float32)
    index_points = np.stack(np.meshgrid(index_points, index_points), axis=-1)
    index_points = np.reshape(index_points, [-1, 2])
    # ==> shape = [25, 2]

    # Kernel with batch_shape [2, 4, 3, 1]
    amplitude = np.array([1., 2.], np.float32).reshape([2, 1, 1, 1])
    length_scale = np.array([1., 2., 3., 4.], np.float32).reshape([1, 4, 1, 1])
    observation_noise_variance = np.array(
        [1e-5, 1e-6, 1e-5], np.float32).reshape([1, 1, 3, 1])
    batched_index_points = np.stack([index_points]*6)
    # ==> shape = [6, 25, 2]
    kernel = tfk.ExponentiatedQuadratic(amplitude, length_scale)
    multi_task_kernel = tfe.psd_kernels.Independent(
        num_tasks=3, base_kernel=kernel)

    mean_fn = lambda x: np.float32(0.)

    gp = tfe.distributions.MultiTaskGaussianProcess(
        multi_task_kernel,
        batched_index_points,
        mean_fn=mean_fn,
        observation_noise_variance=observation_noise_variance,
        validate_args=True)

    batch_shape = [2, 4, 3, 6]
    event_shape = [25, 3]

    self.assertAllEqual(
        self.evaluate(gp.mean()).shape,
        batch_shape + event_shape)

    mean_fn = lambda x: tf.zeros([3], dtype=tf.float32)

    gp = tfe.distributions.MultiTaskGaussianProcess(
        multi_task_kernel,
        batched_index_points,
        mean_fn=mean_fn,
        observation_noise_variance=observation_noise_variance,
        validate_args=True)

    self.assertAllEqual(
        self.evaluate(gp.mean()).shape,
        batch_shape + event_shape)

  def testLogProbMatchesGPNoiseless(self):
    # Check that the independent kernel parameterization matches using a
    # single-task GP.

    # 5x5 grid of index points in R^2 and flatten to 25x2
    index_points = np.linspace(-4., 4., 5, dtype=np.float32)
    index_points = np.stack(np.meshgrid(index_points, index_points), axis=-1)
    index_points = np.reshape(index_points, [-1, 2])
    # ==> shape = [25, 2]

    # Kernel with batch_shape [2, 4, 1, 1]
    amplitude = np.array([1., 2.], np.float32).reshape([2, 1, 1, 1])
    length_scale = np.array([1., 2., 3., 4.], np.float32).reshape([1, 4, 1, 1])
    observation_noise_variance = None
    batched_index_points = np.stack([index_points]*6)
    # ==> shape = [6, 25, 2]
    kernel = tfk.ExponentiatedQuadratic(amplitude, length_scale)
    multi_task_kernel = tfe.psd_kernels.Independent(
        num_tasks=3, base_kernel=kernel)
    multitask_gp = tfe.distributions.MultiTaskGaussianProcess(
        multi_task_kernel,
        batched_index_points,
        observation_noise_variance=observation_noise_variance,
        validate_args=True)
    gp = tfd.GaussianProcess(
        kernel,
        batched_index_points,
        observation_noise_variance=0.,
        validate_args=True)
    observations = np.linspace(-20., 20., 75).reshape(25, 3).astype(np.float32)
    multitask_log_prob = multitask_gp.log_prob(observations)
    single_task_log_prob = sum(
        gp.log_prob(observations[..., i]) for i in range(3))
    self.assertAllClose(
        self.evaluate(single_task_log_prob),
        self.evaluate(multitask_log_prob), rtol=4e-3)

  @test_util.disable_test_for_backend(
      disable_numpy=True, disable_jax=False,
      reason='Jit not available in numpy.')
  def testJitMultitaskGaussianProcess(self):
    # 5x5 grid of index points in R^2 and flatten to 25x2
    index_points = np.linspace(-4., 4., 5, dtype=np.float32)
    index_points = np.stack(np.meshgrid(index_points, index_points), axis=-1)
    index_points = np.reshape(index_points, [-1, 2])
    # ==> shape = [25, 2]

    # Kernel with batch_shape [2, 4, 3, 1]
    amplitude = np.array([1., 2.], np.float32).reshape([2, 1, 1, 1])
    length_scale = np.array([1., 2., 3., 4.], np.float32).reshape([1, 4, 1, 1])
    observation_noise_variance = np.array(
        [1e-5, 1e-6, 1e-5], np.float32).reshape([1, 1, 3, 1])
    batched_index_points = np.stack([index_points]*6)
    # ==> shape = [6, 25, 2]
    kernel = tfk.ExponentiatedQuadratic(amplitude, length_scale)
    multi_task_kernel = tfe.psd_kernels.Independent(
        num_tasks=3, base_kernel=kernel)
    multitask_gp = tfe.distributions.MultiTaskGaussianProcess(
        multi_task_kernel,
        batched_index_points,
        observation_noise_variance=observation_noise_variance,
        validate_args=True)

    @tf.function(jit_compile=True)
    def log_prob(o):
      return multitask_gp.log_prob(o)

    @tf.function(jit_compile=True)
    def sample():
      return multitask_gp.sample(seed=test_util.test_seed())

    observations = tf.convert_to_tensor(
        np.linspace(-20., 20., 75).reshape(25, 3).astype(np.float32))
    self.assertAllEqual(log_prob(observations).shape, [2, 4, 3, 6])
    self.assertAllEqual(sample().shape, [2, 4, 3, 6, 25, 3])

    multitask_gp = tfe.distributions.MultiTaskGaussianProcess(
        multi_task_kernel,
        batched_index_points,
        observation_noise_variance=None,
        validate_args=True)

    @tf.function(jit_compile=True)
    def log_prob_no_noise(o):
      return multitask_gp.log_prob(o)

    @tf.function(jit_compile=True)
    def sample_no_noise():
      return multitask_gp.sample(seed=test_util.test_seed())

    self.assertAllEqual(log_prob_no_noise(observations).shape, [2, 4, 1, 6])
    self.assertAllEqual(sample_no_noise().shape, [2, 4, 1, 6, 25, 3])

  def testLogProbMatchesGP(self):
    # Check that the independent kernel parameterization matches using a
    # single-task GP.

    # 5x5 grid of index points in R^2 and flatten to 25x2
    index_points = np.linspace(-4., 4., 5, dtype=np.float32)
    index_points = np.stack(np.meshgrid(index_points, index_points), axis=-1)
    index_points = np.reshape(index_points, [-1, 2])
    # ==> shape = [25, 2]

    # Kernel with batch_shape [2, 4, 3, 1]
    amplitude = np.array([1., 2.], np.float32).reshape([2, 1, 1, 1])
    length_scale = np.array([1., 2., 3., 4.], np.float32).reshape([1, 4, 1, 1])
    observation_noise_variance = np.array(
        [1e-5, 1e-6, 1e-5], np.float32).reshape([1, 1, 3, 1])
    batched_index_points = np.stack([index_points]*6)
    # ==> shape = [6, 25, 2]
    kernel = tfk.ExponentiatedQuadratic(amplitude, length_scale)
    multi_task_kernel = tfe.psd_kernels.Independent(
        num_tasks=3, base_kernel=kernel)
    multitask_gp = tfe.distributions.MultiTaskGaussianProcess(
        multi_task_kernel,
        batched_index_points,
        observation_noise_variance=observation_noise_variance,
        validate_args=True)
    gp = tfd.GaussianProcess(
        kernel,
        batched_index_points,
        observation_noise_variance=observation_noise_variance,
        validate_args=True)
    observations = np.linspace(-20., 20., 75).reshape(25, 3).astype(np.float32)
    multitask_log_prob = multitask_gp.log_prob(observations)
    single_task_log_prob = sum(
        gp.log_prob(observations[..., i]) for i in range(3))
    self.assertAllClose(
        self.evaluate(single_task_log_prob),
        self.evaluate(multitask_log_prob), rtol=4e-3)


if __name__ == '__main__':
  test_util.main()
