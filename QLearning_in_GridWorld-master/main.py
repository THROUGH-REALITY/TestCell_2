import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter

from grid_world import GridWorld
from qlearning_agent import QLearningAgent

# 定数
NB_EPISODE = 1000   # エピソード数
EPSILON = .1    # 探索率
ALPHA = .1      # 学習率
GAMMA = .90     # 割引率
ACTIONS = np.arange(4)  # 行動の集合
X_MAX = 15
Y_MAX = 18
START_X = X_MAX - 1     # 端からスタートさせる
START_Y = Y_MAX - 1
start = time.time()

if __name__ == '__main__':
    grid_env = GridWorld(   # grid worldの環境の初期化
        x_max=X_MAX,
        y_max=Y_MAX,
        start_x=START_X,
        start_y=START_Y)  
    ini_state = grid_env.start_pos  # 初期状態（エージェントのスタート地点の位置）
    
    agent = QLearningAgent(# エージェントの初期化
        alpha=ALPHA,
        gamma=GAMMA,
        epsilon=EPSILON,  # 探索率
        actions=ACTIONS,   # 行動の集合
        observation=ini_state)  # Q学習エージェント
    #rewards = []    # 評価用報酬の保存
    times = []
    is_end_episode = False  # エージェントがゴールしてるかどうか？

    # 実験
    for episode in range(NB_EPISODE):
        episode_reward = []  # 1エピソードの累積報酬
        while(is_end_episode == False):    # ゴールするまで続ける
            action = agent.act()  # 行動選択
            state, reward, is_end_episode = grid_env.step(action)
            agent.observe(state, reward)   # 状態と報酬の観測
            episode_reward.append(reward)
        #rewards.append(np.sum(episode_reward))  # このエピソードの平均報酬を与える
        times.append(len(episode_reward)) #かかった時間をリストに追加
        state = grid_env.reset()  # 初期化
        agent.observe(state)    # エージェントを初期位置に
        is_end_episode = False
        print(f"EP.{episode +1} End (t = {len(episode_reward)})")

    # 結果のプロット,可視化
    fig = plt.figure(figsize=(12,6),tight_layout=True)  # 図を描く大きさと、図の変数名を宣言
    gs = fig.add_gridspec(1, 3)
    
    ax1 = fig.add_subplot(
        gs[0, 0],
        xlabel="X",
        ylabel="Y",
        title="Grid World")
    ax1.text(START_X, START_Y+0.3, 'S', ha='center', c='brown')
    ax1.text(0, 0.2, 'G', ha='center')
    ax1.imshow(grid_env.map)
    ax2 = fig.add_subplot(
        gs[0, 1:],
        xlabel="episode",
        ylabel="time",
        xlim=(0,NB_EPISODE),
        title="Result")
    ax2.plot(np.arange(NB_EPISODE), times)

    # 目盛りを消す設定
    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    labelbottom='off', right='off', left='off', labelleft='off')
    line, = ax1.plot([START_X], [START_Y], marker="o", color='limegreen', markersize=11)

    # 所要時間の計算
    print(f"time = {time.time()-start}")
    fig.savefig("map_result.jpg")
    fig.show()    

    agents_data = model.datacollector.get_agent_vars_dataframe()    
    state = list(agents_data["state"])
    def init():
        '''背景画像の初期化'''
        line.set_data([], [])
        return (line,)
    def animate(i):
        '''フレームごとの描画内容'''
        s = state[i]  # 現在の場所を描く
        x = s % 3
        y = s // 3
        line.set_data(x, y)
        return (line,)
    #　初期化関数とフレームごとの描画関数を用いて動画を作成する
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(
        state), interval=200, repeat=False) #1秒ごとにlen(state)をanimateに渡している

    anim.save("unbelievable.gif", writer="pillow", fps=60)