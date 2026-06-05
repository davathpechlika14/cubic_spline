
# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt

# # =====================================================
# # Page Config
# # =====================================================

# st.set_page_config(
#     page_title="Cubic Spline Project",
#     page_icon="📈",
#     layout="wide"
# )

# st.markdown("""
# <style>
# [data-testid="metric-container"] {
#     background-color: #dbeafe;
#     border: 1px solid #93c5fd;
#     padding: 15px;
#     border-radius: 12px;
# }

# [data-testid="metric-container"] label {
#     color: #1e3a8a;
#     font-weight: bold;
# }
# </style>
# """, unsafe_allow_html=True)

# # =====================================================
# # Thomas Algorithm
# # =====================================================

# def solve_tridiagonal(A_matrix, B_vector):

#     n = len(B_vector)

#     a = np.zeros(n)
#     b = np.zeros(n)
#     c = np.zeros(n)

#     b[0] = A_matrix[0, 0]
#     c[0] = A_matrix[0, 1]

#     for i in range(1, n - 1):
#         a[i] = A_matrix[i, i - 1]
#         b[i] = A_matrix[i, i]
#         c[i] = A_matrix[i, i + 1]

#     a[n - 1] = A_matrix[n - 1, n - 2]
#     b[n - 1] = A_matrix[n - 1, n - 1]

#     c_prime = np.zeros(n)
#     d_prime = np.zeros(n)

#     c_prime[0] = c[0] / b[0]
#     d_prime[0] = B_vector[0] / b[0]

#     for i in range(1, n):

#         den = b[i] - a[i] * c_prime[i - 1]

#         if i < n - 1:
#             c_prime[i] = c[i] / den

#         d_prime[i] = (
#             B_vector[i]
#             - a[i] * d_prime[i - 1]
#         ) / den

#     X = np.zeros(n)

#     X[n - 1] = d_prime[n - 1]

#     for i in range(n - 2, -1, -1):
#         X[i] = d_prime[i] - c_prime[i] * X[i + 1]

#     return X


# # =====================================================
# # Cubic Spline
# # =====================================================

# def compute_cubic_spline_coefficients(
#     x,
#     y,
#     boundary_type='natural',
#     f_prime_start=0.0,
#     f_prime_end=0.0
# ):

#     n = len(x) - 1
#     h = np.diff(x)

#     a = np.array(y, dtype=float)

#     A_mat = np.zeros((n + 1, n + 1))
#     B_vec = np.zeros(n + 1)

#     for i in range(1, n):

#         A_mat[i, i - 1] = h[i - 1]
#         A_mat[i, i] = 2 * (h[i - 1] + h[i])
#         A_mat[i, i + 1] = h[i]

#         B_vec[i] = (
#             (3 / h[i]) * (a[i + 1] - a[i])
#             - (3 / h[i - 1]) * (a[i] - a[i - 1])
#         )

#     if boundary_type == "natural":

#         A_mat[0, 0] = 1
#         A_mat[n, n] = 1

#     else:

#         A_mat[0, 0] = 2 * h[0]
#         A_mat[0, 1] = h[0]

#         B_vec[0] = (
#             (3 / h[0]) * (a[1] - a[0])
#             - 3 * f_prime_start
#         )

#         A_mat[n, n - 1] = h[n - 1]
#         A_mat[n, n] = 2 * h[n - 1]

#         B_vec[n] = (
#             3 * f_prime_end
#             - (3 / h[n - 1]) * (a[n] - a[n - 1])
#         )

#     c = solve_tridiagonal(A_mat, B_vec)

#     b = np.zeros(n)
#     d = np.zeros(n)

#     for i in range(n):

#         b[i] = (
#             (a[i + 1] - a[i]) / h[i]
#             - h[i] * (2 * c[i] + c[i + 1]) / 3
#         )

#         d[i] = (
#             c[i + 1] - c[i]
#         ) / (3 * h[i])

#     return a[:-1], b, c[:-1], d


