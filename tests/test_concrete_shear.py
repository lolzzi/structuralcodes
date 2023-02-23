import math

import pytest

from structuralcodes.codes.mc2010 import _concrete_shear


@pytest.mark.parametrize(
    'E_s, As, Med, Ved, Ned, z, deltaE, expected',
    [
        (200000, 1000, 50000000, 10000, 2000, 160, 50, 8.1e-4),
        (210000, 1000, 50000000, 10000, 2000, 160, 50, 7.7e-4),
        (210000, 5000, 50000000, 10000, 2000, 160, 50, 1.5e-4),
        (210000, 2000, 50000000, 10000, 2000, 160, 50, 3.9e-4),
        (210000, 2000, 40000000, 20000, 2000, 160, 50, 3.2e-4),
        (210000, 2000, 40000000, 20000, 1000, 160, 50, 3.2e-4),
        (210000, 2000, 40000000, 20000, 1000, 140, 50, 3.64965e-4),
        (210000, 2000, 40000000, 20000, 1000, 180, 50, 2.9e-4),
    ],
)
def test_epsilon_x(E_s, As, Med, Ved, Ned, z, deltaE, expected):
    """Test the epsilon_x function."""
    assert math.isclose(_concrete_shear.epsilon_x(
        E_s, As, Med, Ved, Ned, z, deltaE), expected, rel_tol=0.05
    )


@pytest.mark.parametrize(
    '''approx_lvl_s, fck, bw, theta, z, E_s, As, Med, Ved,
    Ned, delta_e, alfa, gamma_c, expected''',
    [
        (1, 30, 50, 20, 200, 210000, 1000, 200e6,
         50e3, 10e3, 50, 20, 1.5, 70707),
        (2, 30, 50, 20, 200, 210000, 1000, 200e6,
         50e3, 10e3, 50, 20, 1.5, 39997),
        (2, 30, 50, 20, 200, 210000, 1000, 50e6,
         10e3, 10e3, 50, 20, 1.5, 55179.55),
        (2, 30, 50, 45, 200, 210000, 1000, 0, 0, 0, 50, 20, 1.5, 243586),
        (2, 30, 50, 45, 200, 210000, 1000, 0, 0, 0, 50, 45, 1.5, 130000),
        (3, 30, 50, 20, 200, 210000, 1000, 50e6,
         10e3, 10e3, 50, 20, 1.5, 102995),
    ],
)
def test_vrd_max(
    approx_lvl_s, fck, bw, theta, z, E_s, As, Med, Ved, Ned,
    delta_e, alfa, gamma_c, expected
):
    """Test the v_rd_max function."""
    assert math.isclose(_concrete_shear.v_rd_max(
        approx_lvl_s, fck, bw, theta, z, E_s, As, Med, Ved, Ned,
        delta_e, alfa, gamma_c), expected, rel_tol=0.5
    )


