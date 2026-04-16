import numpy as np
import matplotlib.pyplot as plt

# ========================== Universal Raw Qualia Density × MA Model v8.0 ==========================
# Brain-wide Negentropy Engine (no thalamus assumption)
# Dewa et al. (Nature 2025) inspired dual-timescale: labile neuronal phase → astrocytic consolidation

class RawQualiaDensityMA:
    """v8.0 Universal Model - Raw Qualia as living Negentropy Engine
    Brain-region agnostic. Implements labile decay → astro consolidation.
    """
    def __init__(self, alpha=0.92, astro_alpha=0.99985, Q_thresh=0.48,
                 noise_sigma=0.03, labile_decay_rate=0.995,
                 decay_start_step=1440, multiday_mode=True):
        """Initialize Universal Density × MA engine"""
        self.alpha = astro_alpha if multiday_mode else alpha
        self.MA = 0.0
        self.Q_history = []
        self.D_history = []
        self.FE_history = []
        self.labile_decay_rate = labile_decay_rate
        self.decay_start_step = decay_start_step
        self.multiday_mode = multiday_mode
        self.step_count = 0

        print(f"v8.0 Universal RawQualiaDensityMA initialized | "
              f"Mode: {'Multiday Astro + Labile Decay' if multiday_mode else 'Neural'} | "
              f"α={self.alpha:.6f} | Decay starts at step {decay_start_step}")

    def step(self, D: float, pi_s=1.0, pi_p=0.1, k=1.0, other_D=None):
        """One step with Friston precision weighting + explicit labile decay timing"""
        w_precision = pi_s / (pi_s + k * pi_p)
        D_eff = D * w_precision

        # Labile neuronal decay phase (first day)
        if self.step_count < self.decay_start_step:
            D_eff *= (self.labile_decay_rate ** self.step_count)
        else:
            # Astrocytic consolidation (multiday slow trace)
            self.MA = self.alpha * self.MA + (1 - self.alpha) * D_eff

        Q = D_eff * (self.MA + 1e-8)          # Raw Qualia = D_eff × MA
        FE = -Q * np.log(Q + 1e-8)            # Free Energy proxy (energy cost)

        self.Q_history.append(Q)
        self.D_history.append(D)
        self.FE_history.append(FE)
        self.step_count += 1

        return Q, self.MA, FE

    @staticmethod
    def simulate_labile_to_astro(days=5):
        """Simulation: labile phase → astro consolidation (Dewa 2025 inspired)"""
        model = RawQualiaDensityMA(multiday_mode=True)
        t = np.arange(0, days * 1440)
        base_D = 0.7 + 0.2 * np.sin(2 * np.pi * t / (1440 * 2))  # daily rhythm

        Q_list, MA_list, D_list = [], [], []
        for d in base_D:
            Q, MA, _ = model.step(d)
            Q_list.append(Q)
            MA_list.append(MA)
            D_list.append(d)

        return t, np.array(D_list), np.array(Q_list), np.array(MA_list)

# ========================== Visualization ==========================
def plot_labile_to_astro():
    """Visualize your hypothesis: labile → astro consolidation"""
    t, D, Q, MA = RawQualiaDensityMA.simulate_labile_to_astro(days=5)
    
    fig, axs = plt.subplots(3, 1, figsize=(12, 9))
    
    axs[0].plot(t/1440, D, color='blue', label='Current Input Density D(t)')
    axs[0].axvline(x=1, color='red', linestyle='--', label='Day 1: Astro Consolidation Begins')
    axs[0].set_title('v8.0 Universal: Labile Neuronal Phase → Astrocytic Consolidation')
    axs[0].set_ylabel('D(t)')
    axs[0].legend()
    
    axs[1].plot(t/1440, MA, color='orange', lw=2, label='MA (Astro Trace)')
    axs[1].set_ylabel('Historical Assembly Depth MA')
    axs[1].legend()
    
    axs[2].plot(t/1440, Q, color='purple', lw=2, label='Raw Qualia Q = D × MA')
    axs[2].set_xlabel('Time (days)')
    axs[2].set_ylabel('Raw Qualia')
    axs[2].legend()
    
    plt.tight_layout()
    plt.show()

# ========================== Run ==========================
if __name__ == "__main__":
    print("=== Universal Raw Qualia Density × MA Model v8.0 ===")
    print("Brain-wide Negentropy Engine | Dewa et al. (Nature 2025) support")
    plot_labile_to_astro()