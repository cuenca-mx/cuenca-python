from cuenca.resources import Card


def test_update():
    c = Card(id='100', number='123345', cvv=123)
    c.cvv = 1111
    c.update()
    assert c.id == '100'
    assert c.cvv == 1111
