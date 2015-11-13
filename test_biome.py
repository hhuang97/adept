from buffalo import utils
from biome import Biome
utils.init()

class TestBiome:
	def test_init(self):
		b = Biome.GenerateBiomeDefs()
		assert len(b) >= 9