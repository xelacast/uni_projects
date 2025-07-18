import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button

def norm_eig_vec(eigenvectors):
    m = sym.Matrix(eigenvectors[0,0]/eigenvectors).elementary_row_op(op="n<->m", row1=0, row2=1)
    return np.array(m)

def find_c(eig_vec, x_0):
    c_mat = np.append(eig_vec, x_0, axis=1)
    symp_matrix = sym.Matrix(c_mat)
    c_reff = symp_matrix.rref()
    return c_reff[0].col(2)

def dynamic_differential_war(a_coef, b_coef, x_0=np.array([[0],[0]])):
    A = np.array([[0, -a_coef], [-b_coef, 0]])
    eigenvalues, eigenvectors = np.linalg.eig(A)
    lambda_1, lambda_2 = eigenvalues
    eigenvector_norm = norm_eig_vec(eigenvectors)
    v1, v2 = eigenvector_norm[:, 0], eigenvector_norm[:, 1]
    c1, c2 = find_c(eigenvector_norm, x_0)
    def x(t):
        return c1*v1*np.exp(lambda_1*t) + c2*v2*np.exp(lambda_2*t)
    return x


def create_data(time, a, b, x_0):
    x = dynamic_differential_war(a, b, x_0=x_0)
    arr = np.array([[],[]])
    for num in time:
        x_plus_one = x(num).reshape(-1,1)
        arr = np.append(arr, x_plus_one, axis=1)
    return arr


if __name__ == '__main__':
    # what if i wanted to normalize T? lets 3D graph
    fig, ax = plt.subplots()
    a = 5
    b = 10
    x_0 = np.array([[24], [36]])
    time_series = np.linspace(0,2,num=25) # a time stamp for every month for 3 years
    war_data = create_data(time_series, 5, 10, x_0)
    team_a = war_data[0, :]
    team_b = war_data[1, :]

    line, = ax.plot(time_series, team_a, lw=2, label="A Units")
    line2, = ax.plot(time_series, team_b, lw=2, label="B Units")
    x_aves = ax.plot(time_series, time_series*0, lw=0.5, linestyle='--')
    ax.set_xlabel('Time [y]')
    ax.set_ylabel('Units')
    fig.subplots_adjust(left=0.25, bottom=0.25)
    init_text = ax.text(0.5, 2, f"x_0: A units: {x_0[0,0]}, B Units: {x_0[1,0]}")
    init_text.set_x(-0.5)
    init_text.set_y(225)
    unit_values = ax.text(-0.1, -0.1, f"2 year values, A units: {team_a[-1]}, B Units: {team_b[-1]}")
    unit_values.set_x(-0.5)
    unit_values.set_y(210)

    # horizontal sliders
    ax_a=fig.add_axes([0.25, 0.1, 0.65, 0.03])
    a_slider = Slider(
        ax=ax_a,
        label='A Decay',
        valmin=0.01,
        valmax=30,
        valinit=a,
        valstep=0.01
    )
    ax_b=fig.add_axes([0.25, 0.05, 0.65, 0.03])
    b_slider = Slider(
        ax=ax_b,
        label='B Decay',
        valmin=0.01,
        valmax=30,
        valinit=b,
        valstep=0.01
    )
    ax_a_u = fig.add_axes([0.1, 0.25, 0.0225, 0.60] )
    a_unit_slider = Slider(
        ax=ax_a_u,
        label='A',
        valmin=1,
        valmax=200,
        valinit=x_0[0,0],
        orientation='vertical',
        valstep=1,
    )
    ax_b_u = fig.add_axes([0.05, 0.25, 0.0225, 0.60] )
    b_unit_slider = Slider(
        ax=ax_b_u,
        label='B',
        valmin=1,
        valmax=200,
        valinit=x_0[1,0],
        orientation='vertical',
        valstep=1,
    )

    def update(val):
        x_0 = np.array([[a_unit_slider.val], [b_unit_slider.val]])
        data = create_data(time_series, a_slider.val, b_slider.val, x_0)
        a = data[0, :]
        b = data[1, :]
        line.set_ydata(a)
        line2.set_ydata(b)
        fig.canvas.draw_idle()
        unit_values.set_text(f"2 year values, A units: {a[-1]}, B Units: {b[-1]}")
        init_text.set_text(f"x_0: A units: {x_0[0,0]}, B Units: {x_0[1,0]}")

    a_slider.on_changed(update)
    b_slider.on_changed(update)
    a_unit_slider.on_changed(update)
    b_unit_slider.on_changed(update)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = fig.add_axes([0.8, 0.01, 0.1, 0.04])
    button = Button(resetax, 'Reset', hovercolor='0.975')

    def reset(event):
        a_slider.reset()
        b_slider.reset()
        b_unit_slider.reset()
        a_unit_slider.reset()
    button.on_clicked(reset)

    ax.set_ylim(-100, 200)
    ax.legend()
    plt.show()