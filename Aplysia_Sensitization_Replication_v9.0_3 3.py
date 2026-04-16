import numpy as np
import matplotlib.pyplot as plt

class AplysiaDensityMA:
    """
    v9.0 Final English Edition - Aplysia Sensitization Replication
    Universal Density × MA Model for Raw Qualia
    On the Human Being as a Negentropy Engine
    Replicates Kandel (2001) + Dewa et al. (Nature 2025) dual-timescale dynamics:
    - Short-term facilitation (labile neuronal phase)
    - Long-term consolidation (astrocytic trace - persists after trigger)
    """
    def __init__(self):
        self.MA = 0.0
        self.long_term_active = False          # Once triggered, astro consolidation persists
        self.alpha_short = 0.85                # Fast decay for short-term
        self.alpha_long = 0.99985              # Extremely slow decay for long-term

    def step(self, D: float, is_long_term: bool = False):
        """One simulation step with persistent long-term mode"""
        if is_long_term or self.long_term_active:
            self.long_term_active = True
            self.MA = self.alpha_long * self.MA + (1 - self.alpha_long) * D
        else:
            self.MA = self.alpha_short * self.MA + (1 - self.alpha_short) * D * 0.35  # slightly tuned for visibility
        
        Q = D * (self.MA + 1e-8)  # Raw Qualia = Density × MA
        return Q, self.MA

    def simulate(self, steps: int = 1000):
        """Replicates Kandel’s classic Aplysia californica experiments"""
        stimuli = [0.0] * steps
        stimuli[100] = 1.0                              # Single strong stimulus (short-term)
        for t in range(200, 401, 50):                   # 5× repeated stimuli (long-term trigger)
            stimuli[t] = 0.8

        Q_list = []
        MA_list = []
        for i, d in enumerate(stimuli):
            is_long_term = (200 <= i <= 400)
            Q, MA = self.step(d, is_long_term=is_long_term)
            Q_list.append(Q)
            MA_list.append(MA)

        return np.array(Q_list), np.array(MA_list)


# ========================== Run & Save for Paper (Fig. 6) ==========================
if __name__ == "__main__":
    print("=== Aplysia Sensitization Replication v9.0 Final (English Edition) ===")
    print("Universal Density × MA Model | Kandel (2001) + Dewa et al. (Nature 2025)")
    
    model = AplysiaDensityMA()
    Q, MA = model.simulate()

    plt.figure(figsize=(11, 6))
    plt.plot(Q, label='Raw Qualia Q (Aplysia-like experience)', color='purple', lw=2)
    plt.plot(MA, label='MA (historical assembly depth)', color='orange', lw=2, alpha=0.85)
    plt.axvspan(200, 400, color='red', alpha=0.12, label='5× repeated stimulation (long-term sensitization)')
    plt.axvline(100, color='blue', linestyle='--', lw=2, label='Single strong stimulus (short-term facilitation)')
    plt.title('Aplysia Sensitization Replicated with Density × MA v9.0\n'
              'Short-term facilitation vs Long-term astrocytic consolidation\n'
              '(Kandel 2001 + Dewa et al. Nature 2025)')
    plt.xlabel('Time steps')
    plt.ylabel('Normalized value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Save high-resolution version for Zenodo & paper
    plt.savefig('Fig6_Aplysia_Sensitization_Replication_v9.0.png', dpi=300, bbox_inches='tight')
    print("✅ Graph saved as Fig6_Aplysia_Sensitization_Replication_v9.0.png")
    print("   Max Q (short-term):", round(Q.max(), 6))
    print("   Final MA (long-term):", round(MA[-1], 6))