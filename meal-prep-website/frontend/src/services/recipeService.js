import api from './api';

const recipeService = {
  // Get all recipes with optional search and pagination
  getRecipes: async (search = '', page = 0, limit = 10) => {
    const skip = page * limit;
    const params = { skip, limit };
    
    if (search) {
      params.search = search;
    }
    
    const response = await api.get('/recipes', { params });
    return response.data;
  },
  
  // Get a single recipe by ID
  getRecipe: async (id) => {
    const response = await api.get(`/recipes/${id}`);
    return response.data;
  },
  
  // Create a new recipe
  createRecipe: async (recipeData) => {
    const response = await api.post('/recipes', recipeData);
    return response.data;
  },
  
  // Update an existing recipe
  updateRecipe: async (id, recipeData) => {
    const response = await api.put(`/recipes/${id}`, recipeData);
    return response.data;
  },
  
  // Delete a recipe
  deleteRecipe: async (id) => {
    const response = await api.delete(`/recipes/${id}`);
    return response.data;
  }
};

export default recipeService;
