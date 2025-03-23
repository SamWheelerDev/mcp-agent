import api from './api';

const chatService = {
  // Send a message and get a response
  sendMessage: async (userId, message) => {
    const response = await api.post('/chat/chat', {
      user_id: userId,
      message: message
    });
    return response.data;
  },
  
  // Get chat history for a user
  getChatHistory: async (userId, skip = 0, limit = 100) => {
    const response = await api.get(`/chat/history/${userId}`, {
      params: { skip, limit }
    });
    return response.data;
  }
};

export default chatService;
