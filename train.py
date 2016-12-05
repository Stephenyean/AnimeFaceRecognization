import getData
import tensorflow as tf
animes  = getData.dataSet("thumb_test")

x_image=tf.placeholder("float",shape=[None, 60, 60, 3])
y_=tf.placeholder("float",shape=[None, 20])
eps = 1e-9
#x_image=tf.reshape(x,[-1,60,60,1])

def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1,shape=shape)
	return tf.Variable(initial)

def conv2d(x,W):
	return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

def max_pool_2x2(x):
	return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

W_conv1 = weight_variable([5,5,3,64])
b_conv1 = bias_variable([64])

h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5,5,64,128])
b_conv2 = bias_variable([128])

h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1   = weight_variable([15 * 15 * 128, 2048 ])
b_fc1   = bias_variable([2048])

h_pool2_flat = tf.reshape(h_pool2,[-1,15 * 15 * 128])
h_fc1   = tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1) + b_fc1)

keep_prob=tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)
W_fc2 = weight_variable([2048,20])
b_fc2 = bias_variable([20])

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2) + b_fc2)
cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv + eps))
train_step = tf.train.AdadeltaOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

with tf.Session() as sess:
	with tf.device("/gpu:0"):
		sess.run(tf.initialize_all_variables())
		for i in range(20000):
  			batch = animes.next_train_batch(128)
			#print "W_fc2:",sess.run(W_fc2,feed_dict={x_image:batch[0], y_: batch[1], keep_prob: 1.0})
			#print "b_fc2:",sess.run(b_fc2,feed_dict={x_image:batch[0], y_: batch[1], keep_prob: 1.0})
			#print "y_conv:",sess.run(y_conv,feed_dict={x_image:batch[0], y_: batch[1], keep_prob: 1.0})
			#print "cross_entropy",sess.run(cross_entropy,feed_dict={x_image:batch[0], y_: batch[1], keep_prob: 1.0})
			#print "train_step",sess.run(train_step,feed_dict={x_image:batch[0], y_: batch[1], keep_prob: 1.0})
			#print "correct_prediction",sess.run(correct_prediction,feed_dict={x_image:batch[0], y_: batch[1], keep_prob: 1.0})
			#print "accuracy",sess.run(accuracy,feed_dict={x_image:batch[0], y_: batch[1], keep_prob: 1.0})
				

			#print batch[0][0]
			#print sess.run(b_fc2)
  			if i%20 == 0:
				train_accuracy = sess.run( accuracy, feed_dict={x_image:batch[0], y_: batch[1], keep_prob: 1.0})
				print("step %d, training accuracy %g"%(i, train_accuracy))
			sess.run(train_step,feed_dict={x_image: batch[0], y_: batch[1], keep_prob: 0.3})
			#print sess.run(b_fc2)
			if i%40 == 0:
				print("test accuracy %g"% sess.run(accuracy, feed_dict={ x_image: animes.testSet, y_: animes.testLabel, keep_prob: 1.0}))