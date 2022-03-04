# Copyright 2020 The TensorFlow Probability Authors.
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
"""Tests for `tfp.util.DeferredModule`."""

import tensorflow.compat.v2 as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import samplers
from tensorflow_probability.python.internal import test_util


tfb = tfp.bijectors
tfd = tfp.distributions


def _gamma_from_loc_scale(loc, log_scale):
  return tfd.Gamma(concentration=(loc / tf.exp(log_scale))**2,
                   rate=loc / (tf.exp(log_scale))**2)


@test_util.test_all_tf_execution_regimes
class DeferredModuleTest(test_util.TestCase):

  def testDistributionTapeSafety(self):
    log_precision = tf.Variable(0.)
    mean_times_precision = tf.Variable(1.)

    def normal_from_natural(log_precision, mean_times_precision):
      variance = 1./tf.exp(log_precision)
      mean = mean_times_precision * variance
      return tfd.Normal(loc=mean, scale=tf.sqrt(variance))
    dist = tfp.experimental.util.DeferredModule(
        normal_from_natural, log_precision, mean_times_precision)
    self.assertIn(log_precision, dist.trainable_variables)
    self.assertIn(mean_times_precision, dist.trainable_variables)

    with tf.GradientTape() as tape:
      lp = dist.log_prob(0.4)
    grads = tape.gradient(lp, dist.trainable_variables)
    self.assertLen(grads, 2)
    for grad in grads:
      self.assertIsNotNone(grad)

  def testTracksExogenousTrainableVariables(self):
    loc = tf.Variable(0., name='loc')
    def build_normal(scale):
      return tfd.Normal(loc=loc, scale=scale)
    dist = tfp.experimental.util.DeferredModule(
        build_normal, scale=tf.Variable(1., name='scale'), also_track=loc)

    # Check that variable tracking works recursively, as well as directly.
    wrapped_dist = tfd.Sample(dist, sample_shape=[2])
    self.assertLen(getattr(wrapped_dist, 'trainable_variables'), 2)
    self.assertLen(getattr(dist, 'trainable_variables'), 2)

  def testDistributionBatchSlicing(self):

    batch_shape = [4, 3]
    seed0, seed1 = samplers.split_seed(test_util.test_seed(), 2)
    log_precision = tf.Variable(samplers.normal(batch_shape, seed=seed0))
    mean_times_precision = tf.Variable(samplers.normal(batch_shape, seed=seed1))

    def normal_from_natural(log_precision, mean_times_precision):
      variance = 1./tf.exp(log_precision)
      mean = mean_times_precision * variance
      return tfd.Normal(loc=mean, scale=tf.sqrt(variance))
    dist = tfp.experimental.util.DeferredModule(
        normal_from_natural, log_precision, mean_times_precision)
    self.assertLen(dist.trainable_variables, 2)

    sliced = dist[:2]
    self.assertEqual(sliced.batch_shape, [2, 3])
    # We do *not* expect the slicing itself to be deferred: like log_prob,
    # sample, and other methods, slicing produces a concrete value (that happens
    # to be a Distribution instance).
    self.assertLen(sliced.trainable_variables, 0)

    sliced_sample = sliced.sample(5)
    self.assertEqual(sliced_sample.shape, [5, 2, 3])

  def testDeferredTransformedDistribution(self):
    log_concentration = tf.Variable(0.)
    log_rate = tf.Variable(0.)
    log_scale = tf.Variable(-1.0)
    dist = tfp.experimental.util.DeferredModule(
        lambda a, b, c: tfd.TransformedDistribution(tfd.Gamma(tf.exp(a),  # pylint: disable=g-long-lambda
                                                              tf.exp(b)),
                                                    tfb.Scale(tf.exp(c))),
        log_concentration,
        log_rate,
        log_scale)
    with tf.GradientTape() as tape:
      x = dist.sample()
    self.assertAllNotNone(
        tape.gradient(x,
                      [log_concentration,
                       log_rate,
                       log_scale]))

  def testBijectorCallDistribution(self):
    log_scale = tf.Variable(-1.0)
    self.evaluate(log_scale.initializer)

    bij = tfp.experimental.util.DeferredModule(
        lambda log_scale: tfb.Scale(tf.exp(log_scale)),
        log_scale)
    self.assertLen(bij.trainable_variables, 1)

    # Calling the deferred bij produces a concretized TransformedDistribution.
    dist = bij(tfd.Normal(0., 1.))
    self.assertLen(dist.trainable_variables, 0)

    # We can also defer the call itself, if we like.
    deferred_dist = tfp.experimental.util.DeferredModule(
        lambda loc, scale: bij(tfd.Normal(loc, scale)), loc=0., scale=1.)

    lp = dist.log_prob(17.)
    with tf.GradientTape() as tape:
      lp_deferred = deferred_dist.log_prob(17.)
    g = tape.gradient(lp_deferred, log_scale)
    self.assertIsNotNone(g)
    self.assertAllClose(*self.evaluate((lp, lp_deferred)))

  def testCallingConventions(self):

    loc = tf.Variable(3.)
    log_scale = tf.Variable(1.)
    self.evaluate((loc.initializer, log_scale.initializer))

    # Check that we can call the build_fn with positional or named arguments.
    dist_args = tfp.experimental.util.DeferredModule(
        _gamma_from_loc_scale, loc, log_scale)
    dist_kwargs = tfp.experimental.util.DeferredModule(
        _gamma_from_loc_scale, loc=loc, log_scale=log_scale)

    with tf.GradientTape(persistent=True) as tape:
      mean1, log_stddev1 = dist_args.mean(), tf.math.log(dist_args.stddev())
      mean2, log_stddev2 = dist_kwargs.mean(), tf.math.log(dist_kwargs.stddev())
    self.assertAllClose(
        self.evaluate(tape.gradient(mean1, [loc, log_scale])),
        [1., 0.])
    self.assertAllClose(
        self.evaluate(tape.gradient(mean2, [loc, log_scale])),
        [1., 0.])
    self.assertAllClose(
        self.evaluate(tape.gradient(log_stddev1, [loc, log_scale])),
        [0., 1.])
    self.assertAllClose(
        self.evaluate(tape.gradient(log_stddev2, [loc, log_scale])),
        [0., 1.])


if __name__ == '__main__':
  test_util.main()