# def evaluate_spline(
#     x_nodes,
#     x_eval,
#     a,
#     b,
#     c,
#     d
# ):

#     y_eval = np.zeros_like(x_eval)

#     for i in range(len(x_nodes) - 1):

#         mask = (
#             (x_eval >= x_nodes[i])
#             &
#             (x_eval <= x_nodes[i + 1])
#         )

#         dx = x_eval[mask] - x_nodes[i]

#         y_eval[mask] = (
#             a[i]
#             + b[i] * dx
#             + c[i] * dx**2
#             + d[i] * dx**3
#         )

#     return y_eval


# # =====================================================
# # Data
# # =====================================================

# curves = {

#     "Curve 1": {

#         "x": np.array(
#             [1,2,5,6,7,8,10,13,17],
#             dtype=float
#         ),

#         "y": np.array(
#             [3.0,3.7,3.9,4.2,5.7,6.6,7.1,6.7,4.5],
#             dtype=float
#         ),

#         "fp_s": 1.0,
#         "fp_e": -0.67
#     },

#     "Curve 2": {

#         "x": np.array(
#             [17,20,23,24,25,27,27.7],
#             dtype=float
#         ),

#         "y": np.array(
#             [4.5,7.0,6.1,5.6,5.8,5.2,4.1],
#             dtype=float
#         ),

#         "fp_s": 3.0,
#         "fp_e": -4.0
#     },

#     "Curve 3": {

#         "x": np.array(
#             [27.7,28,29,30],
#             dtype=float
#         ),

#         "y": np.array(
#             [4.1,4.3,4.1,3.0],
#             dtype=float
#         ),

#         "fp_s": 0.33,
#         "fp_e": -1.5
#     }
# }

# # =====================================================
# # Sidebar
# # =====================================================

# st.sidebar.title("📊 Controls")

# curve_name = st.sidebar.selectbox(
#     "Select Curve",
#     list(curves.keys())
# )

# show_natural = st.sidebar.checkbox(
#     "Natural Spline",
#     True
# )

# show_clamped = st.sidebar.checkbox(
#     "Clamped Spline",
#     True
# )

# # =====================================================
# # Header
# # =====================================================

# st.markdown("""
# <h1 style='color:#2563eb'>
# 📈 Cubic Spline Interpolation Dashboard
# </h1>
# """, unsafe_allow_html=True)

# st.caption(
#     "Numerical Analysis Mini Project"
# )

# curve = curves[curve_name]

# x = curve["x"]
# y = curve["y"]

# # =====================================================
# # Metrics
# # =====================================================

# c1, c2, c3, c4 = st.columns(4)

# c1.metric(
#     "Curve",
#     curve_name
# )

# c2.metric(
#     "Points",
#     len(x)
# )

# c3.metric(
#     "Intervals",
#     len(x)-1
# )

# c4.metric(
#     "Method",
#     "TDMA"
# )

# st.divider()

# # =====================================================
# # Graph + Info
# # =====================================================

# left, right = st.columns([4,1])

# x_fine = np.linspace(
#     x[0],
#     x[-1],
#     500
# )

# fig, ax = plt.subplots(
#     figsize=(8,4)
# )

# if show_clamped:

#     a,b,c,d = compute_cubic_spline_coefficients(
#         x,
#         y,
#         "clamped",
#         curve["fp_s"],
#         curve["fp_e"]
#     )

#     y_clamped = evaluate_spline(
#         x,
#         x_fine,
#         a,b,c,d
#     )

#     ax.plot(
#     x_fine,
#     y_clamped,
#     color="#2563eb",
#     linewidth=4,
#     label="Clamped Spline"
#     )

# if show_natural:

#     a,b,c,d = compute_cubic_spline_coefficients(
#         x,
#         y,
#         "natural"
#     )

#     y_natural = evaluate_spline(
#         x,
#         x_fine,
#         a,b,c,d
#     )

