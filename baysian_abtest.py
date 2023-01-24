import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import math
import base64
from io import BytesIO

def run_baysian_abtest(segA_n: int, segA_cv: int, segB_n: int, segB_cv: int):
    # Assuming a Beta distribution as the conjugate prior distribution and a uniform distribution for the prior
    alpha_pre = 1
    beta_pre = 1

    # posterior distribution
    postA = stats.beta(alpha_pre + segA_cv, beta_pre + segA_n - segA_cv)
    postB = stats.beta(alpha_pre + segB_cv, beta_pre + segB_n - segB_cv)

    # plot result
    sample_size = 100000 #元々のモデルが充分に表現できるサンプルサイズを設定

    beta_A = postA.rvs(size=sample_size, random_state=42) * 100
    beta_B = postB.rvs(size=sample_size, random_state=41) * 100

    bins = round(math.log2(sample_size)) + 50 #More than the Sturgess formula.
    beta_diff = beta_B - beta_A
    
    winnerB_prob = (beta_diff > 0).mean() * 100
    winner = 'B' if winnerB_prob >= 50.0 else 'A'
    win_prob = round(winnerB_prob, 2) if winner == 'B'else round(100 - winnerB_prob, 2)

    return winner, win_prob, beta_A, beta_B, beta_diff, bins


def encode_figure_base64(fig):
    io = BytesIO()
    fig.savefig(io, format='png')
    io.seek(0)
    return base64.b64encode(io.read()).decode()


def save_result_image(beta_A, beta_B, beta_diff, bins): 
    bins_list = np.linspace(
        min(beta_A.min(), beta_B.min()),
        max(beta_A.max(), beta_B.max()),
        bins
    ) 
    
    # plotting abtest results
    fig_res = plt.figure(figsize=(20, 10))
    plt.rcParams['font.size'] = 24
    plt.hist(beta_A, bins=bins_list, alpha=0.5, density=True, color='tab:red', label='A')
    plt.hist(beta_B, bins=bins_list, alpha=0.5, density=True, color='tab:blue', label='B')
    plt.xlabel('cv rate(%)')
    plt.legend()
    base64_img_res = encode_figure_base64(fig_res)
    
    # plotting diff distribution of ab
    fig_diff = plt.figure(figsize=(20, 10))
    plt.hist(beta_diff, bins=bins, color='tab:green', alpha=0.5, label='B - A')
    plt.axvline(x=0, color='tab:red')
    plt.xlabel('cv rate diff(%)')
    plt.legend()
    base64_img_diff = encode_figure_base64(fig_diff)
    
    return base64_img_res, base64_img_diff