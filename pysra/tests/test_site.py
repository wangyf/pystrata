#!/usr/bin/env python
# encoding: utf-8

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright (C) Albert Kottke, 2013-2015

import nose
from numpy.testing import assert_almost_equal, assert_approx_equal

from pysra import site


def nlp_setup():
    """Setup for the NonlinearProperty tests"""
    global nlp
    nlp = site.NonlinearProperty('', [0.01, 1], [0., 1.])


def nlp_teardown():
    """Teardown for the NonlinearProperty tests"""
    global nlp
    del nlp


@nose.with_setup(nlp_setup, nlp_teardown)
def test_nlp_lowerbound():
    global nlp
    assert_almost_equal(nlp(0.001), 0.)


@nose.with_setup(nlp_setup, nlp_teardown)
def test_nlp_upperbound():
    global nlp
    assert_almost_equal(nlp(2.), 1.)


@nose.with_setup(nlp_setup, nlp_teardown)
def test_nlp_midpoint():
    global nlp
    assert_approx_equal(nlp(0.1), 0.5)


@nose.with_setup(nlp_setup, nlp_teardown)
def test_nlp_update():
    global nlp
    new_values = [0, 2]
    nlp.values = new_values
    assert_almost_equal(new_values, nlp.values)

    new_strains = [0.1, 10]
    nlp.strains = new_strains
    assert_almost_equal(new_strains, nlp.strains)

    assert_approx_equal(nlp(1.), 1.)


def test_iterative_value():
    """Test the iterative value and relative error."""
    iv = site.IterativeValue(11)
    value = 10
    iv.value = value
    assert_approx_equal(iv.value, value)
    assert_approx_equal(iv.relative_error, 10.)


def test_soil_type_linear():
    """Test the soil type update process on a linear material."""
    damping = 1.0
    l = site.Layer(site.SoilType('', 18.0, None, damping), 2., 500.)
    l.strain = 0.1

    assert_approx_equal(l.shear_mod.value, l.initial_shear_mod)
    assert_approx_equal(l.damping.value, damping)


def test_soil_type_iterative():
    """Test the soil type update process on a nonlinear property."""
    mod_reduc = site.NonlinearProperty('', [0.01, 1.], [1, 0])
    damping = site.NonlinearProperty('', [0.01, 1.], [0, 10])

    st = site.SoilType('', 18.0, mod_reduc, damping)
    l = site.Layer(st, 2., 500.)

    strain = 0.1
    l.strain = strain

    assert_approx_equal(l.strain.value, strain)
    assert_approx_equal(l.shear_mod.value, 0.5 * l.initial_shear_mod)
    assert_approx_equal(l.damping.value, 5.0)

