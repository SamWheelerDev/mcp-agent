import api from './api';

const calendarService = {
  // Get meal plans for a user within a date range
  getMealPlans: async (userId, startDate, endDate) => {
    const params = { user_id: userId };
    
    if (startDate) {
      params.start_date = startDate;
    }
    
    if (endDate) {
      params.end_date = endDate;
    }
    
    const response = await api.get('/calendar/meal-plans', { params });
    return response.data;
  },
  
  // Create a new meal plan
  createMealPlan: async (mealPlanData) => {
    const response = await api.post('/calendar/meal-plans', mealPlanData);
    return response.data;
  },
  
  // Delete a meal plan
  deleteMealPlan: async (mealPlanId) => {
    const response = await api.delete(`/calendar/meal-plans/${mealPlanId}`);
    return response.data;
  },
  
  // Generate a weekly meal plan
  generateWeeklyPlan: async (userId, startDate) => {
    const params = { user_id: userId };
    
    if (startDate) {
      params.start_date = startDate;
    }
    
    const response = await api.post('/calendar/generate-weekly-plan', null, { params });
    return response.data;
  }
};

export default calendarService;
