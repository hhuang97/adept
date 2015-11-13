from buffalo import utils
from recipeManager import RecipeManager
utils.init()

class TestRecipe:
	def test_manager(self):
		RecipeManager.loadRecipes()
		assert len(RecipeManager.RECIPES) > 0