#     ax.plot(
#     x_fine,
#     y_natural,
#     "--",
#     color="#f97316",
#     linewidth=4,
#     label="Natural Spline"
#     )

# ax.scatter(
#     x,
#     y,
#     color="#dc2626",
#     s=120,
#     label="Data Points",
#     zorder=5
# )

# ax.set_title(curve_name)
# ax.grid(True)
# ax.legend()

# with left:
#     st.pyplot(
#         fig,
#         use_container_width=True
#     )

# with right:

#     st.subheader("Curve Info")

#     st.write(
#         f"**Start Slope:** {curve['fp_s']}"
#     )

#     st.write(
#         f"**End Slope:** {curve['fp_e']}"
#     )

#     st.write(
#         f"**x range:** {x[0]} → {x[-1]}"
#     )

# # =====================================================
# # TDMA Demo
# # =====================================================

# st.divider()

# st.subheader(
#     "🔢 Thomas Algorithm Demo"
# )

# A = np.array([
#     [2,1,0,0,0],
#     [1,2,1,0,0],
#     [0,1,2,1,0],
#     [0,0,1,2,1],
#     [0,0,0,1,2]
# ], dtype=float)

# B = np.array(
#     [1,1,4,6,5],
#     dtype=float
# )

# if st.button("Solve AX = B"):

#     X = solve_tridiagonal(
#         A,
#         B
#     )

#     st.success(
#         "Solution Computed Successfully"
#     )

#     st.write("Solution Vector:")

#     st.code(
#         np.array2string(
#             X,
#             precision=4
#         )
#     )













# vesna
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# Page Config
# =====================================================

