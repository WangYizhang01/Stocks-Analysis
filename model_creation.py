import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import minmax_scale
import matplotlib.pyplot as plt
tf.keras.backend.set_floatx('float64')

# 读取数据集
df = pd.read_csv('/Users/apple/PycharmProjects/untitled4/stock_analysis/fun_data.csv')
df = df[['open','high','low','rise']]
# 数据归一化
df['open'] = minmax_scale(df['open'])
df['high'] = minmax_scale(df['high'])
df['low'] = minmax_scale(df['low'])
df['rise'] = minmax_scale(df['rise'])
# print(df.shape)

# 定义输入序列并分割数据集
valid_set_size_percentage = 10
test_set_size_percentage = 10


def load_data(stock,seq_len=20):
    data_raw = stock.values # pd to numpy array
    data = []
    # 创建所有可能的长度序列seq_len
    for index in range(len(data_raw)-seq_len):
        data.append(data_raw[index:index+seq_len])
    data = np.array(data)
    valid_set_size = int(np.round(valid_set_size_percentage/100 * data.shape[0]))
    test_set_size = int(np.round(test_set_size_percentage / 100 * data.shape[0]))
    train_set_size = data.shape[0] - (valid_set_size+test_set_size)
    # x_train = data[:train_set_size,:-1,:-1]
    # y_train = data[:train_set_size,-1,0]
    # x_valid = data[train_set_size:(train_set_size+valid_set_size),:-1,:-1]
    # y_valid = data[train_set_size:(train_set_size+valid_set_size),-1,0]
    x_train = data[:train_set_size, :-1,0]
    y_train = data[:train_set_size, -1, 0]
    x_valid = data[train_set_size:(train_set_size + valid_set_size), :-1,0]
    y_valid = data[train_set_size:(train_set_size + valid_set_size), -1, 0]

    x_test = data[(train_set_size+valid_set_size):,:-1,:-1]
    y_test = data[(train_set_size+valid_set_size):,-1,0]
    return [x_train,y_train,x_valid,y_valid,x_test,y_test]


# 模型参数
seq_len = 20
n_steps = seq_len-1 # 输入张量维数
n_inputs = 1
n_neurons = 200 # GRU层神经元个数
n_outputs = 1
learning_rate = 0.001 # 学习率
batch_size = 500
n_epochs = 100 # 训练次数


class GRUModel(tf.keras.Model):
    def __init__(self, batch_size, seq_length, cell_size,n_inputs,n_outputs):
        super().__init__()
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.cell_size = cell_size
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs

        self.layer1 = tf.keras.layers.Reshape((self.seq_length, self.n_inputs), batch_size=self.batch_size)
        self.layer_GRU = tf.keras.layers.GRU(self.cell_size, return_sequences=True)
        self.layer_last_GRU = tf.keras.layers.GRU(self.cell_size)
        self.layer_dense = tf.keras.layers.Dense(self.n_outputs)

    def call(self, inputs):
        x = self.layer1(inputs)
        x = self.layer_GRU(x)
        x = self.layer_last_GRU(x)
        output = self.layer_dense(x)
        return output

x_train,y_train,x_valid,y_valid,x_test,y_test = load_data(df,seq_len)
model = GRUModel(batch_size, n_steps,n_neurons,n_inputs,n_outputs)
optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate)

for epoch in range(n_epochs):
    with tf.GradientTape() as tape:
        y_pred = model(x_train)
        loss = tf.reduce_mean((y_pred - y_train) ** 2)
        if epoch % 5 == 0:
            print("epoch: {}, loss: {}".format(epoch, loss.numpy()))

    grads = tape.gradient(loss, model.variables)
    optimizer.apply_gradients(zip(grads, model.variables))

    # categorical_accuracy = tf.keras.metrics.CategoricalAccuracy()
    # y_test_pred = model.predict(x=x_valid)
    # categorical_accuracy.update_state(y_true=y_valid, y_pred=y_test_pred)
    # accuracy = categorical_accuracy.result().numpy()
    # if epoch % 5 == 0:
    #     print("epoch: {}, loss: {}, accuracy: {}".format(epoch, loss.numpy(),accuracy))

x_t = x_train[-50:]
y_t = y_train[-50:]
y_ = model.predict(x_t)
y_ = y_.reshape([1,-1])[0]
len = len(y_)
count = 0
for i in range(len-1):
    if y_[i+1] >= y_[i] and y_t[i+1] >= y_t[i]:
        count += 1
    elif y_[i+1] < y_[i] and y_t[i+1] < y_t[i]:
        count += 1
print(count)
print(count/len)
# print(y_)
# print(y_valid)
df2 = pd.DataFrame({'y_':y_,'y_valid':y_t})
df2.plot()
plt.show()
