import numpy as np
import matplotlib.pyplot as plt

# ====================== TRIBE v2刺激パターン再現 ======================
np.random.seed(42)
n_samples = 1200
block_length = 400

D = np.zeros(n_samples)
D[0:block_length] = np.abs(np.random.normal(0.45, 0.12, block_length))      # Music
D[block_length:2*block_length] = np.abs(np.random.normal(0.65, 0.15, block_length))  # Language
D[2*block_length:] = np.abs(np.random.normal(0.82, 0.18, block_length))    # Visual
D = np.clip(D, 0.05, 0.95)

# ====================== Density × MA モデル（論文仕様に統一） ======================
alpha = 0.92                                      # ← Supplement S1と完全一致
MA = np.zeros(n_samples)
MA[0] = D[0]
for i in range(1, n_samples):
    MA[i] = alpha * MA[i-1] + (1 - alpha) * D[i]

Q_densityma = D * MA

# ====================== 他の理論の簡易プロキシ ======================
Phi = D * 0.08 + MA * 0.15                    # IIT proxy
ignition = np.where(D > 0.65, D * 1.2, D * 0.3)  # GNWT proxy
FEP = 1.0 - np.exp(-D * MA * 2.5)             # FEP proxy

# ====================== 結果出力 ======================
print("=== TRIBE v2 Comparative Simulation ===")
print(f"Density × MA  Mean Q : {np.mean(Q_densityma):.3f}")
print(f"IIT Proxy      Mean : {np.mean(Phi):.3f}")
print(f"GNWT Proxy     Mean : {np.mean(ignition):.3f}")
print(f"FEP Proxy      Mean : {np.mean(FEP):.3f}")

# ====================== 高品質グラフ（あなたのpng画像と同じ見た目） ======================
fig, axs = plt.subplots(2, 2, figsize=(14, 9))
plt.suptitle('TRIBE v2 Stimulus Pattern: Music → Language → Visual\n'
             'Consciousness Theory Comparison', fontsize=14, fontweight='bold')

# 共通設定
for ax in axs.flat:
    ax.axvline(400, color='gray', linestyle='--', alpha=0.7)
    ax.axvline(800, color='gray', linestyle='--', alpha=0.7)
    ax.set_xlabel('Time steps')
    ax.set_xlim(0, 1200)

# Density × MA
axs[0,0].plot(Q_densityma, color='purple', label='Density × MA Q')
axs[0,0].set_title('Density × MA (proposed)')
axs[0,0].legend()

# IIT
axs[0,1].plot(Phi, color='blue', label='IIT Phi proxy')
axs[0,1].set_title('IIT Proxy')

# GNWT
axs[1,0].plot(ignition, color='green', label='GNWT Ignition proxy')
axs[1,0].set_title('GNWT Proxy (Ignition)')

# FEP
axs[1,1].plot(FEP, color='orange', label='FEP Free Energy proxy')
axs[1,1].set_title('FEP Proxy')

# ブロック背景（あなたのpngと同じ）
for ax in axs.flat:
    ax.axvspan(0, 400, color='lightgreen', alpha=0.08)
    ax.axvspan(400, 800, color='lightblue', alpha=0.08)
    ax.axvspan(800, 1200, color='lightyellow', alpha=0.08)

plt.tight_layout()
plt.savefig('TRIBE_v2_comparison_figure9.png', dpi=300, bbox_inches='tight')
plt.show()