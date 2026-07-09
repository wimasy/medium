import random

N = 1_000_000

fail_three_tier = 0
fail_three_tier_r = 0
fail_spine_leaf = 0

for _ in range(N):
    # ==========================
    # Three-Tier
    # Access -> Distribution -> Core
    # ==========================

    access = random.random() < 0.02
    distribution = random.random() < 0.01
    core = random.random() < 0.01

    if access or distribution or core:
        fail_three_tier += 1

    # ==================================================
    # Three-Tier Redundan
    #
    # Access
    #    │
    # Dist1 ----- Dist2
    #    │         │
    # Core1 ----- Core2
    #
    # Distribution gagal jika Dist1 DAN Dist2 gagal
    # Core gagal jika Core1 DAN Core2 gagal
    # ==================================================

    access = random.random() < 0.02

    dist1 = random.random() < 0.01
    dist2 = random.random() < 0.01

    core1 = random.random() < 0.01
    core2 = random.random() < 0.01

    distribution_failed = dist1 and dist2
    core_failed = core1 and core2

    if access or distribution_failed or core_failed:
        fail_three_tier_r += 1

    # ==========================
    # Spine-Leaf
    # Leaf -> (Spine1 || Spine2) -> Leaf
    # ==========================

    source_leaf = random.random() < 0.01
    destination_leaf = random.random() < 0.01

    spine1 = random.random() < 0.01
    spine2 = random.random() < 0.01

    # Backbone gagal jika kedua spine gagal
    backbone_failed = spine1 and spine2

    if source_leaf or backbone_failed or destination_leaf:
        fail_spine_leaf += 1

print(f"Three-Tier : {fail_three_tier/N:.4%}")
print(f"Three-TierR: {fail_three_tier_r/N:.4%}")
print(f"Spine-Leaf : {fail_spine_leaf/N:.4%}")