@pytest.mark.parametrize(
    '''approx_lvl_c, approx_lvl_s, fck, z, bw, dg, E_s, As, Med,
     Ved, Ned, delta_e, alfa, gamma_c, expected''',
    [
        (1, 0, 35, 180, 300, 0, 0, 0, 0, 0, 0, 0, 0, 1.5, 31294),
        (1, 0, 35, 200, 300, 0, 0, 0, 0, 0, 0, 0, 0, 1.5, 34077),
        (1, 1, 35, 200, 300, 0, 0, 0, 0, 0, 0, 0, 0, 1.5, 34077),
        (2, 1, 35, 140, 300, 16, 21e4, 2000, 40e6, 2e4, 1000, 50, 0, 1.5,
         48828),
        (2, 1, 35, 140, 300, 32, 21e4, 2000, 40e6, 2e4, 1000, 50, 0, 1.5,
         50375),
        (0, 3, 35, 200, 300, 32, 21e4, 2000, 40e6, 2e4, 1000, 50, 1.5, 1.5,
         67566),
        (0, 3, 35, 200, 300, 32, 21e4, 2000, 40e6, 20e6, 1000, 50, 1.5, 1.5,
         0),
    ],
)
def test_v_rdc(
    approx_lvl_c, approx_lvl_s, fck, z, bw, dg, E_s, As, Med,
    Ved, Ned, delta_e, alfa, gamma_c, expected
):

    """Test the v_rdc function."""
    assert math.isclose(_concrete_shear.v_rdc(
                approx_lvl_c, approx_lvl_s, fck, z, bw, dg, E_s, As, Med, Ved,
                Ned, delta_e, alfa, gamma_c
                ),
        expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''asw, sw, z, fywd, theta, alpha, expected''',
    [
        (1600, 50, 200, 355, 25, 30, 4403769),
        (2000, 50, 200, 355, 25, 30, 5504711),
        (1600, 50, 200, 355, 25, 30, 4403769),
        (1600, 100, 200, 355, 25, 30, 2201884),
        (1600, 50, 200, 275, 25, 30, 3411370),
        (1600, 50, 200, 355, 22, 30, 4779308),
        (1600, 50, 200, 355, 25, 25, 4118262),
    ],
)
def test_v_rds(asw, sw, z, fywd, theta, alpha, expected):

    """Test the v_rds function."""
    assert math.isclose(_concrete_shear.v_rds(
                asw, sw, z, fywd, theta, alpha
                ),
        expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''approx_lvl_h, f_ctd, i_c, s_c, b_w, sigma_cp, l_x, l_bd0, S_cy,
    b_wy, y, y_c, A_c, A_cy, y_pt, f_p_lx, f_p_lx_dx, expected''',
    [
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 839136),
        (1, 3.5, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 976183),
        (1, 2.6, 5e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 699280),
        (1, 2.6, 6e8, 5e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 1006963),
        (1, 2.6, 6e8, 6e5, 40, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 671309),
        (1, 2.6, 6e8, 6e5, 50, 180, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 918050),
        (1, 2.6, 6e8, 6e5, 50, 150, 35, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 785800),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 25, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 918050),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 2e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 839136),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 2e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 839136),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 80, 200, 2000, 1000, 80,
         1000e3, 200e3, 839136),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 180, 2000, 1000, 80,
         1000e3, 200e3, 839136),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 1800, 1000, 80,
         1000e3, 200e3, 839136),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1200, 80,
         1000e3, 200e3, 839136),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 60,
         1000e3, 200e3, 839136),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         800e3, 200e3, 839136),
        (1, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 250e3, 839136),

        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 160002777),
        (2, 3.5, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 214002777),
        (2, 2.6, 5e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 137336111),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 160002777),
        (2, 2.6, 6e8, 6e5, 40, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 160002777),
        (2, 2.6, 6e8, 6e5, 50, 180, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 160002777),
        (2, 2.6, 6e8, 6e5, 50, 150, 35, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 160002430),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 25, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 160003333),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 2e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 228004166),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 2e5, 100, 200, 2000, 1000, 80,
         1000e3, 200e3, 108001851),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 80, 200, 2000, 1000, 80,
         1000e3, 200e3, 160003333),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 180, 2000, 1000, 80,
         1000e3, 200e3, 156002222),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 1800, 1000, 80,
         1000e3, 200e3, 157780864),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1200, 80,
         1000e3, 200e3, 156002777),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 60,
         1000e3, 200e3, 164002777),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         800e3, 200e3, 160002222),
        (2, 2.6, 6e8, 6e5, 50, 150, 40, 30, 3e6, 3e5, 100, 200, 2000, 1000, 80,
         1000e3, 250e3, 161002777),

    ],
)
def test_v_rd_ct(
    approx_lvl_h, f_ctd, i_c, s_c, b_w, sigma_cp, l_x, l_bd0, S_cy,
    b_wy, y, y_c, A_c, A_cy, y_pt, f_p_lx, f_p_lx_dx, expected
):

    """Test the v_rd_ct function."""
    assert math.isclose(_concrete_shear.v_rd_ct(
        approx_lvl_h, f_ctd, i_c, s_c, b_w, sigma_cp, l_x, l_bd0, S_cy,
        b_wy, y, y_c, A_c, A_cy, y_pt, f_p_lx, f_p_lx_dx
    ),
        expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''beta, v_ed, z, b_i, expected''',
    [
        (0.7, 50e3, 200, 50, 3.5),
        (0.75, 50e3, 200, 50, 3.75),
        (0.7, 40e3, 200, 50, 2.8),
        (0.7, 50e3, 180, 50, 3.888),
        (0.7, 50e3, 200, 60, 2.916),
    ],
)
def test_tau_edi(beta, v_ed, z, b_i, expected):

    """Test the tau_edi function."""
    assert math.isclose(_concrete_shear.tau_edi(
        beta, v_ed, z, b_i
    ),
        expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''c_a, f_ctd, mu, sigma_n, f_ck, f_cd, expected''',
    [
        (0.2, 2.6, 0.6, 100, 30, 17, 4.675),
        (0.2, 3.5, 0.6, 100, 30, 17, 4.675),
        (0.2, 2.6, 0.7, 100, 30, 17, 4.675),
        (0.2, 2.6, 0.6, 80, 30, 17, 4.675),
        (0.2, 2.6, 0.6, 100, 20, 11.3, 3.1075),
        (0.2, 2.6, 0.6, 100, 30, 17, 4.675),
    ],
)
def test_tau_rdi_without_reinforcement(
    c_a, f_ctd, mu, sigma_n, f_ck, f_cd, expected
):

    """Test the tau_rdi_without_reinforcement function."""
    assert math.isclose(_concrete_shear.tau_rdi_without_reinforceent(
        c_a, f_ctd, mu, sigma_n, f_ck, f_cd
    ),
        expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''c_r, k1, k2, mu, ro, sigma_n, alfa,
    beta_c, f_ck, f_yd, f_cd, expected''',
    [
        (0.1, 0.5, 0.9, 0.7, 0.05, 100, 15, 0.5, 30, 434, 17, 4.675),
    ],
)
def test_tau_rdi_with_reinforcement(
    c_r, k1, k2, mu, ro, sigma_n, alfa, beta_c, f_ck, f_yd, f_cd, expected
):

    """Test the tau_rdi_with_reinforcement function."""
    assert math.isclose(_concrete_shear.tau_rdi_with_reinforcement(
        c_r, k1, k2, mu, ro, sigma_n, alfa, beta_c, f_ck, f_yd, f_cd
    ),
        expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''approx_lvl_c, approx_lvl_s, reinforcment, fck, z,
    bw, dg, E_s, As, Med, Ved, Ned, delta_e, alfa, gamma_c,
    asw, sw, f_ywd, theta, expected''',
    [
        (1, 0, False, 35, 180, 200, 16, 200000, 2000, 0, 2000, 0, 20, 90, 1.5,
         0, 0, 434, 40, 20863),
        (2, 0, False, 35, 180, 200, 16, 200000, 2000, 0, 2000, 0, 20, 90, 1.5,
         0, 0, 434, 40, 62336),
        (2, 3, True, 35, 180, 200, 16, 200000, 2000, 0, 2000, 0, 20, 90, 1.5,
         500, 200, 434, 40, 126506),
        (2, 2, True, 35, 180, 200, 16, 200000, 2000, 0, 2000, 0, 20, 90, 1.5,
         500, 200, 434, 40, 232749),
        (2, 1, True, 35, 180, 200, 16, 200000, 2000, 0, 2000, 0, 20, 90, 1.5,
         500, 200, 434, 40, 216096),
    ],
)
def test_v_rd(
    approx_lvl_c, approx_lvl_s, reinforcment, fck, z,
    bw, dg, E_s, As, Med, Ved, Ned, delta_e, alfa, gamma_c,
    asw, sw, f_ywd, theta, expected
):

    """Test the tau_edi function."""
    assert math.isclose(_concrete_shear.v_rd(
        approx_lvl_c, approx_lvl_s, reinforcment, fck, z,
        bw, dg, E_s, As, Med, Ved, Ned, delta_e, alfa, gamma_c,
        asw, sw, f_ywd, theta
    ),
        expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''t_ed, a_k, z_i, expected''',
    [
        (2000000, 2000, 300, 150000),
    ],
)
def test_ved_ti(t_ed, a_k, z_i, expected):

    """Test the ved_ti function."""
    assert math.isclose(_concrete_shear.v_ed_ti(t_ed, a_k, z_i),
                        expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''f_ck, gamma_c, d_k, a_k, theta, approx_lvl_s, E_s, As,
        Med, Ved, Ned, z, delta_e, expected''',
    [
        (35, 1.5, 150, 50000, 40, 1, 200000, 2000, 0, 2000, 0, 180, 20,
         11256044),
        (35, 1.5, 150, 50000, 40, 2, 200000, 2000, 0, 2000, 0, 180, 20,
         13301400),
        (35, 1.5, 150, 50000, 40, 3, 200000, 2000, 0, 2000, 0, 180, 20,
         10084000),

    ],
)
def test_t_rd_max(
        f_ck, gamma_c, d_k, a_k, theta, approx_lvl_s, E_s, As,
        Med, Ved, Ned, z, delta_e, expected):

    """Test the t_rd_max function."""
    assert math.isclose(_concrete_shear.t_rd_max(
            f_ck, gamma_c, d_k, a_k, theta, approx_lvl_s, E_s, As,
            Med, Ved, Ned, z, delta_e), expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''t_ed, approx_lvl_s, fck, bw, theta, z, E_s, As,
        Med, Ved, Ned, delta_e, alfa, d_k, a_k, gamma_c, expected''',
    [
        (100e3, 1, 35, 200, 40, 180, 200000, 2000, 0, 10e3, 10e3, 20,
         90, 150, 50000, 1.5, True),
        (100e3, 1, 35, 200, 40, 180, 200000, 2000, 0, 1000e3, 10e3, 20,
         90, 150, 50000, 1.5, False),
        (100e3, 1, 35, 200, 40, 180, 200000, 2000, 0, 10e3, 10e3, 20,
         90, 150, 50000, 1.5, True),
        (10000e3, 1, 35, 200, 40, 180, 200000, 2000, 0, 10e3, 10e3, 20,
         90, 150, 50000, 1.5, False),
    ],
)
def test_t_rd(
        t_ed, approx_lvl_s, fck, bw, theta, z, E_s, As,
        Med, Ved, Ned, delta_e, alfa, d_k, a_k, gamma_c, expected
        ):

    """Test the t_rd function."""
    assert math.isclose(_concrete_shear.t_rd(
        t_ed, approx_lvl_s, fck, bw, theta, z, E_s, As,
        Med, Ved, Ned, delta_e, alfa, d_k, a_k, gamma_c), expected)


@pytest.mark.parametrize(
    '''Ved, e_u, l_x, l_y, l_min, inner,
    edge_par, edge_per, corner, expected''',
    [
        (10e3, 20, 2e3, 2e3, 2000, True, False, False, False, 1401),
        (10e3, 20, 2e3, 3e3, 2000, False, True, False, False, 2500),
        (10e3, 20, 2e3, 3e3, 2000, False, False, True, False, 1497),
        (10e3, 20, 2e3, 3e3, 2000, False, False, False, True, 5000),
    ],
)
def test_m_ed(
    Ved, e_u, l_x, l_y, l_min, inner,
    edge_par, edge_per, corner, expected
):

    """Test the m_ed function."""
    assert math.isclose(_concrete_shear.m_ed(
        Ved, e_u, l_x, l_y, l_min, inner,
        edge_par, edge_per, corner), expected, rel_tol=0.001)


@pytest.mark.parametrize(
    '''l_x, l_y, f_yd, d, e_s, approx_lvl_p, Ved, e_u,
    l_min, inner, edge_par, edge_per, corner, m_rd,
    m_pd, expected''',
    [
        (2e3, 3e3, 434, 160, 200e3, 1, 50e3, 20, 2e3,
         True, False, False, False, 140, 0, 0.013426875),
        (2e3, 3e3, 434, 160, 200e3, 2, 10e3, 20, 2e3,
         True, False, False, False, 140, 0, 0.41269218238),
    ],
)
def test_psi_punching(
    l_x, l_y, f_yd, d, e_s, approx_lvl_p, Ved, e_u,
    l_min, inner, edge_par, edge_per, corner, m_rd,
    m_pd, expected
):

    """Test the psi_punching function."""
    assert math.isclose(_concrete_shear.psi_punching(
        l_x, l_y, f_yd, d, e_s, approx_lvl_p, Ved, e_u,
        l_min, inner, edge_par, edge_per, corner, m_rd,
        m_pd), expected, rel_tol=0.001)
