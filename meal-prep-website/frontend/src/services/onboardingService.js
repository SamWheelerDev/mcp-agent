import api from './api';

const onboardingService = {
  // Start the onboarding process for a user
  startOnboarding: async (userId) => {
    const response = await api.post('/onboarding/start', {
      user_id: userId
    });
    return response.data;
  },
  
  // Process an onboarding step
  processStep: async (userId, stepId, data) => {
    const response = await api.post('/onboarding/step', {
      user_id: userId,
      step_data: {
        step_id: stepId,
        data: data
      }
    });
    return response.data;
  },
  
  // Get the current onboarding step for a user
  getCurrentStep: async (userId) => {
    const response = await api.get(`/onboarding/current-step/${userId}`);
    return response.data;
  },
  
  // Complete the onboarding process
  completeOnboarding: async (userId) => {
    const response = await api.post('/onboarding/complete', {
      user_id: userId
    });
    return response.data;
  },
  
  // Get user preferences
  getUserPreferences: async (userId) => {
    const response = await api.get(`/onboarding/preferences/${userId}`);
    return response.data;
  }
};

export default onboardingService;
