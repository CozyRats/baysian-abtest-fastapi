import numpy as np
from matplotlib import pyplot as plt
import japanize_matplotlib
import seaborn as sns
from scipy import stats
import math

# 実験結果を入力
# segA_n = 1000
# segA_cv = 100

# segB_n = 1000
# segB_cv = 105

def run_baysian_abtest(segA_n: int, segA_cv: int, segB_n: int, segB_cv: int):
    
    # 共役事前分布としてBeta分布を、事前分布を一様分布と仮定
    alpha_pre = 1
    beta_pre = 1

    # 事後分布
    postA = stats.beta(alpha_pre + segA_cv, beta_pre + segA_n - segA_cv)
    postB = stats.beta(alpha_pre + segB_cv, beta_pre + segB_n - segB_cv)

    # 事後分布のパラメーターを元にヒストグラムを作成
    sample_size = 100000 #元々のモデルが充分に表現できるサンプルサイズを設定

    beta_A = postA.rvs(size=sample_size) * 100 #%にするために100を掛ける
    beta_B = postB.rvs(size=sample_size) * 100

    bins = round(math.log2(sample_size)) + 50 #多めに区切る
    bins_list = np.linspace(
        min(beta_A.min(), beta_B.min()),
        max(beta_A.max(), beta_B.max()),
        bins
        ) 

    # plt.hist(beta_A, bins=bins_list, alpha=0.5, density=True, color='tab:red')
    # plt.hist(beta_B, bins=bins_list, alpha=0.5, density=True, color='tab:blue')
    # plt.show()

    # 差をプロット
    beta_diff = beta_B - beta_A
    # plt.hist(beta_diff, bins=bins, color='tab:green', alpha=0.5)
    # plt.show()

    
    winnerB_prob = round((beta_diff > 0).mean(), 3) * 100
    
    winner = 'B' if winnerB_prob >= 50.0 else 'A'
    win_prob = winnerB_prob if winner == 'B'else 100 - winnerB_prob

    return winner, win_prob