st.set_page_config(
    page_title="Cubic Spline Project",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="metric-container"] {
    background-color: #dbeafe;
    border: 1px solid #93c5fd;
    padding: 15px;
    border-radius: 12px;
}
[data-testid="metric-container"] label {
    color: #1e3a8a;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# Thomas Algorithm
# =====================================================

def solve_tridiagonal(A_matrix, B_vector):

    n = len(B_vector)
    a = np.zeros(n)
    b = np.zeros(n)
    c = np.zeros(n)

    b[0] = A_matrix[0, 0]
    c[0] = A_matrix[0, 1]

    for i in range(1, n - 1):
        a[i] = A_matrix[i, i - 1]
        b[i] = A_matrix[i, i]
        c[i] = A_matrix[i, i + 1]

    a[n - 1] = A_matrix[n - 1, n - 2]
    b[n - 1] = A_matrix[n - 1, n - 1]

    c_prime = np.zeros(n)
    d_prime = np.zeros(n)

    c_prime[0] = c[0] / b[0]
    d_prime[0] = B_vector[0] / b[0]

    for i in range(1, n):
        den = b[i] - a[i] * c_prime[i - 1]
        if i < n - 1:
            c_prime[i] = c[i] / den
        d_prime[i] = (B_vector[i] - a[i] * d_prime[i - 1]) / den

    X = np.zeros(n)
    X[n - 1] = d_prime[n - 1]
    for i in range(n - 2, -1, -1):
        X[i] = d_prime[i] - c_prime[i] * X[i + 1]

    return X


# =====================================================
# Cubic Spline
# =====================================================

def compute_cubic_spline_coefficients(
    x, y, boundary_type='natural',
    f_prime_start=0.0, f_prime_end=0.0
):
    n = len(x) - 1
    h = np.diff(x)
    a = np.array(y, dtype=float)

    A_mat = np.zeros((n + 1, n + 1))
    B_vec = np.zeros(n + 1)

    for i in range(1, n):
        A_mat[i, i - 1] = h[i - 1]
        A_mat[i, i]     = 2 * (h[i - 1] + h[i])
        A_mat[i, i + 1] = h[i]
        B_vec[i] = (
            (3 / h[i]) * (a[i + 1] - a[i])
            - (3 / h[i - 1]) * (a[i] - a[i - 1])
        )

    if boundary_type == "natural":
        A_mat[0, 0] = 1
        A_mat[n, n] = 1
    else:
        A_mat[0, 0] = 2 * h[0]
        A_mat[0, 1] = h[0]
        B_vec[0] = (3 / h[0]) * (a[1] - a[0]) - 3 * f_prime_start
        A_mat[n, n - 1] = h[n - 1]
        A_mat[n, n]     = 2 * h[n - 1]
        B_vec[n] = 3 * f_prime_end - (3 / h[n - 1]) * (a[n] - a[n - 1])

    c = solve_tridiagonal(A_mat, B_vec)

    b = np.zeros(n)
    d = np.zeros(n)
    for i in range(n):
        b[i] = (a[i + 1] - a[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])

    return a[:-1], b, c[:-1], d


def evaluate_spline(x_nodes, x_eval, a, b, c, d):
    y_eval = np.zeros_like(x_eval)
    for i in range(len(x_nodes) - 1):
        mask = (x_eval >= x_nodes[i]) & (x_eval <= x_nodes[i + 1])
        dx = x_eval[mask] - x_nodes[i]
        y_eval[mask] = a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3
    return y_eval


# =====================================================
# Default Project Data
# =====================================================

DEFAULT_CURVES = {
    "Curve 1": {
        "x": [1, 2, 5, 6, 7, 8, 10, 13, 17],
        "y": [3.0, 3.7, 3.9, 4.2, 5.7, 6.6, 7.1, 6.7, 4.5],
        "fp_s": 1.0,
        "fp_e": -0.67
    },
    "Curve 2": {
        "x": [17, 20, 23, 24, 25, 27, 27.7],
        "y": [4.5, 7.0, 6.1, 5.6, 5.8, 5.2, 4.1],
        "fp_s": 3.0,
        "fp_e": -4.0
    },
    "Curve 3": {
        "x": [27.7, 28, 29, 30],
        "y": [4.1, 4.3, 4.1, 3.0],
        "fp_s": 0.33,
        "fp_e": -1.5
    }
}

# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("📊 Controls")

# --- Dataset mode ---
data_mode = st.sidebar.radio(
    "Dataset",
    ["📂 Project Data", "✏️ Custom Input"],
    index=0
)

st.sidebar.divider()

if data_mode == "📂 Project Data":

    curve_name = st.sidebar.selectbox(
        "Select Curve",
        list(DEFAULT_CURVES.keys())
    )

    curve = DEFAULT_CURVES[curve_name]
    x = np.array(curve["x"], dtype=float)
    y = np.array(curve["y"], dtype=float)
    fp_s = curve["fp_s"]
    fp_e = curve["fp_e"]
    label = curve_name

else:
    # ---- Custom Input ----
    st.sidebar.subheader("Enter Your Data")

    label = st.sidebar.text_input("Dataset name", value="Custom Curve")

    n_pts = st.sidebar.number_input(
        "Number of points", min_value=3, max_value=20, value=5, step=1
    )

    st.sidebar.markdown("**X values** (comma-separated)")
    x_raw = st.sidebar.text_input(
        "x", value=", ".join(["0", "1", "2", "3", "4"][:n_pts])
    )

    st.sidebar.markdown("**Y values** (comma-separated)")
    y_raw = st.sidebar.text_input(
        "y", value=", ".join(["0", "1", "0", "-1", "0"][:n_pts])
    )

    fp_s = st.sidebar.number_input("Start slope (clamped)", value=1.0, step=0.1)
    fp_e = st.sidebar.number_input("End slope (clamped)",   value=0.0, step=0.1)

    try:
        x = np.array([float(v.strip()) for v in x_raw.split(",")])
        y = np.array([float(v.strip()) for v in y_raw.split(",")])

        if len(x) != len(y):
            st.sidebar.error("x and y must have the same number of values.")
            st.stop()

        if len(x) < 3:
            st.sidebar.error("Need at least 3 points.")
            st.stop()

        if not np.all(np.diff(x) > 0):
            st.sidebar.error("x values must be strictly increasing.")
            st.stop()

    except ValueError:
        st.sidebar.error("Invalid numbers. Use commas to separate values.")
        st.stop()

st.sidebar.divider()

show_natural = st.sidebar.checkbox("Natural Spline",  True)
show_clamped = st.sidebar.checkbox("Clamped Spline",  True)
show_table   = st.sidebar.checkbox("Show Coefficient Table", False)

# =====================================================
# Header
# =====================================================

st.markdown("""
<h1 style='color:#2563eb'>
📈 Cubic Spline Interpolation Dashboard
</h1>
""", unsafe_allow_html=True)

st.caption("Numerical Analysis Mini Project")

# =====================================================
# Metrics
# =====================================================

c1, c2, c3, c4 = st.columns(4)
c1.metric("Dataset",   label)
c2.metric("Points",    len(x))
c3.metric("Intervals", len(x) - 1)
c4.metric("Method",    "TDMA")

st.divider()

# =====================================================
# Graph + Info
# =====================================================

left, right = st.columns([4, 1])

x_fine = np.linspace(x[0], x[-1], 500)

fig, ax = plt.subplots(figsize=(8, 4))

coeff_nat = coeff_clamp = None

if show_clamped:
    coeff_clamp = compute_cubic_spline_coefficients(
        x, y, "clamped", fp_s, fp_e
    )
    y_clamped = evaluate_spline(x, x_fine, *coeff_clamp)
    ax.plot(x_fine, y_clamped,
            color="#2563eb", linewidth=4, label="Clamped Spline")

if show_natural:
    coeff_nat = compute_cubic_spline_coefficients(x, y, "natural")
    y_natural = evaluate_spline(x, x_fine, *coeff_nat)
    ax.plot(x_fine, y_natural,
            "--", color="#f97316", linewidth=4, label="Natural Spline")

ax.scatter(x, y, color="#dc2626", s=120, label="Data Points", zorder=5)
ax.set_title(label)
ax.grid(True)
ax.legend()

with left:
    st.pyplot(fig, use_container_width=True)

with right:
    st.subheader("Info")
    st.write(f"**x range:** {x[0]} → {x[-1]}")
    st.write(f"**Start slope:** {fp_s}")
    st.write(f"**End slope:** {fp_e}")

# =====================================================
# Optional Coefficient Table
# =====================================================

if show_table:
    st.divider()
    st.subheader("📋 Spline Coefficients")

    import pandas as pd

    def make_df(coeffs, x_nodes):
        a, b, c, d = coeffs
        rows = []
        for i in range(len(a)):
            rows.append({
                "i": i,
                f"[x_i, x_{{i+1}}]": f"[{x_nodes[i]:.3g}, {x_nodes[i+1]:.3g}]",
                "a_i": round(a[i], 6),
                "b_i": round(b[i], 6),
                "c_i": round(c[i], 6),
                "d_i": round(d[i], 6),
            })
        return pd.DataFrame(rows).set_index("i")

    if show_natural and coeff_nat:
        st.markdown("**Natural Spline**")
        st.dataframe(make_df(coeff_nat, x), use_container_width=True)

    if show_clamped and coeff_clamp:
        st.markdown("**Clamped Spline**")
        st.dataframe(make_df(coeff_clamp, x), use_container_width=True)

# =====================================================
# TDMA Demo
# =====================================================

st.divider()
st.subheader("🔢 Thomas Algorithm Demo")

A = np.array([
    [2,1,0,0,0],
    [1,2,1,0,0],
    [0,1,2,1,0],
    [0,0,1,2,1],
    [0,0,0,1,2]
], dtype=float)

B = np.array([1,1,4,6,5], dtype=float)

if st.button("Solve AX = B"):
    X = solve_tridiagonal(A, B)
    st.success("Solution Computed Successfully")
    st.write("Solution Vector:")
    st.code(np.array2string(X, precision=4))