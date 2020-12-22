import pytest



class TestDemo2:



    @pytest.mark.parametrize('min, max', [(1, 2), (3, 4)])
    def test_indirect(self,min, max):
        print(min)
        print(max)
        assert min <= max
        assert 1<2

    # min max 对应的实参重定向到同名的 fixture 中

    @pytest.mark.parametrize('min', [11], indirect=True)
    @pytest.mark.parametrize('max', [1,2,3,4,5,6], indirect=True)
    def test_indirect_indirect(self, min, max):
        print(min)
        print(max)
        assert min >= max
        assert 1 > 0

    # 只将 max 对应的实参重定向到 fixture 中
    @pytest.mark.parametrize('min, max', [(1, 2), (3, 4)], indirect=['max'])
    def test_indirect_part_indirect(self, min, max):
        print(min)
        print(max)
        assert min == max
        assert 1 > 2




